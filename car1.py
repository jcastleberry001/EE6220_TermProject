import socket
import time

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('192.168.0.1', 12345))
        s.listen()
        print("Car1 Server is listening...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                if not data: break
                
                print(f"Message from {addr}: {data}")
                time.sleep(1)
                if "emergency" in data.lower():
                    conn.sendall(b"Emergency Signal Accepted, Forwarding")
                    time.sleep(1)
                    print("Closing Car2 Connection")
                    time.sleep(1)
                    for attempt in range(10):
                      try:
                          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                              a.settimeout(5)
                              print(f"Attempt {attempt+1}: Connecting to Sta1")
                              time.sleep(1)
                              a.connect(("192.168.0.100", 12345))
                              message = "emergency"
                              a.sendall(message.encode('utf-8'))
                              print(f"Message forwarded successfully to Sta1")
                              return
                      except Exception as e:
                        print(f"Error:{e}")
                        time.sleep(1)

                else:
                   conn.sendall(b"Random Data, Rejected")


if __name__ == "__main__":
    server()
