"""
eap.py

EAP - EPD Analysis to PGN

Analyze EPD with an engine and create a PGN with engine pv as moves.
"""


import time
from pathlib import Path
import argparse
import logging

import chess
import chess.pgn
import chess.engine


APP_NAME = 'EAP - EPD Analysis to PGN'
APP_VERSION = 'v0.23.beta'


def get_time_h_mm_ss_ms(time_delta_ns):
    time_delta_ms = time_delta_ns // 1000000
    s, ms = divmod(time_delta_ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    return '{:01d}h:{:02d}m:{:02d}s:{:03d}ms'.format(h, m, s, ms)


def get_epd(infn):
    """
    Read infn file and return the epd in a list.

    :param infn: a file with analysis previously done by EPD Analyzer
    :return: a list of EPD
    """
    epds = []

    analyzed_file = Path(infn)
    if analyzed_file.is_file():
        with open(infn) as f:
            for lines in f:
                board, _ = chess.Board().from_epd(lines.strip())
                epds.append(board.epd())

    return epds


def save_output(game, board, depth, movetimems, score, pvval, engine_name,
                posid, dmval, outputpgn, outputepd, elapse_ns):
    # Save to pgn
    with open(outputpgn, 'a') as s:
        s.write(f'{game}\n\n')

    # Save to epd output
    with open(outputepd, 'a') as s:
        acsval = int(movetimems / 1000)
        idval = f'{posid}'
        pmval = pvval[0]
        anno = f'{engine_name}'
        # Acms = Analysis count: milliseconds
        acmsval = movetimems
        # Aacms = Actual analysis count: milliseconds
        Aacmsval = elapse_ns // 1000000
        hmvcval = board.halfmove_clock

        if dmval is None:
            if hmvcval > 0:
                new_epd = board.epd(acd=depth, acs=acsval, ce=score,
                                    hmvc=hmvcval, id=idval, pm=pmval,
                                    pv=pvval, Anno=anno, Acms=acmsval,
                                    Aacms=Aacmsval)
            else:
                new_epd = board.epd(acd=depth, acs=acsval, ce=score,
                                    id=idval, pm=pmval, pv=pvval, Anno=anno,
                                    Acms=acmsval, Aacms=Aacmsval)
        else:
            if hmvcval > 0:
                new_epd = board.epd(acd=depth, acs=acsval, ce=score, dm=dmval,
                                    hmvc=hmvcval, id=idval, pm=pmval,
                                    pv=pvval, Anno=anno, Acms=acmsval,
                                    Aacms=Aacmsval)
            else:
                new_epd = board.epd(acd=depth, acs=acsval, ce=score, dm=dmval,
                                    id=idval, pm=pmval, pv=pvval, Anno=anno,
                                    Acms=acmsval, Aacms=Aacmsval)

        s.write(f'{new_epd}\n')


def search_limit(extend_search, movetimems, sdepth):
    limit = None
    if extend_search:
        if sdepth == 0:
            if movetimems < 1:
                # If depth and movetime are both zero, set time to 100ms
                limit = chess.engine.Limit(time=100/1000)
            else:
                limit = chess.engine.Limit(time=4 * movetimems / 1000)
        else:
            if movetimems < 1:
                limit = chess.engine.Limit(depth=sdepth)
            else:
                limit = chess.engine.Limit(time=4 * movetimems / 1000,
                                           depth=sdepth)
    else:
        if sdepth == 0:
            if movetimems < 1:
                limit = chess.engine.Limit(time=100 / 1000)
            else:
                limit = chess.engine.Limit(time=movetimems / 1000)
        else:
            if movetimems < 1:
                limit = chess.engine.Limit(depth=sdepth)
            else:
                limit = chess.engine.Limit(time=movetimems / 1000,
                                           depth=sdepth)

    return limit


def runengine(engine_file, engineoption, enginename, epdfile, movetimems,
              outputpgn, outputepd, extend_search, sdepth):
    """
    Run engine, save search info and output game in pgn format, and epd format.
    """
    # Read existing epd output file, if position is present don't analyze it.
    existing_epds = get_epd(outputepd)

    pos_num = 0
    folder = Path(engine_file).parents[0]
    engine = chess.engine.SimpleEngine.popen_uci(engine_file, cwd=folder)

    # Set engine option
    if engineoption is not None:
        for opt in engineoption.split(','):
            optname = opt.split('=')[0].strip()
            optvalue = opt.split('=')[1].strip()
            engine.configure({optname: optvalue})

    limit = search_limit(extend_search, movetimems, sdepth)

    engine_name = engine.id['name'] if enginename is None else enginename

    # Open epd file to get epd lines, analyze, and save it.
    with open(epdfile) as f:
        for lines in f:
            epdline = lines.strip()
            logging.info(epdline)
            board, epdinfo = chess.Board().from_epd(epdline)
            epd = board.epd()
            orig_board = board.copy()
            pos_num += 1

            if epd in existing_epds:
                logging.info(f'{epd} is already analyzed.')
                continue

            # Get epd id from input epd file
            posid = None if 'id' not in epdinfo else epdinfo['id']

            pv, depth, score, dm, elapse_ns = '', None, None, None, 0
            t1 = time.perf_counter_ns()
            with engine.analysis(board, limit) as analysis:
                for info in analysis:
                    if ('upperbound' not in info
                            and 'lowerbound' not in info
                            and 'score' in info
                            and 'pv' in info
                            and 'depth' in info):
                        score = info['score'].relative.score(
                            mate_score=32000)
                        pv = info['pv']
                        depth = int(info['depth'])

                        if info['score'].is_mate() and score > 0:
                            dm = int(str(info['score']).split('#')[1])

                        # If moves in the pv is only 1, extend the search if
                        # the score is not a mate and extend_search is set.
                        if extend_search:
                            elapse_ns = time.perf_counter_ns() - t1
                            if elapse_ns >= movetimems * 1000000:
                                if info['score'].is_mate():
                                    break
                                if len(pv) > 1:
                                    break

            if not extend_search:
                elapse_ns = time.perf_counter_ns() - t1

            print(f'pos: {pos_num}\r', end='')

            # Update board for pgn output
            for m in pv:
                board.push(m)

            game = chess.pgn.Game().from_board(board)
            game.headers['Event'] = f'Position no. {pos_num}'
            game.headers['Annotator'] = engine_name
            game.headers['AnalysisMovetimeMs'] = str(movetimems)
            if posid is not None:
                game.headers['EPDId'] = posid
            game.headers['CentipawnEvaluation'] = str(score)

            save_output(game, orig_board, depth, movetimems, score, pv,
                        engine_name, posid, dm, outputpgn, outputepd,
                        elapse_ns)

    engine.quit()


def main():
    parser = argparse.ArgumentParser(
        prog='%s %s' % (APP_NAME, APP_VERSION),
        description='Analyze epd and output to pgn and epd',
        epilog='%(prog)s')
    parser.add_argument('--input', required=True, help='input epd file')
    parser.add_argument('--outputpgn', required=False,
                        help='output pgn file in append mode, default=out.pgn',
                        default='out.pgn')
    parser.add_argument('--outputepd', required=False,
                        help='output epd file in append mode, default=out.epd',
                        default='out.epd')
    parser.add_argument('--engine', required=True, help='input engine file')
    parser.add_argument('--engine-name', required=False,
                        help='input engine name')
    parser.add_argument(
        '--engine-option', required=False,
        help='input engine options, e.g '
             '--engine-option "Threads=1, Hash=128, Debug Log File=log.txt"')
    parser.add_argument('--movetimems', required=False, type=int,
                        help='input analysis time in ms, default=1000',
                        default=1000)
    parser.add_argument('--depth', required=False, type=int,
                        help='input analysis depth, default=0',
                        default=0)
    parser.add_argument('--log', action="store_true",
                        help='a flag to enable logging')
    parser.add_argument('--extend-search', action="store_true",
                        help='a flag to extend the search if move in the pv '
                             'is only 1, except if the score is already mate.')

    args = parser.parse_args()
    epd_file = args.input
    engine_file = args.engine
    outpgn_file = args.outputpgn
    outepd_file = args.outputepd
    movetimems = args.movetimems
    engineoption = args.engine_option
    enginename = args.engine_name

    if args.log:
        logging.basicConfig(level=logging.DEBUG,
                            filename='log_epdanalyzer.txt', filemode='w')

    timestart = time.perf_counter_ns()

    print('Analysis starts ...')
    runengine(engine_file, engineoption, enginename, epd_file, movetimems,
              outpgn_file, outepd_file, args.extend_search, args.depth)
    print('Analysis done!')

    elapse = time.perf_counter_ns() - timestart
    print(f'Elapse: {get_time_h_mm_ss_ms(elapse)}')


if __name__ == '__main__':
    main()
