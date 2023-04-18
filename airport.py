import random
import threading
import time
from airport_class import Airport

start_time = time.time()
current_time = time.time()
delta_time = current_time - start_time
airport = Airport()
lock = threading.Lock()
threads = []
server_running = True

while delta_time < 3600:
    current_time = time.time()
    print("Waiting for the incoming connections")
    print("-------------------------------------")
    try:
        client_socket, address = airport.socket.accept()
    except Exception as e:
        print(f"Server closed connection")
        server_running = False
        break
    try:
        t = threading.Thread(target=airport.handle_new_client, args=(client_socket,))
        t.start()
        threads.append(t)
    except Exception as e:
        print(f"I tried to start new thread but i got Excpetion: {e}")
        server_running = False
        break

    delta_time = current_time - start_time

for t in threads:
    t.join()
    
if not server_running:
    airport.socket.close()
