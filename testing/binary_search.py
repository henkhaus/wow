

def binary_search(lst, item):
    alist = sorted(lst)
    first = 0
    last = len(alist)-1
    found = False

    while first <= last and not found:
        midpoint = (first + last)//2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1
    return found


test = [1, 4, 87, 3, 6, 84, 8, 33, 78, 653]

print (binary_search(test, 1))


