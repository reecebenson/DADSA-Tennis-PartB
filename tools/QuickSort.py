"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
def quick_sort_score(arr):
    if(len(arr) <= 1): return arr
    else:
        piv = arr[0]
        gt  = [ e for e in arr[1:] if e['score'] > piv['score'] ]
        lt  = [ e for e in arr[1:] if e['score'] <= piv['score'] ]
        return quick_sort_score(lt) + [piv] + quick_sort_score(gt)
