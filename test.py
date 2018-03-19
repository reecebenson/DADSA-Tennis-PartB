points = [ 5, 10, 20, 50, 100 ]
diffs = [ (next_p - p) for next_p, p in zip(points, [0] + points[:]) ]
print(diffs)

"""for i in range(len(points)):
    p = points[i-1] if i > 0 else 0
    next_p = points[i]
    print(p, next_p, "=", next_p - p)

print(points)
print(diffs)"""