def printSomething():
  a = "before yield!"
  yield a
  
  b = "after yield"
  yield b

for i, v in enumerate(printSomething()):
  # this is creating generator
  print("#{} : {}".format(i, v))
 