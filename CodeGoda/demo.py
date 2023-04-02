# Enter your code here. Read input from STDIN. Print output to STDOUT

from collections import Counter

v = int(input())
text = []

numeric = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten"
]

result = []

for i in range(v):
    text.append(input())

    # program start
    ls = list(text[i])
    
    di = dict(Counter(ls))

    no_avaiable = False
    for n in numeric:
        while not no_avaiable:
            for ch in n:
                """
                if di[ch] > 0:
                    di[ch] -= 1
                else:
                    # not enough character
                    no_avaiable = True
                    break
                """
                print(ch)
            else:
                result.append(n)

        no_avaiable = False


print(result)


