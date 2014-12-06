def swap(seq, a, b):
    tmp = seq[a]
    seq[a] = seq[b]
    seq[b] = tmp

def b_up_merge(A, ileft, iright, iend, B):
    il = ileft
    ir = iright
    for j in range(ileft, iend):
        if il < iright and (ir >= iend or A[il] <= A[ir]):
            B[j] = A[il]
            il += 1
        else:
            B[j] = A[ir]
            ir += 1

def partition(A, l, r):
    p = r - 1 # we choose pivot to be right
    pv = A[p]
    s = l
    for i in range(l, p):
        if A[i] < pv:
            swap(A, s, i)
            s += 1
    swap(A, s, p)
    return s

def quick_sort(A, i, k):
    if i < k:
        p = partition(A, i, k)
        quick_sort(A, i, p )
        quick_sort(A, p + 1, k)


class Sorters(object):
    ALGORITHMS = ('dummy', 'bubble', 'bubble_optimized', 'insertion', 'merge',
                  'quick')
    @staticmethod
    def dummy(to_sort, n):
        return sorted(to_sort)

    @staticmethod
    def bubble(to_sort, n):
        while True:
            swapped = False
            for i in range(n-1):
                if to_sort[i] > to_sort[i+1]:
                    swap(to_sort, i, i+1)
                    swapped = True
            if not swapped:
                break
        return to_sort

    @staticmethod
    def bubble_optimized(to_sort, n):
        while True:
            newn = 0
            for i in range(n-1):
                if to_sort[i] > to_sort[i+1]:
                    swap(to_sort, i, i+1)
                    newn = i+1
            n = newn
            if n == 0:
                break
        return to_sort

    @staticmethod
    def insertion(to_sort, n):
        for i in range(1,n):
            j = i
            while j > 0 and to_sort[j] < to_sort[j-1]:
                swap(to_sort, j, j-1)
                j -= 1
        return to_sort

    @staticmethod
    def merge(to_sort, n):
        buff = to_sort[:]
        width = 1
        while width < n:
            i = 0
            while i < n:
                b_up_merge(to_sort, i, min(i+width, n), min(i+2*width, n),
                             buff) 

                i += 2 * width
            to_sort = buff[:]
            width *= 2
        return to_sort

    @staticmethod
    def quick(to_sort, n):
        quick_sort(to_sort, 0, n)
        return to_sort
