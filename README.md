# EPD-Analyzer
Read epd file, analyze positions and save it to pgn and epd files.

### A. Guide
##### 1. Use python source code
* Install python 3.8 and above
* Install requirements.txt

##### 2. Use eap.exe
* Download the eap.exe file in release link

### B. Command line
* See sample batch file run_eap.bat
* Sample command line using default options  
`python eap.py --input d:/chess/epd/wac.epd --engine D:/chess/engine/stockfish-11/sf11.exe --engineoption "Hash=128, Threads=2" --movetimems 1000`  
or  
`eap.exe --input d:/chess/epd/wac.epd --engine D:/chess/engine/stockfish-11/sf11.exe --engineoption "Hash=128, Threads=2" --movetimems 1000`
* Use enginename option  
`eap.exe --input d:/chess/epd/wac.epd --enginename "Stockfish 11" --engine D:/chess/engine/stockfish-11/sf11.exe --engineoption "Hash=128, Threads=2" --movetimems 1000`
* Output pgn output to sfpgnoutput.pgn  
`eap.exe --input d:/chess/epd/wac.epd --enginename "Stockfish 11" --engine D:/chess/engine/stockfish-11/sf11.exe --engineoption "Hash=128, Threads=2" --movetimems 1000 --outputpgn sfpgnoutput.pgn`
* Use a fixed depth to analyze the EPD.  
`... --depth 14 --movetimems 0`
* Combine depth and time  
`--depth 14 --movetimems 1000`  
Engine will stop whichever is reached first.

### C. Sample output
##### 1. PGN
```
[Event "?"]
[Site "?"]
[Date "????.??.??"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "1-0"]
[AnalysisMovetimeMs "1000"]
[Annotator "Stockfish 11 64 POPCNT"]
[CentipawnEvaluation "31998"]
[EPDId "WAC.001"]
[FEN "2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - - 0 1"]
[SetUp "1"]

1. Qg6 Nxe5 2. Qh7# 1-0
```

##### 2. EPD
`2rr3k/pp3pp1/1nnqbN1p/3pN3/2pP4/2P3Q1/PPB4P/R4RK1 w - - acd 245; acs 1; ce 31998; id "WAC.001"; pm Qg6; pv Qg6 Nxe5 Qh7#; c0 "analyzed by Stockfish 11 64 POPCNT";`


### D. Help
```
(venv) D:\github\EPD-Analyzer>python eap.py -h
usage: EAP - EPD Analysis to PGN v0.23.beta [-h] --input INPUT [--outputpgn OUTPUTPGN] [--outputepd OUTPUTEPD] --engine ENGINE [--engine-name ENGINE_NAME]
                                            [--engine-option ENGINE_OPTION] [--movetimems MOVETIMEMS] [--depth DEPTH] [--log] [--extend-search]

Analyze epd and output to pgn and epd

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         input epd file
  --outputpgn OUTPUTPGN
                        output pgn file in append mode, default=out.pgn
  --outputepd OUTPUTEPD
                        output epd file in append mode, default=out.epd
  --engine ENGINE       input engine file
  --engine-name ENGINE_NAME
                        input engine name
  --engine-option ENGINE_OPTION
                        input engine options, e.g --engine-option "Threads=1, Hash=128, Debug Log File=log.txt"
  --movetimems MOVETIMEMS
                        input analysis time in ms, default=1000
  --depth DEPTH         input analysis depth, default=0
  --log                 a flag to enable logging
  --extend-search       a flag to extend the search if move in the pv is only 1, except if the score is already mate.

EAP - EPD Analysis to PGN v0.23.beta
```

### E. Credits
* Python-chess  
https://github.com/niklasf/python-chess
