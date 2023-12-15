from timsort import timsort, mergesort, insertionsort, timsort_brute
from matplotlib import pyplot as plt
from multiprocessing import Pool
import plotly.tools as tls
import plotly.io as pio
from faker import Faker
from tqdm import tqdm
import datetime
import time

fake = Faker()


def generate_names(n):
    return [fake.name().lower() for _ in range(n)]


if __name__ == "__main__":
    input_size = int(input("Input size: "))
    with Pool() as p:
        inputs = list(
            tqdm(p.imap(generate_names, [input_size] * 100), total=100, desc="Dataset")
        )

    def measure_time(sort_func, lst):
        start_time = time.time()
        sort_func(lst)
        end_time = time.time()
        return end_time - start_time

    timsort_times = [measure_time(timsort, lst) for lst in tqdm(inputs, desc="timsort")]
    mergesort_times = [
        measure_time(mergesort, lst) for lst in tqdm(inputs, desc="mergesort")
    ]
    insertionsort_times = [
        measure_time(insertionsort, lst) for lst in tqdm(inputs, desc="insertionsort")
    ]
    # timsort_brute_times = [
    #     measure_time(timsort_brute, lst) for lst in tqdm(inputs, desc="timsort_brute")
    # ]

    fig, ax = plt.subplots()

    ax.plot(timsort_times, label="timsort")
    ax.plot(mergesort_times, label="mergesort")
    ax.plot(insertionsort_times, label="insertionsort")
    # ax.plot(timsort_brute_times, label="timsort_brute")

    ax.set_title(f"Input array size: {input_size}")
    ax.set_xlabel("Input index")
    ax.set_ylabel("Time (seconds)")
    ax.legend()

    pio.write_html(
        tls.mpl_to_plotly(fig),
        file=f"figure-{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.html",
    )
