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
APP_VERSION = 'v0.7.beta'


def get_time_h_mm_ss_ms(time_delta_ns):
    time_delta_ms = time_delta_ns // 1000000
    s, ms = divmod(time_delta_ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)

    return '{:01d}h:{:02d}m:{:02d}s:{:03d}ms'.format(h, m, s, ms)


def runengine(engine_file, engineoption, enginename, epdfile, movetimems,
              outputpgn, outputepd):
    """
    Run engine, save search info and output game in pgn format, and epd format.
    """
    num_pos = 0
    folder = Path(engine_file).parents[0]
    engine = chess.engine.SimpleEngine.popen_uci(engine_file, cwd=folder)

    # Set engine option
    if engineoption is not None:
        for opt in engineoption.split(','):
            optname = opt.split('=')[0].strip()
            optvalue = opt.split('=')[1].strip()
            engine.configure({optname: optvalue})

    limit = chess.engine.Limit(time=movetimems/1000)
    engine_name = engine.id['name'] if enginename is None else enginename

    # Open epd file to get epd lines, analyze, and save it.
    with open(epdfile) as f:
        for lines in f:
            epdline = lines.strip()
            logging.info(epdline)
            board, epdinfo = chess.Board().from_epd(epdline)
            orig_board = board.copy()

            # Get epd id
            posid = None
            try:
                posid = epdinfo['id']
            except KeyError:
                pass
            except Exception:
                print('Unexpected exception:')
                raise

            pv, depth, score = '', None, None
            with engine.analysis(board, limit) as analysis:
                for info in analysis:
                    if 'score' in info:
                        score = info['score'].relative.score(mate_score=32000)
                    if 'depth' in info:
                        depth = int(info['depth'])
                    if ('pv' in info and 'upperbound' not in info and
                            'lowerbound' not in info):
                        pv = info['pv']

            num_pos += 1
            print(f'pos: {num_pos}\r', end='')

            nboard, sanpv, pm = board.copy(), [], None
            for i, m in enumerate(pv):
                sanpv.append(nboard.san(m))
                if i == 0:
                    pm = nboard.san(m)
                nboard.push(m)

            for m in pv:
                board.push(m)

            game = chess.pgn.Game().from_board(board)
            game.headers['Annotator'] = engine_name
            game.headers['AnalysisMovetimeMs'] = str(movetimems)
            if posid is not None:
                game.headers['EPDId'] = posid
            game.headers['CentipawnEvaluation'] = str(score)

            # Save to pgn output
            with open(outputpgn, 'a') as s:
                s.write(f'{game}\n\n')

            # Save to epd output
            with open(outputepd, 'a') as s:
                acs = int(movetimems / 1000)
                save_epd = orig_board.epd()
                if posid is None:
                    s.write(f'{save_epd} acd {depth}; acs {acs}; '
                            f'ce {score}; pm {pm}; pv {" ".join(sanpv)}; '
                            f'c0 "analyzed by {engine_name}";\n')
                else:
                    s.write(f'{save_epd} acd {depth}; acs {acs}; '
                            f'ce {score}; id "{posid}"; pm {pm}; '
                            f'pv {" ".join(sanpv)}; c0 "analyzed by {engine_name}";\n')

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
    parser.add_argument('--enginename', required=False,
                        help='input engine name')
    parser.add_argument(
        '--engineoption', required=False,
        help='input engine options, e.g '
             '--engineoption "Threads=1, Hash=128, Debug Log File=log.txt"')
    parser.add_argument('--movetimems', required=False, type=int,
                        help='input analysis time in ms, default=1000',
                        default=1000)
    parser.add_argument('--log', action="store_true",
                        help='a flag to enable logging')

    args = parser.parse_args()
    epd_file = args.input
    engine_file = args.engine
    outpgn_file = args.outputpgn
    outepd_file = args.outputepd
    movetimems = args.movetimems
    engineoption = args.engineoption
    enginename = args.enginename

    if args.log:
        logging.basicConfig(level=logging.DEBUG,
                            filename='log_epdanalyzer.txt', filemode='w')

    timestart = time.perf_counter_ns()

    print('Analysis starts ...')
    runengine(engine_file, engineoption, enginename, epd_file, movetimems,
              outpgn_file, outepd_file)
    print('Analysis done!')

    elapse = time.perf_counter_ns() - timestart
    print(f'Elapse: {get_time_h_mm_ss_ms(elapse)}')


if __name__ == '__main__':
    main()
