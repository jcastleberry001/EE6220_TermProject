import socket
import time

def send_emergency():
    # Try to connect up to 10 times to account for simulation boot time
    for attempt in range(10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5) # Don't hang forever
                print(f"Crash detected, sending signal to nearby vehicle")
                time.sleep(1)
                print(f"Attempt {attempt+1}: Connecting to car1")
                time.sleep(1)
                s.connect(('192.168.0.1', 12345))
                
                message = "emergency"
                s.sendall(message.encode('utf-8'))
                
                data = s.recv(1024)
                print(f"Car1 responded: {data.decode('utf-8')}")
                return
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    send_emergency()
