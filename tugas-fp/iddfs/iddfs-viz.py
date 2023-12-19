from asciimatics.screen import Screen
from time import sleep
import time
import re

refresh_speed = 0.1
m, n = map(int, re.split(" +", input()))
mat = [list(map(int, input().split())) for _ in range(m)]

start = tuple(map(lambda x: int(x) - 1, input("Starting coords: ").split()))
end = tuple(map(lambda x: int(x) - 1, input("End coords: ").split()))
max_depth = len(list(filter(bool, [item for sublist in mat for item in sublist])))

screen = Screen.open()


def visualize(screen: Screen, mat, path):
    for i, row in enumerate(mat):
        for j, cell in enumerate(row):
            if (i, j) in path:
                screen.print_at("*", j, i)
            elif cell == 1:
                screen.print_at(".", j, i)
            else:
                screen.print_at("X", j, i)
    screen.refresh()
    sleep(refresh_speed)


def reconstruct(start, end, parents, res=None):
    if res is None:
        res = [start]
    if start == end:
        return res
    res.append(parents[start])
    return reconstruct(parents[start], end, parents, res)


def dls(matrix, current, start, finish, depth, limit, parents, visited):
    visualize(screen, matrix, reconstruct(current, start, parents))

    if depth == limit and current != finish:
        return False

    if current == finish:
        recons = reconstruct(current, start, parents)
        visualize(screen, matrix, recons)
        return recons

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


visualize(screen, mat, [])

result = None
s_time = time.time()

for depth in range(1, max_depth):
    res = dls(mat, start, start, end, 1, depth, {}, [start])

    if not res:
        continue

    result = res
    break

e_time = time.time()
screen.close()

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
