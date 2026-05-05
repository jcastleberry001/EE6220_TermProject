import socket
import time

def server():

    #start TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('192.168.0.1', 12345))
        s.listen()
        print("Car1 Server is listening...")

        #server logic after TCP socket begins
        while True:

            #logic after a connection
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode('utf-8')
                #break connection if no data sent
                if not data: break
                #else, data available. sleep 1 second to show progression more clearly
                print(f"Message from {addr}: {data}")
                time.sleep(1)

                #logic for "emergency" signal
                if "emergency" in data.lower():
                    conn.sendall(b"Emergency Signal Accepted, Forwarding")
                    #sleep 1 second to show progression more clearly
                    time.sleep(1)
                    print("Closing Car2 Connection")
                    #sleep 1 second to show progression more clearly
                    time.sleep(1)
                    #begin attempts to connect to "RSU", sta1
                    for attempt in range(10):
                      try:
                          with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as a:
                              a.settimeout(5)
                              print(f"Attempt {attempt+1}: Connecting to Sta1")
                              #sleep 1 second to show progression more clearly
                              time.sleep(1)
                              #try to connect to "RSU"
                              a.connect(("192.168.0.100", 12345))
                              message = "emergency"
                              a.sendall(message.encode('utf-8'))
                              print(f"Message forwarded successfully to Sta1")
                              return
                      except Exception as e:
                        #error message in case "emergency" cannot be sent
                        print(f"Error:{e}")
                        time.sleep(1)

                else:
                   #if "emergency" is not sent from car2, or if data is different, then do not forward
                   conn.sendall(b"Random Data, Rejected")


if __name__ == "__main__":
    server()
