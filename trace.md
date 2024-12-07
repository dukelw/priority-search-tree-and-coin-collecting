F = [
[0, 1, 1],
[1, 1, 1],
[2, 2, 3]
]

S1:
path = []
i, j = 2, 2
path = [(2, 2)]
2 > 0 and 2 > 0
left = 2 > top = 1
move left
paths.extend(2, 1)
S2:
path = [(2, 2), (2, 1)]
2 > 0 and 1 > 0
left = 2 > top = 1
paths.extend(2, 0)
S3:
path = [(2, 2), (2, 1), (2, 0)]
2 > 0 but 0 = 0
2 > 0 (first column)
paths.extend(1, 0)
S4:
path = [(2, 2), (2, 1), (2, 0), (1, 0)]
1 > 0
paths.extend(0, 0)
S5:
path = [(2, 2), (2, 1), (2, 0), (1, 0), (0, 0)]
return path
