from math import ceil, log
from read import read
#import os
#import psutil
from memory_profiler import profile
import time

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
def print_matrix(matrix):
  for line in matrix:
    print("\t".join(map(str, line)))


def addition(X, Y):
  n = len(X)
  result = [[0 for j in range(0, n)] for i in range(0, n)]
  for i in range(0, n):
    for j in range(0, n):
      result[i][j] = X[i][j] + Y [i][j]
  return result


def substraction(X, Y):
  n = len(X)
  result = [[0 for j in range(0, n)] for i in range(0, n)]
  for i in range(0, n):
    for j in range(0, n):
      result[i][j] = X[i][j] - Y[i][j]
  return result

#@profile
def strassenMM(X, Y):
  n = len(X)

  if n <= 1:
    n = len(X)
    C = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for k in range(n):
            for j in range(n):
                C[i][j] += X[i][k] * Y[k][j]
    return C
  else:
    split_matrix = n / 2

    x11 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    x12 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    x21 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    x22 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]

    y11 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    y12 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    y21 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    y22 = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]

    result_x = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]
    result_y = [[0 for j in range(0, split_matrix)] for i in range(0, split_matrix)]

    for i in range(0, split_matrix):
      for j in range(0, split_matrix):
        x11[i][j] = X[i][j]
        x12[i][j] = X[i][j + split_matrix]
        x21[i][j] = X[i + split_matrix][j]
        x22[i][j] = X[i + split_matrix][j + split_matrix]

        y11[i][j] = Y[i][j]
        y12[i][j] = Y[i][j + split_matrix]
        y21[i][j] = Y[i + split_matrix][j]
        y22[i][j] = Y[i + split_matrix][j + split_matrix]

    #p1 to p7 calculations
    result_x = addition(x11, x22)
    result_y = addition(y11, y22)

    p1 = strassenMM(result_x, result_y)

    result_x = addition(x21, x22)
    p2 = strassenMM(result_x, y11)

    result_y = substraction(y12, y22)
    p3 = strassenMM(x11, result_y)

    result_y = substraction(y21, y11)
    p4 = strassenMM(x22, result_y)

    result_x = addition(x11, x12)
    p5 = strassenMM(result_x, y22)

    result_x = substraction(x21, x11)
    result_y = addition(y11, y12)
    p6 = strassenMM(result_x, result_y)

    result_x = substraction(x12, x22)
    result_y = addition(y21, y22)
    p7 = strassenMM(result_x, result_y)

    #calculating the cuadrants
    result12 = addition(p3, p5)
    result21 = addition(p2, p4)

    result_x = addition(p1, p4)
    result_y = addition(result_x, p7)
    result11 = substraction(result_y, p5)

    result_x = addition(p1, p3)
    result_y = addition(result_x, p6)
    result22 = substraction(result_y, p2)

    #Put the results in a matrix
    result_matrix = [[0 for j in range(0, n)] for i in range(0, n)]
    for i in range (0, split_matrix):
      for j in range (0, split_matrix):
        result_matrix[i][j] = result11[i][j]
        result_matrix[i][j + split_matrix] = result12[i][j]
        result_matrix[i + split_matrix][j] = result21[i][j]
        result_matrix[i + split_matrix][j + split_matrix] = result22[i][j]
    return result_matrix

@profile
def strassen(X, Y):

  assert type(X) == list and type(Y) == list
  assert len(X) == len(X[0]) and len(Y) == len(Y[0])
  #X = list(X)
  #Y = list(Y)

  #this makes the matrices bigger not to deal with odd matrix sizes
  matrix_pow2 = lambda n: 2 ** int(ceil(log(n, 2)))
  n = len(X)
  m = matrix_pow2(n)

  prep_x = [[0 for i in range(m)] for j in range(m)]
  #prep_x = list(prep_x)
  prep_y = [[0 for i in range(m)] for j in range(m)]
  #prep_y = list (prep_y)

  for i in range(n):
    for j in range(n):
      prep_x[i][j] = X[i][j]
      prep_y[i][j] = Y[i][j]

  prep_result_matrix = strassenMM(prep_x, prep_y)
  result_matrix = [[0 for j in range(n)] for i in range(n)]
  for i in range(n):
    for j in range(n):
      result_matrix[i][j] = prep_result_matrix[i][j]
  return result_matrix


X, Y = read('matrix80')

time_start = time.clock()

result_matrix = strassen(X, Y)

time_elapsed = (time.clock() - time_start)
print(time_elapsed)

#print_matrix(result_matrix)
#print('RAM memory % used:', psutil.virtual_memory()[2])
