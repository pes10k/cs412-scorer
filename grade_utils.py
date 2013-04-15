import os

cols = ('1a', '1b', '1c', '1d', '2a', '2b', '3a')

grades = [[float(n) for n in l.split()[1:]] for l in open(os.path.join("data/grades.txt")).readlines()[::-1][:-5]]
    

