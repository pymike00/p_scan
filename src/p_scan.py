from multiprocessing.pool import ThreadPool
import os
import socket
import sys

import pyfiglet
from rich.console import Console

console = Console()


class PScan:
    def __init__(self):
        self.open_ports = []
        self.remote_host = ""

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            console.print(f"\nPort {port} is OPEN\n", style="bold blue")
            self.open_ports.append(port)
        sock.close()

    def threadpool_executer(self, ports):
        number_of_workers = os.cpu_count()
        console.print(
            f"Running Scanner using [bold blue]{number_of_workers}[/bold blue] workers."
        )
        with ThreadPool(number_of_workers) as pool:
            for loop_index, _ in enumerate(pool.imap(self.scan_port, ports), 1):
                advancment = loop_index / len(ports) * 100
                print("%.1f" % advancment)

    def show_completion_message(self):
        print()
        print("#" * 35)
        if self.open_ports:
            console.print("Open Ports:", style="bold green")
            console.print(*self.open_ports, sep=", ")
        else:
            console.print(f"No Open Ports Found on Target", style="bold green")

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
        console.print(
            f"\nIP address acquired: [bold blue]{ip_addr}[/bold blue]"
        )
        try:
            input("Press enter to move forward, CTRL + C to exit.")
        except KeyboardInterrupt:
            console.print(f"\nRoger that. Exiting.", style="bold red")
            sys.exit()
        return ip_addr

    def run(self):
        self.show_startup_message()
        try:
            target = input("Target: ")
        except KeyboardInterrupt:
            sys.exit("\nRoger that! Closing down.")
        self.remote_host = self.get_host_ip_addr(target)
        self.threadpool_executer(range(1, 81))
        self.show_completion_message()


if __name__ == "__main__":
    scanner = PScan()
    scanner.run()