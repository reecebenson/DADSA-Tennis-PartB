"""Pure implementation of quick sort algorithm in Python"""
def quick_sort(arr, attr = None):
    if(len(arr) <= 1): return arr
    else:
        piv = arr[0]
        gt  = [ e for e in arr[1:] if e.highest_score(attr, False) > piv.highest_score(attr, False) ]
        lt  = [ e for e in arr[1:] if e.highest_score(attr, False) <= piv.highest_score(attr, False) ]
        return quick_sort(lt, attr) + [piv] + quick_sort(gt, attr)

def attr_quick_sort(arr, sort_type = None):
    if(len(arr) <= 1): return arr
    else:
        piv = arr[0]

        # Sort Type
        if(sort_type == "score"):
            gt  = [ e for e in arr[1:] if e._total_score > piv._total_score ]
            lt  = [ e for e in arr[1:] if e._total_score <= piv._total_score ]
        elif(sort_type == "prize_money"):
            gt  = [ e for e in arr[1:] if e._total_prize_money > piv._total_prize_money ]
            lt  = [ e for e in arr[1:] if e._total_prize_money <= piv._total_prize_money ]
        elif(sort_type == "wins"):
            gt  = [ e for e in arr[1:] if e._total_wins > piv._total_wins ]
            lt  = [ e for e in arr[1:] if e._total_wins <= piv._total_wins ]
        else:
            return None

        return attr_quick_sort(lt, sort_type) + [piv] + attr_quick_sort(gt, sort_type)