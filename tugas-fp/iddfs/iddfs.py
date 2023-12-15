import re

m, n = map(int, re.split(" +", input()))
mat = [list(map(int, input().split())) for _ in range(m)]

start = tuple(map(lambda x: int(x) - 1, input("Starting coords: ").split()))
end = tuple(map(lambda x: int(x) - 1, input("End coords: ").split()))


def reconstruct(start, end, parents, res=None):
    if res is None:
        res = [start]
    if start == end:
        return res
    res.append(parents[start])
    return reconstruct(parents[start], end, parents, res)


def dls(matrix, current, start, finish, depth, limit, parents, visited):
    if depth == limit and current != finish:
        return False

    if current == finish:
        return reconstruct(current, start, parents)

    visited.append(current)

    neighbors = list(
        filter(
            lambda x: bool(x) and x not in visited and bool(matrix[x[0]][x[1]]),
            [
                (current[0] - 1, current[1]) if current[0] > 0 else None,
                (current[0] + 1, current[1]) if current[0] < len(matrix) - 1 else None,
                (current[0], current[1] - 1) if current[1] > 0 else None,
                (current[0], current[1] + 1)
                if current[1] < len(matrix[0]) - 1
                else None,
            ],
        )
    )

    for n in neighbors:
        parents[n] = current
        path = dls(
            matrix,
            n,
            start,
            finish,
            depth + 1,
            limit,
            parents,
            visited,
        )
        if path:
            return path
        continue


result = None

for depth in range(1, len(mat) * len(mat[0])):
    res = dls(mat, start, start, end, 1, depth, {}, [])

    if not res:
        continue

    result = res
    break

if not result:
    print("No path was found :<")
else:
    # print(result)
    for i, r in enumerate(mat):
        for j, e in enumerate(r):
            if (i, j) in result:
                if (i, j) != result[0]:
                    print("*", end=" ")
                else:
                    print("$", end=" ")
            else:
                print(e, end=" ")
            if j == len(r) - 1:
                print()
