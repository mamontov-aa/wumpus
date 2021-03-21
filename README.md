# WumpusHunter
simple python-3 console game app

## How to run:
### Pre-requisites:
- Internet connection (access to GitHub)
- Git client
- Python3
- 100Kb free space
### What to do:
- > git clone git@github.com:mamontov-aa/wumpus.git
(Linux)
- > python3 -m venv .venv
- > .venv/bin/pip install -r requirements.txt
- > .venv/bin/python3 wumpus.py
(Windows)
- > python -m venv .venv
- > .venv\scripts\pip.exe install -r requirements.txt
- > .venv\scripts\python.exe wumpus.py


## Gameplay:
- GameWorld is a labirynth (non-directed graph)
- Player can move himself in labirynth and shoot arrows ahead
- Wumpus is a monster to be found and killed
- Wumpus can eat player
- There are also bats (carry player to random place) and gulfs (player dyes inside)
### Controls:
- Console commands [cmd_name arg1 arg2 ...]
- Type [help] to see the actual list


## Side conditions:
- When player comes into hall where Wumpus is, Wumpus eats player regardless there can also be bats or gulf in this hall
- When player is shooting, this shot wakes Wumpus only after shot ends
- When round ends (no matter the player winned or losed) th world resets and the game restarts
- No checks for map consistency and coherency
- Wumpus and bats CAN locate in cave-romms with gulfs
- Bats cannot put the player to their own place

## Future ideas
- Add OS-like commands input with TAB
- Add ability to pick up arrow perviously shot and missed (think about gameplay)
- Add game file-save an file-load options
- Add world file-load option