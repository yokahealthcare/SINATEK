import math

def rowMax(arr):
	n = len(arr)
	lside = math.floor(n / 2)
	if sum(arr[:lside]) <  sum(arr[lside:]):
		# flip right to left
		return arr[-1::-1]


arr = [[10,20,30,40], [50,60,70,80], [90,100,110,120], [130,140,150,160]]
n = len(arr)

for y in range(n):
	for x in range(n):
		print("{}".format(arr[y][x]), end=' ')
	print()	

print()

# THE ALGORITHM
for y in range(n):
	for x in range(n):
		print(arr[y][x])
		print(arr[y][-x-1])
		print(arr[-y-1][x])
		print(arr[-y-1][-x-1])
		print()
	print("--------------cls")