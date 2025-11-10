import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(f"\n{msg}")
        except:
            break

def start_client(username):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 5555))

    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    while True:
        msg = input()
        sock.send(f"{username}: {msg}".encode())

# Example usage:
# start_client("user1")
