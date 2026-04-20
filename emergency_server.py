import socket
def server_e1():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.0.100', 12345))
    s.listen()
    print("Sta1 server is listening...")

    while True:
      conn, addr = s.accept()
      with conn:
        data = conn.recv(1024).decode('utf-8')
        if not data: break

        print(f"Message from {addr}: {data}")
        if "emergency" in data.lower():
          conn.sendall(b"Warning, crash detected, emergency vehicle notified.")
          print(f"Emergency vehicle notified.")
        else:
          conn.sendall(b"Random Data, Rejected")
if __name__ == "__main__":
   server_e1()
