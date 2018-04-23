# Gerrymandering Simulator

A simulator for detecting potential bias in an MxN districting grid

## Usage

The simulator takes a JSON file as input detailing the districting, see `example3x3.json` for an example 3x3 districting.

For generating 10 5-step simulations on the 3x3 grid defined in `example3x3.json`, the command would be the following:

```
$ python simulation.py --rows 3 --cols 3 --steps 5 --num-simulations 10 --file example3x3.json
```

The simulation gave the following districtings:

```
Original Districting
---------------

D,a      D,a      R,b
R,a      D,b      R,b
R,c      R,c      R,c

Resulting Districting
---------------

D,a      D,a      R,b
R,c      D,b      R,b
R,c      R,c      R,b

Resulting Districting
---------------

D,a      D,a      R,b
R,a      D,b      R,b
R,c      R,c      R,c

Resulting Districting
---------------

D,a      D,a      R,b
R,a      D,b      R,b
R,c      R,c      R,c

Resulting Districting
---------------

D,a      D,a      R,b
R,a      D,c      R,b
R,c      R,c      R,b

Resulting Districting
---------------

D,a      D,a      R,b
R,a      D,c      R,b
R,a      R,c      R,b

Resulting Districting
---------------

D,a      D,c      R,b
R,a      D,c      R,b
R,a      R,a      R,a

Resulting Districting
---------------

D,a      D,c      R,b
R,a      D,c      R,b
R,a      R,a      R,a

Resulting Districting
---------------

D,a      D,c      R,b
R,a      D,c      R,b
R,a      R,a      R,a

Resulting Districting
---------------

D,a      D,c      R,b
R,a      D,c      R,b
R,a      R,a      R,a

Resulting Districting
---------------

D,c      D,c      R,b
R,a      D,c      R,b
R,a      R,a      R,b
```

Note that all of the districtings are simply connected and contiguous, adhering to the rules specificied for districtings of a state.

The command line args can be viewed with the `-h` flag:

```
$ python simulation.py --help
usage: simulation.py [-h] -r ROWS -c COLS -s STEPS -n NUM_SIMULATIONS -f FILE

Run the gerrymandering simulator on an nxn grid

optional arguments:
  -h, --help            show this help message and exit
  -r ROWS, --rows ROWS  Number of rows in the grid
  -c COLS, --cols COLS  Number of columns in the grid
  -s STEPS, --steps STEPS
                        Number of steps to take for the random walk
  -n NUM_SIMULATIONS, --num-simulations NUM_SIMULATIONS
                        Number of simulations to run
  -f FILE, --file FILE  JSON file representing the grid to simulate on
```
