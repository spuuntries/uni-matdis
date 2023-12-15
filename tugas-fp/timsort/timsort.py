import os
import string

debug = int(os.environ.get("DEBUG") if os.environ.get("DEBUG") else 1)
# 2 for full debug, 1 for semi-debug, 0 for none
timsort_mode = 0
# For brute. 1 = No runs optimization, anything else is with all optimizations.
steps = 0
charset = string.printable

if __name__ == "__main__":
    print(
        """
    Algorithms:
          1: Timsort
          2: Merge Sort
          3: Insertion Sort
          4: Timsort (Old) - Deprecated, initial implementation, for runs proof.
    """
    )
    algo = int(input("Choose which algorithm to use: "))

    print("Testing? (i.e., use random strings if yes)")
    testing = ["n", "y"].index(input("Testing [y/n]: ")[0].lower())
    if not testing:
        n = int(input())
        inputs = [input() for _ in range(n)]
    else:
        # fmt: off
        # testing
        import random
        def random_string(n):
            return "".join(
                random.choice(string.ascii_letters) for _ in range(random.randint(n // 2, n))
            )
        inputs = [random_string(100) for _ in range(300)]
        # fmt: on
    inputs = list(map(lambda x: x.lower(), inputs))


def mergesort(lst):
    global steps
    steps += 1

    def merge(left_list, right_list):
        global steps
        steps += 1
        sorted_list = []
        left_list_index = right_list_index = 0

        # Merge smaller elements first
        while left_list_index < len(left_list) and right_list_index < len(right_list):
            steps += 1
            if left_list[left_list_index] <= right_list[right_list_index]:
                sorted_list.append(left_list[left_list_index])
                left_list_index += 1
            else:
                sorted_list.append(right_list[right_list_index])
                right_list_index += 1

        # If left list has more items, append them to sorted_list
        while left_list_index < len(left_list):
            steps += 1
            sorted_list.append(left_list[left_list_index])
            left_list_index += 1

        # If right list has more items, append them to sorted_list
        while right_list_index < len(right_list):
            steps += 1
            sorted_list.append(right_list[right_list_index])
            right_list_index += 1

        return sorted_list

    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left_list = mergesort(lst[:mid])
    right_list = mergesort(lst[mid:])

    return merge(left_list, right_list)


def insertionsort(arr):
    global steps
    for i in range(1, len(arr)):
        steps += 1
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            steps += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def timsort(inputs: list[str]):
    global steps

    def calculate_minrun(n):
        r = 0
        while n >= 32:
            r |= n & 1
            n >>= 1
        return n + r

    minrun = calculate_minrun(len(inputs))

    # Insertion sort based on lexicographical ordering up to minrun
    chunks = []
    for e in inputs:
        steps += 1
        if not len(chunks) or len(chunks[len(chunks) - 1]) == minrun:
            chunks.append([e])
            continue
        else:
            to_ins = chunks[len(chunks) - 1]
            i = 0
            while i < len(to_ins) and e > to_ins[i]:
                steps += 1
                i += 1
            to_ins.insert(i, e)
            chunks[len(chunks) - 1] = to_ins

    while len(chunks) > 1:
        steps += 1
        m = 0
        new_chunks = []
        while m < len(chunks) - 1:
            steps += 1
            aux = []
            l1 = chunks[m]
            l2 = chunks[m + 1]
            i = j = 0
            while i < len(l1) and j < len(l2):
                steps += 1
                if l2[j] > l1[i]:
                    aux.append(l1[i])
                    i += 1
                else:
                    aux.append(l2[j])
                    j += 1
            while i < len(l1):
                steps += 1
                aux.append(l1[i])
                i += 1
            while j < len(l2):
                steps += 1
                aux.append(l2[j])
                j += 1
            new_chunks.append(aux)
            m += 2
        if m == len(chunks) - 1:
            new_chunks.append(chunks[m])
        chunks = new_chunks
    res = chunks[0]

    return res


def timsort_brute(inputs: list[str]):
    global steps
    longest = len(inputs[0])
    for e in inputs:
        if len(e) > longest:
            longest = len(e)

    def padding(x: str):
        return x + "0" * (longest - len(x)) if len(x) < longest else x

    inputs = list(
        map(
            padding,
            inputs,
        )
    )

    for i, e in enumerate(inputs):
        inputs[i] = [[], [charset.index(c) for c in e]]

    # print(inputs)
    for _ in range(longest):
        steps += 1

        grouping = {}
        for e in inputs:
            key = ",".join(map(str, e[0]))
            if key not in grouping:
                grouping[key] = [e[1]]
            else:
                grouping[key].append(e[1])
        grouping_i = list(dict.items(grouping))

        def calculate_minrun(n):
            r = 0
            while n >= 32:
                r |= n & 1
                n >>= 1
            return n + r

        minrun = calculate_minrun(len(inputs))

        for h in grouping_i:
            steps += 1

            g = h[1]
            felem_g = [(s[0], s[1:]) for s in g]

            if timsort_mode == 1:
                chunks = [
                    felem_g[i : i + minrun] for i in range(0, len(felem_g), minrun)
                ]  # Split by minrun

                for chunk in chunks:  # Insertion sort
                    steps += 1
                    sorted_chunk = []
                    for e in chunk:
                        steps += 1
                        for i, r in enumerate(sorted_chunk):
                            steps += 1
                            if r[0] > e[0]:
                                sorted_chunk.insert(i, e)
                                break
                        else:
                            sorted_chunk.append(e)
                    chunk[:] = sorted_chunk
            else:
                chunks = []
                for i, t in enumerate(felem_g):  # Insertion sort until minrun
                    steps += 1
                    if not len(chunks) or len(chunks[len(chunks) - 1]) == minrun:
                        chunks.append([t])
                        continue
                    else:
                        to_ins = chunks[len(chunks) - 1]
                        j = 0
                        while j < len(to_ins) and t[0] > to_ins[j][0]:
                            steps += 1
                            j += 1
                        to_ins.insert(j, t)
                        chunks[len(chunks) - 1] = to_ins

            if debug == 2:
                print(
                    "".join(
                        list(
                            map(
                                lambda x: charset[int(x)] if int(x) != 0 else "",
                                list(filter(bool, h[0].split(","))),
                            )
                        )
                    ),
                    list(
                        map(
                            lambda x: list(
                                map(
                                    lambda y: (
                                        charset[y[0]] if int(y[0]) != 0 else "",
                                        "".join(
                                            list(
                                                map(
                                                    lambda z: charset[z]
                                                    if int(z) != 0
                                                    else "",
                                                    y[1],
                                                )
                                            )
                                        ),
                                    ),
                                    x,
                                )
                            ),
                            chunks,
                        )
                    ),
                )

            while len(chunks) > 1:
                steps += 1

                new_chunks = []
                for i in range(0, len(chunks), 2):  # Merge sort
                    steps += 1
                    if i < len(chunks) - 1:
                        res = []
                        m, n = 0, 0
                        while m < len(chunks[i]) or n < len(chunks[i + 1]):
                            steps += 1
                            if m < len(chunks[i]) and (
                                n == len(chunks[i + 1])
                                or chunks[i][m][0] < chunks[i + 1][n][0]
                            ):
                                res.append(chunks[i][m])
                                m += 1
                            elif n < len(chunks[i + 1]):
                                res.append(chunks[i + 1][n])
                                n += 1
                        new_chunks.append(res)
                    else:
                        steps += 1

                        new_chunks.append(chunks[i])
                chunks = new_chunks

            for nc in chunks:
                for i, c in enumerate(nc):
                    c[1].insert(0, c[0])
                    nc[i] = c[1]

            for c in chunks:
                grouping[h[0]] = c

        grouping_i = list(dict.items(grouping))
        inter = []
        for group in grouping_i:
            for item in group[1]:
                inter.append(
                    [list(filter(bool, group[0].split(","))) + [item[0]], item[1:]]
                )
        inputs = inter

    res = []
    for r in inputs:
        res.append("".join(map(lambda x: charset[int(x)] if int(x) != 0 else "", r[0])))
    return res


if __name__ == "__main__":
    algorithms = [timsort, mergesort, insertionsort, timsort_brute]
    while algo - 1 not in list(range(len(algorithms))):
        algo = int(input("Invalid algorithm. Choose which algorithm to use: "))
    print(f"Unsorted: {inputs} {len(inputs)}")
    res = list(map(lambda x: x.title(), algorithms[algo - 1](inputs)))
    print(f"Sorted: {res} {len(res)}")
    if debug:
        print(f"Took {steps} steps")
