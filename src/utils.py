import json
from multiprocessing.pool import ThreadPool
import os
import os

from rich.console import Console

console = Console()


PORTS_DATA_FILE = "./common_ports.json"


def display_progress(iteration, total):
    bar_max_width = 45  # chars
    bar_current_width = bar_max_width * iteration // total
    bar = "█" * bar_current_width + "-" * (bar_max_width - bar_current_width)
    progress = "%.1f" % (iteration / total * 100)
    console.print(f"|{bar}| {progress} %", end="\r", style="bold green")
    if iteration == total:
        print()


def threadpool_executer(function, iterable, iterable_length):
    number_of_workers = os.cpu_count()
    console.print(
        f"\nRunning using [bold blue]{number_of_workers}[/bold blue] workers.\n"
    )
    with ThreadPool(number_of_workers) as pool:
        for loop_index, _ in enumerate(pool.imap(function, iterable), 1):
            display_progress(loop_index, iterable_length)


def extract_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def get_ports_info():
    data = extract_json_data(PORTS_DATA_FILE)
    return {int(k): v for (k, v) in data.items()}


if __name__ == "__main__":
    print(get_ports_info())