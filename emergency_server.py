import socket
def server_e1():
  #start TCP socket
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('192.168.0.100', 12345))
    s.listen()
    print("Sta1 server is listening...")

    #"RSU" or sta1 logic after TCP socket begins
    while True:

      #logic after connection
      conn, addr = s.accept()
      with conn:
        data = conn.recv(1024).decode('utf-8')
        #break connection if no data sent
        if not data: break
        #else, data available.
        print(f"Message from {addr}: {data}")
        if "emergency" in data.lower():
          conn.sendall(b"Warning, crash detected, emergency vehicle notified.")
          #emergency data from car 1 successfully sent
          print(f"Emergency vehicle notified.")
        else:
          #error message in case "emergency" cannot be sent
          conn.sendall(b"Random Data, Rejected")
if __name__ == "__main__":
   server_e1()
