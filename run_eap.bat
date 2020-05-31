set MTMS=1000
set EPD=./epd/wacnew.epd


:: Stockfish
eap.exe --input %EPD% --movetimems %MTMS% --engine ./engine/stockfish-11-win/stockfish_20011801_x64_modern.exe --engineoption "Hash=128" --outputpgn sf_wacnew_result.pgn --outputepd sf_wacnew_result.epd

pause
