# Maze-Runner
Autonomous Maze Navigation Robot Using a Raspberry pi.

##Assumptions:
- The maze has no isolated blocks
- There exists only one solution to the maze, one entrance and one exit.
- All junctions and corners are at a 90 degree angle.
- Raspberry pi pin mode: BCM
- The maze is color coded (This is not a necessary assumption as the algorithm can work without the color code)

##Components used:
- Ultrasonic sensors (for obstacle detection)
- Color Sensor, TCS3200, (for color detection)


##NOTE: 
- The file, mazerunner.py, was successful during simulation but had errors when synchronising with the real life robot in the code.
- The two python files, tourney.py and mazerunner.py, are to be integrated to work together.
- This is not a necessary assumption as the algorithm can work without the color code
