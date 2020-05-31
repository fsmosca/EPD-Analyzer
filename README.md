# EPD-Analyzer
Read epd file, analyze positions and save it to pgn and epd files.

### Guide
##### A. Use python source code
* Install python 3.8 and above
* Install requirements.txt

##### B. Use eap.exe
* Download the eap.exe file in release link

### Command line
* See sample batch file run_eap.bat
* Sample command line  
`python eap.py --input d:/chess/epd/wac.epd --engine D:/chess/engine/stockfish-11/sf11.exe --engineoption "Hash=128, Threads=2" --movetimems 1000`  
or  
`eap.exe --input d:/chess/epd/wac.epd --engine D:/chess/engine/stockfish-11/sf11.exe --engineoption "Hash=128, Threads=2" --movetimems 1000`


### Help
```
usage: EAP - EPD Analysis to PGN v0.1.beta [-h] --input INPUT [--outputpgn OUTPUTPGN] [--outputepd OUTPUTEPD] --engine
                                           ENGINE [--engineoption ENGINEOPTION] --movetimems MOVETIMEMS

Analyze epd and output to pgn and epd

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         input epd file
  --outputpgn OUTPUTPGN
                        output pgn file in append mode, default=out.pgn
  --outputepd OUTPUTEPD
                        output epd file in append mode, default=out.epd
  --engine ENGINE       input engine file
  --engineoption ENGINEOPTION
                        input engine options, e.g --engineoption "Threads=1, Hash=128, Debug Log File=log.txt"
  --movetimems MOVETIMEMS
                        input analysis time in ms, default=1000

EAP - EPD Analysis to PGN v0.1.beta
```

### Credits
* Python-chess  
https://github.com/niklasf/python-chess
