set MTMS=1000
set EPD="./epd/wacnew.epd"


:: Enable logging
eap.exe --log --input %EPD% --movetimems %MTMS% --engine "./engine/stockfish-11-win/stockfish_20011801_x64_modern.exe" --engineoption "Hash=128" --outputpgn sf_wacnew_result.pgn --outputepd sf_wacnew_result.epd


:: Stockfish uses ending tablebase syzygy
:: Add SyzygyPath=D:/Chess/syzygy in engineoption
:: eap.exe --log --input %EPD% --movetimems %MTMS% --engine "D:/Chess/Engines/Stockfish/stockfish_11.exe" --engineoption "Hash=128, SyzygyPath=D:/Chess/syzygy" --outputpgn sf_wacnew_result.pgn --outputepd sf_wacnew_result.epd


:: Stockfish
:: eap.exe --input %EPD% --movetimems %MTMS% --engine "./engine/stockfish-11-win/stockfish_20011801_x64_modern.exe" --engineoption "Hash=128" --outputpgn sf_wacnew_result.pgn --outputepd sf_wacnew_result.epd

pause
