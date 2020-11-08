import socket

OPEN_PORTS = list()


def scan_port(remote_host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_status = sock.connect_ex((remote_host, port))
    if conn_status == 0:
        print(f"\nPort {port} is OPEN\n")
        OPEN_PORTS.append(port)
    sock.close()


def run():
    remote_host = input("Target: ")
    for port in range(1, 81):
        print(f"Scanning port: {port}")
        scan_port(remote_host, port)


if __name__ == "__main__":
    run()
    if OPEN_PORTS:
        print("#" * 20)
        print("Open Ports:")
        print(*OPEN_PORTS, sep=', ')
