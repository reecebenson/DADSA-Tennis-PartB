import cProfile
import random
import datetime

# Pure implementation of quick sort algorithm in Python
def quick_sort_score(arr,d):
    print("QUICKSORT [{}] - START".format(d))

    cp = cProfile.Profile()
    cp.enable()
    result = quick_sort_score_actual(arr)
    cp.disable()
    cp.print_stats()

    print("QUICKSORT [{}] - END\n\n".format(d))
    return result

def quick_sort_score_actual(arr):
    if(len(arr) <= 1): return arr
    else:
        piv = arr[0]
        gt  = [ e for e in arr[1:] if e > piv ]
        lt  = [ e for e in arr[1:] if e <= piv ]
        return quick_sort_score_actual(lt) + [piv] + quick_sort_score_actual(gt)

def tim_sort(arr,d):
    print("TIMSORT [{}] - START\n\n".format(d))

    cp = cProfile.Profile()
    cp.enable()
    result = sorted(arr)
    cp.disable()
    cp.print_stats()

    print("TIMOSRT [{}] - END\n\n".format(d))
    return result

data_100t = []
for i in range(1, 100000):
    data_100t.append(random.randint(1, 10000000))

data_250t = []
for i in range(1, 250000):
    data_250t.append(random.randint(1, 10000000))

data_500t = []
for i in range(1, 500000):
    data_500t.append(random.randint(1, 10000000))

data_1m = []
for i in range(1, 1000000):
    data_1m.append(random.randint(1, 10000000))

data_5m = []
for i in range(1, 5000000):
    data_5m.append(random.randint(1, 10000000))
    
data_10m = []
for i in range(1, 10000000):
    data_10m.append(random.randint(1, 10000000))

quick_sort_score(data_100t,"100t")
tim_sort(data_100t,"100t")

quick_sort_score(data_250t,"250t")
tim_sort(data_250t,"250t")

quick_sort_score(data_500t,"500t")
tim_sort(data_500t,"500t")

quick_sort_score(data_1m,"1m")
tim_sort(data_1m,"1m")

quick_sort_score(data_5m,"5m")
tim_sort(data_5m,"5m")

quick_sort_score(data_10m,"10m")
tim_sort(data_10m,"10m")