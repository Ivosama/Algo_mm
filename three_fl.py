#3x3 matrix multiplication
A = [[2, 3, 8],
     [8, 8, 4],
     [8, 9, 3]]

B = [[12, 3, 5],
     [2, 4, 11],
     [1, 7, 5]]

C = [[0, 0, 0],
     [0, 0, 0],
     [0, 0, 0]]

n = len(A)
print(n)

#Go through rows of A
for i in range (n):
  #Columns of B
  for j in range(n):
    #Rows of B
    for k in range(n):
      C[i][j] += A[i][k] * B[k][j]

for r in C:
  print(r)
