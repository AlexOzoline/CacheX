# CacheX
Overview
Cachex is a perfect-information two-player game played on an n × n rhombic, hexagonally tiled
board, based on the strategy game Hex. Two players (named Red and Blue) compete, with the
goal to form a connection between the opposing sides of the board corresponding to their respective
color.
![Local Image](CacheX.png)
To play a game using referee, invoke it as follows. The referee module (the directory referee/) and
the modules with your Player class(es) should be within your current directory:
python -m referee <n> <red module> <blue module>
Upon calling this the game will be played out by the two AI agents.
For example:
python -m referee 5 random_group_18 random_agent
