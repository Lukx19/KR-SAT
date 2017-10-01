
import numpy as np
import math

import sudoku
import argparse
import copy

parser = argparse.ArgumentParser(description='Solves sudokus and return SAT statistics.')
parser.add_argument('-o', action="store", dest="out_file", default='sudoku_stats.csv',
                    help='output file with sudoku and additional statistics')
parser.add_argument('-i', dest='in_file', action='store', default='sudoku.csv',
                    help='input file in format sudoku, givens,min, max')

args = parser.parse_args()
count =0
f_out = open(args.out_file,'w')
f_out.write(','.join(['sudoku','givens','min','max','visits','propagations',
    'conflicts','avg_level','seconds','assignments','restarts'])+"\n")
base_clauses = sudoku.extended_encoding_clauses(size_block = 3)
with open(args.in_file) as f:
    for line in f:
        if count % 1000 == 0:
            print(count, ' processed')
        count=count+1
        clauses = copy.deepcopy(base_clauses)
        parts = line.split(",")
        parts[-1] = parts[-1][:-1]
        length = len(parts[0])
        data = [0 for i in range(length)]
        i =0
        for num in parts[0]:
            data[i] = int(num)
            i= i+1    
        sol = sudoku.solve(sudoku=data,clauses = clauses, size_block = 3)
        if not sol['solved']:
            print("sudoku not solved: ",count)
            continue
        f_out.write(','.join([parts[0],parts[1],parts[2],parts[3],
            str(sol['visits']),str(sol['propagations']),str(sol['conflicts']),
            str(sol['avg_level']),str(sol['seconds']),str(sol['assignments']),str(sol['restarts'])])+"\n")
        f_out.flush()

f_out.close()
   