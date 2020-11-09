from multiprocessing.pool import ThreadPool
import os
import socket
import sys

import pyfiglet
from rich.console import Console
from rich.table import Table

from utils import get_ports_info

console = Console()


class PScan:
    def __init__(self):
        self.ports_info = {}
        self.open_ports = []
        self.remote_host = ""

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            self.open_ports.append(port)
        sock.close()

    @staticmethod
    def display_progress(iteration, total):
        bar_max_width = 45 # chars
        bar_current_width = bar_max_width * iteration // total
        bar = "█" * bar_current_width + "-" * (bar_max_width - bar_current_width)
        progress = "%.1f" % (iteration / total * 100)
        console.print(f"|{bar}| {progress} %", end="\r", style="bold green")
        if iteration == total:
            print()

    def threadpool_executer(self, ports_list, ports_list_length):
        number_of_workers = os.cpu_count()
        console.print(
            f"\nRunning Scanner using [bold blue]{number_of_workers}[/bold blue] workers.\n"
        )
        with ThreadPool(number_of_workers) as pool:
            for loop_index, _ in enumerate(pool.imap(self.scan_port, ports_list), 1):
                self.display_progress(loop_index, ports_list_length)

    def show_completion_message(self):
        print()
        if self.open_ports:
            console.print("Scan Completed. Open Ports:", style="bold blue")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("PORT")
            table.add_column("STATE", justify="center")
            table.add_column("SERVICE")
            for port in self.open_ports:
                table.add_row(str(port), "OPEN", self.ports_info[port])
            console.print(table)
        else:
            console.print(f"No Open Ports Found on Target", style="bold magenta")

    @staticmethod
    def show_startup_message():
        ascii_art = pyfiglet.figlet_format("P SCAN")
        console.print(f"[bold green]{ascii_art}[/bold green]")
        console.print("#" * 35, style="bold green")
        console.print("A bare bone Python TCP Port Scanner", style="bold green")
        console.print("#" * 35, style="bold green")
        print()

    @staticmethod
    def get_host_ip_addr(target):
        try:
            ip_addr = socket.gethostbyname(target)
        except socket.gaierror as e:
            console.print(f"{e}. Exiting.", style="bold red")
            sys.exit()
        console.print(f"\nIP address acquired: [bold blue]{ip_addr}[/bold blue]")
        try:
            input("Press enter to move forward, CTRL + C to exit.")
        except KeyboardInterrupt:
            console.print(f"\nRoger that. Exiting.", style="bold red")
            sys.exit()
        return ip_addr

    def initial_setup(self):
        self.show_startup_message()
        self.ports_info = get_ports_info()

    def run(self):
        try:
            target = input("Target: ")
        except KeyboardInterrupt:
            sys.exit("\nRoger that! Closing down.")
        self.remote_host = self.get_host_ip_addr(target)
        self.threadpool_executer(self.ports_info.keys(), len(self.ports_info))
        self.show_completion_message()


if __name__ == "__main__":
    scanner = PScan()
    scanner.initial_setup()
    scanner.run()