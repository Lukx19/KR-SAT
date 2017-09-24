
import numpy as np
import math

import sudoku


sudoku_data = []
with open("test_input.txt") as f:
    for line in f:
            parts = line.split(";")
#             parts[1] = parts[1][:-1]
            length = len(parts[0])
            data = [0 for i in range(length)]
            i =0
            for num in parts[0]:
                data[i] = int(num)
                i= i+1    
            sudoku_data.append({'input': data, 'desc': parts[2]})

for sud in sudoku_data:
    sol = sudoku.solve(sud['input'])
    print(sud['desc'],'visits:',sol['visits'],'propagations:',sol['propagations'],'decisions:',sol['decisions'])