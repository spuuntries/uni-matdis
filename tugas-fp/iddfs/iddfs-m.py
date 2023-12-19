import time
import re

m, n = map(int, re.split(" +", input()))
mat = [list(map(int, input().split())) for _ in range(m)]

start = tuple(map(lambda x: int(x) - 1, input("Starting coords: ").split()))
end = tuple(map(lambda x: int(x) - 1, input("End coords: ").split()))
is_end_node_right = end[1] > len(mat[0]) // 2
is_end_node_lower = end[0] > len(mat) // 2
max_depth = len(list(filter(bool, [item for sublist in mat for item in sublist])))


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

    neighbors = [
        (current[0] - 1, current[1]) if current[0] > 0 else None,
        (current[0] + 1, current[1]) if current[0] < len(matrix) - 1 else None,
        (current[0], current[1] - 1) if current[1] > 0 else None,
        (current[0], current[1] + 1) if current[1] < len(matrix[0]) - 1 else None,
    ]

    if is_end_node_right and is_end_node_lower:
        order = [1, 3, 0, 2]  # Down, Right, Up, Left
    elif is_end_node_right and not is_end_node_lower:
        order = [0, 3, 1, 2]  # Up, Right, Down, Left
    elif not is_end_node_right and is_end_node_lower:
        order = [1, 2, 0, 3]  # Down, Left, Up, Right
    elif (not is_end_node_right and not is_end_node_lower) or (
        end[0] == len(mat) // 2 and end[1] == len(mat[0]) // 2
    ):
        order = [0, 2, 1, 3]  # Up, Left, Down, Right

    neighbors = [neighbors[i] for i in order]
    neighbors = list(
        filter(
            lambda x: bool(x) and x not in visited and bool(matrix[x[0]][x[1]]),
            neighbors,
        )
    )

    for n in neighbors:
        parents[n] = current
        visited.append(n)
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
        visited.remove(n)
        continue


result = None
s_time = time.time()

for depth in range(1, max_depth):
    res = dls(mat, start, start, end, 1, depth, {}, [start])

    if not res:
        continue

    result = res
    break

e_time = time.time()
print(f"Execution took: {e_time - s_time} secs")

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
