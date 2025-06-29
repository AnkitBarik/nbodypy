# nbodypy
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<p align="center" width="100%">
<img src="https://raw.githubusercontent.com/AnkitBarik/nbodypy/refs/heads/main/images/trajectories.png" width="500">
</p>

Python codes for N-body simulations. Uses the leapfrog scheme.

## Prerequisites
The code is fairly barebones and the only requisites are [`NumPy`](https://numpy.org/) and [`Matplotlib`](https://matplotlib.org/).

## Scripts
There are two codes that can be run: 
 - `main_serial.py` : Even though it is "serial" in nature, the code is heavily vectorized using `Numpy` and is thus quite fast. 
 - `main_parallel.py`: This is parallelized using `mpi4py` and is object oriented. However, this is still somewhat **experimental** and is in fact a bit slower. I am currently trying to see if there is a better way to parallelize and vectorize it.

#### Acknowledgements

Data for the solar system objects has been taken from https://hanno-rein.de/teaching/PSCB57_notes_lecture10.pdf which in turn has been taken from the [NASA Horizons system](https://ssd.jpl.nasa.gov/horizons/app.html#/) .
I received no funding for this. :D
