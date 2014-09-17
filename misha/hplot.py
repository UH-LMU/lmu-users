import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

f = open("slices.csv")
lines = f.readlines()
f.close()

n = len(lines)

r = [None]*n
z = [None]*n
intensity = [None]*n

i = 0
for l in lines:
    print i
    l = l.rstrip()
    r[i], z[i], intensity[i] = l.split(",")
    i = i + 1

print r


