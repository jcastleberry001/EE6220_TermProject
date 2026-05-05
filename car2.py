import socket
import time

def send_emergency():
    #Start crash message from car2
    #Try to connect up to 10 times to account for simulation boot time
    for attempt in range(10):
        try:
            #start TCP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                print(f"Crash detected, sending signal to nearby vehicle")
                #sleep 1 second to show progression more clearly
                time.sleep(1)
                print(f"Attempt {attempt+1}: Connecting to car1")
                #sleep 1 second to show progression more clearly
                time.sleep(1)
                #try to connect to car1
                s.connect(('192.168.0.1', 12345))
                
                message = "emergency"
                s.sendall(message.encode('utf-8'))
                #if data was received correctly by car1, send confirmation
                data = s.recv(1024)
                print(f"Car1 responded: {data.decode('utf-8')}")
                return
        except Exception as e:
            #error message in case "emergency" cannot be sent
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    send_emergency()
