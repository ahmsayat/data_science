import math, queue

def min_max_heap():
    q = queue.PriorityQueue()

    for x in range(5):
        q.put( (-x, x) )

    while q.empty() is False:
        x = q.get()
        print(x[1])

def custom_sorting():
    import functools
    arr = range(10)
    
    def cmp(a,b):
        return (a > b) - (a < b)
        
    def comparator(a,b):
        return cmp(a,b)
    
    nsarr = sorted(arr, key = functools.cmp_to_key( comparator ) )
    print(nsarr)

custom_sorting()