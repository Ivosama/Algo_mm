def read(filename):
  lines = open(filename, "r").read().splitlines()
  X = []
  Y = []

  matrix = X
  for line in lines:
    if line != "":
      matrix.append(map(int, line.split("\t")))
    else:
      matrix = Y
  return X, Y
