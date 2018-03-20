"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
def quick_sort_score(arr, attr="score"):
    if(len(arr) <= 1): return arr
    else:
        piv = arr[0]
        gt  = [ e for e in arr[1:] if e[attr] > piv[attr] ]
        lt  = [ e for e in arr[1:] if e[attr] <= piv[attr] ]
        return quick_sort_score(lt) + [piv] + quick_sort_score(gt)
