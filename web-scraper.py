from bs4 import BeautifulSoup
import numpy as np
import re
import requests
import os.path
import sys, getopt
from time import sleep

regex = re.compile(r'(?:<a.*?>\s*(.*?)\s*</a>)|(\w+)', re.IGNORECASE)

difficulty = 9  # number between 0 (super easy) and 9 (super hard)
N = 10000      # non-negative number of attempts to scrape one sudoku
outdir = ''
delay_time = 0.33 # seconds between each request to prevent server overload

# use this url when you want a random sudoku of size 9x9 (3x3 on this website)
url = 'http://www.menneske.no/sudoku/6/eng'

# use this url when you want a random sudoku with specified difficulty (number between 0 and 9)
#url = 'http://www.menneske.no/sudoku/eng/random.html?diff='+str(difficulty)

def main(argv):
    XWING = False
    CROSSHATCHING = False
    ALTERN_PAIRS = False
    
    global difficulty
    global outdir
    global N
    
    try:
        opts, args = getopt.getopt(argv,"hd:o:n:",["difficulty=", "outdir=", "number="])

    except getopt.GetoptError:
        print ('script.py -d <difficulty> -o <outdir> -n <number>')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print ('script.py -d <difficulty> -o <outdir> -n <number>')
            sys.exit()
        elif opt in ("-d", "--difficulty"):
            difficulty = arg
        elif opt in ("-o", "--outdir"):
            outdir = arg
        elif opt in ("-n", "--number"):
            N = int(arg)
            
    assert (int(difficulty) >=0 and int(difficulty) <= 9), "difficulty ranges between 0 and 9!"
    assert (N >= 0), "the number of sudokus must be non negative"
    
    s_list = []
    i = 0
    all_sudokus = []
    counter = 0
    previous_checkpoint = 0
    checkpoint_int = 2000 # write scraped sudokus until this checkpoint to a file
    sudoku_size = 36 # 9 for 9x9 sudokus and 36 for 36x36 sudokus
    
    while i < N:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "lxml")
        s_id=str(soup.body).split("number: ")[1]
        s_id = s_id[0:7]
        table = soup.find('div', class_='grid')
                
        if s_id in s_list:
            print(s_id," is a copy\n")
            sleep(delay_time) # to prevent server overload
        else:
            i+=1
            print("Importing Sudoku # ",i," on ",N," ----- ID: ",s_id)
            s_list.append(s_id)
            
            sudoku = np.zeros((sudoku_size, sudoku_size))
            encoding= ''
            r = 0
            
            for row in table.find_all('tr'):
                c = 0
                for col in row.find_all('td'):                    
                    if '> </td>' in str(col) or '"> </td>' in str(col):
                        x = "0"
                    else:
                        x = (str(col).split('">',1)[1]).split('</td>',1)[0]
                    #x = (str(col).split('">',1)[1][0]).replace(" ","0")
                    
                    sudoku[r][c] = int(x)
                    if x!="0":
                        encoding+= str(r+1)+str(c+1)+x+" 0\n"
                        
                        for d in range(1,10):
                            if str(d) != x:
                                encoding += '-'+str(r+1)+str(c+1)+str(d)+" 0\n"
                        
                    c+=1
                r+=1
            
            
            tmp = str(soup.body).split("Solution methods:  ")        
            tech = []
            if len(tmp) > 1:
                tmp =regex.findall(tmp[1].split("<br/>")[0])
                for t in tmp:
                    if t[0] == '':
                        tech.append(t[1])
                    else:
                        tech.append(t[0])
                        
            print("Count:", str(counter), "/", str(N))
            
            # transform sudoku into list of numbers
            sudoku_list = []
            for r in range(sudoku_size):
                for c in range(sudoku_size):
                    sudoku_list.append(int(sudoku[r][c]))
            
            # add current sudoku to list of sudokus (don't allow duplicates)
            if sudoku_list not in all_sudokus:
                all_sudokus.append(sudoku_list)
                counter += 1
                            
            # every X iterations, write the current sudokus to a file
            if counter % checkpoint_int == 0:
                with open(os.path.join(outdir, "all_sudokus_"+str(counter)+".txt"), "w") as myfile:
                    for sudoku in all_sudokus[previous_checkpoint:]:
                        for number in sudoku:
                            myfile.write(str(number)+" ")
                        myfile.write("\n")
                    myfile.close()
                previous_checkpoint = counter
                sleep(delay_time) # to prevent server overload
                    
            sleep(delay_time) # to prevent server overload
                        
    print('Done scraping')
    print('Start writing to file...')

    # write all sudokus to a file        
    with open(os.path.join(outdir, "all_sudokus.txt"), "w") as myfile:
        for sudoku in all_sudokus:
            for number in sudoku:
                myfile.write(str(number)+" ")
            myfile.write("\n")
        myfile.close()
        
    print('Finished!')


if __name__ == "__main__":
   main(sys.argv[1:])