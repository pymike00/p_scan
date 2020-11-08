from multiprocessing.pool import ThreadPool
import os
import socket

class PScan:

    def __init__(self):
        self.open_ports = list()
        self.remote_host = ""

    def scan_port(self, port):
        print(f"Scanning Port {port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            print(f"\nPort {port} is OPEN\n")
            self.open_ports.append(port)
        sock.close()

    def threadpool_executer(self, ports):
        number_of_workers = os.cpu_count()
        with ThreadPool(number_of_workers) as pool:
            pool.map(self.scan_port, ports)

    def run(self):
        self.remote_host = input("Target: ")
        self.threadpool_executer(range(1, 1000))


if __name__ == "__main__":
    scanner = PScan()
    scanner.run()