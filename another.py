from math import log10
from read import read
#import os
#import psutil
from memory_profiler import profile
import time
from try3_strassen import print_matrix

'''
# inner psutil function
def process_memory():
  process = psutil.Process(os.getpid())
  mem_info = process.memory_info()
  return mem_info.rss


# decorator function
def profile(func):
  def wrapper(*args, **kwargs):
    mem_before = process_memory()
    result = func(*args, **kwargs)
    mem_after = process_memory()
    print("{}:consumed memory: {:,}".format(
      func.__name__,
      mem_before, mem_after, mem_after - mem_before))

    return result

  return wrapper
'''

@profile

def matrix_multiply(X, Y):
  n = len(X)
  maxi = 0 #max iterations

  for i in range(n):
    for j in range(n):
      if maxi < X[i][j]: maxi = X[i][j]
      if maxi < Y[i][j]: maxi = Y[i][j]

  M = int(log10(maxi))+1
  P = int(log10((10 ** (2 * M) -1) * n))+1

  C, D, result_matrix = [], [], [[0 for i in range(n)] for j in range(n)]

  for i in range(n):
    sum_1 = 0
    for j in range(n):
      sum_1 = sum_1 * (10 ** P) + X[i][j]
    C.append(sum_1)
  for j in range(n):
    sum_1 = 0
    for i in range(n):
      sum_1 = sum_1 * (10 ** P) + Y[n-1-i][j]
    D.append(sum_1)
  for i in range(n):
    for j in range(n):
      result_matrix[i][j] = int(C[i] * D[j] / (10 ** (P * (n-1)))) % (10 ** P)
  return result_matrix

A, B = read('matrix40')

time_start = time.clock()

matrix_multiply(A, B)

time_elapsed = (time.clock() - time_start)
print(time_elapsed)


#print('RAM memory % used:', psutil.virtual_memory()[2])
