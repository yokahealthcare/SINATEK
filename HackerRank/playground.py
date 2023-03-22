def findZigZagSequence(a, n):
    a.sort()
    print("a - sorted : {}".format(a))

    mid = int((n + 1)/2)
    print("mid : {}".format(mid))
    
    a[mid], a[n-1] = a[n-1], a[mid]
    print("a - swapped : {}".format(a))

    st = mid + 1
    ed = n - 1
    print("st : {}".format(st))
    print("ed : {}".format(ed))
    while(st <= ed):
        a[st], a[ed] = a[ed], a[st]
        st = st + 1
        ed = ed + 1
    
    for i in range (n):
        if i == n-1:
            print(a[i])
        else:
            print(a[i], end = ' ')
    return

a = [1,2,3,4,5,6,7]
n = len(a)

findZigZagSequence(a, n)

