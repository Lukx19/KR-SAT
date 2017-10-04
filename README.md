# KR-SAT

## Prerequisite
In order to build this package you need basic development tools as make, gcc, python3
This project was tested on Anaconda environment.

## Build

	1. cd pycosat
	2. make
	3. python3 setup.py install

## Run
Scrapping datasets

	python3 web-scraper.py

Base sudoku.py files provides solve method for solving sudoku. When it is run it also runs two tests on 9x9 sudoku and 36x36 to check that everything is working

	python3 sudoku.py

Running solving on sudoku datasets. Sudoku dataset need to have format sudoku,givens,min,max

	python3 sudoku3x3.py -i [input file path] -o[output file path]
	python3 sudoku3x3.py -i datasets/sudokus_with_info_3by3.txt -o datasets/sudokus_3x3_stats.csv

Running statistics. Just open a Jupyter notebooks and go to cell-> run all	

## Acknowledgments
1. We would like to thank author of repository https://github.com/ContinuumIO/pycosat for his implementation of pycosat wrapper which we used in our project
2. We would like to thank Davide Belli for his scrapping script for sudoku website.