import threading
import time
from airport_class.airport_instance import Airport
from .db_manager import DbManager

'''
database = DbManager("airport_class")

start_time = time.time()
current_time = time.time()
delta_time = current_time - start_time

airport_class = Airport()
threads = []
server_running = True

while delta_time < 3600:
    current_time = time.time()
    print("Waiting for the incoming connections")
    print("-------------------------------------")
    try:
        print("I'm here")
        client_socket, address = airport_class.socket.accept()
    except Exception as e:
        print(e)
        print(f"Server closed connection")
        server_running = False
        break
    try:
        t = threading.Thread(target=airport_class.handle_new_client, args=(client_socket,))
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
    airport_class.socket.close()
'''


class AirportSimulator:
    def __init__(self):
        self.database = DbManager()
        self.start_time = time.time()
        self.current_time = time.time()
        self.delta_time = self.current_time - self.start_time
        self.airport = Airport()
        self.threads = []
        self.server_running = True

    def run_simulation(self, simulation_time=3600):
        while self.delta_time < simulation_time:
            self.current_time = time.time()
            print("Waiting for the incoming connections")
            print("-------------------------------------")
            try:
                print("I'm here")
                client_socket, address = self.airport.socket.accept()
            except Exception as e:
                print(e)
                print(f"Server closed connection")
                self.server_running = False
                break
            try:
                t = threading.Thread(target=self.airport.handle_new_client, args=(client_socket,))
                t.start()
                self.threads.append(t)
            except Exception as e:
                print(f"An exception occurred while attempting to start a new thread. The details are as follows: "
                      f"Exception Type: {type(e).__name__} \nException Message: {str(e)}")
                self.server_running = False
                break

            self.delta_time = self.current_time - self.start_time

        for t in self.threads:
            t.join()

        if not self.server_running:
            self.airport.socket.close()
