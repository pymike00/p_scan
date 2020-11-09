from multiprocessing.pool import ThreadPool
import os
import socket
import sys

import pyfiglet

class PScan:

    def __init__(self):
        self.open_ports = []
        self.remote_host = ""

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            print(f"\nPort {port} is OPEN\n")
            self.open_ports.append(port)
        sock.close()

    def threadpool_executer(self, ports):
        number_of_workers = os.cpu_count()
        print(f"\nRunning Scanner using {number_of_workers} workers.")
        with ThreadPool(number_of_workers) as pool:
            for loop_index, _ in enumerate(pool.imap(self.scan_port, ports), 1):
                advancment = loop_index / len(ports) * 100
                print("%.1f" % advancment)

    def show_completion_message(self):
        print()
        print("#" * 20)
        if self.open_ports:
            print("Open Ports:")
            print(*self.open_ports, sep=', ')
        else:
            print(f"No Open Ports Found on {self.remote_host}")

    @staticmethod
    def show_startup_message():
        ascii_art = pyfiglet.figlet_format("P SCAN")
        print(ascii_art)
        print("#" * 35)
        print("A bare bone Python TCP Port Scanner")
        print("#" * 35)
        print()

    def run(self):
        self.show_startup_message()
        try:
            self.remote_host = input("Target: ")
        except KeyboardInterrupt:
            sys.exit("\nRoger that! Closing down.")
        self.threadpool_executer(range(1, 1000))
        self.show_completion_message()


if __name__ == "__main__":
    scanner = PScan()
    scanner.run()