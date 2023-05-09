import random
import threading
import time
from airport_class import Airport
from airport_instance import Airport as Ap

start_time = time.time()
current_time = time.time()
delta_time = current_time - start_time
#airport = Airport()
airport = Ap()
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
        print(f"An exception occurred while attempting to start a new thread. The details are as follows: "
              f"Exception Type: {type(e).__name__} \nException Message: {str(e)}")
        server_running = False
        break

    delta_time = current_time - start_time

for t in threads:
    t.join()
    
if not server_running:
    airport.socket.close()
