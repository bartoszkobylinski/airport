import socket
import threading

class Airport(socket.socket):

    def __init__(self, host='127.0.0.1', port=7485 , encoder='utf-8', buffer=1024):
        self.host = host
        self.port = port
        self.encoder = encoder
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(2)
    
    def handle_new_client(self, client_socket):

        while True:
            
            data = client_socket.recv(self.buffer)
            print(data)
            if not data:
                break
            print("Received message: ", data.decode())
            if data.decode() == "stop":
                self.socket.close()
            client_socket.send("Response from server: Messsage received".encode())
    

airport = Airport()


while True:
    print("waititng for the incoming connections")
    try:
        client_socket, adrres = airport.socket.accept()
    except Exception as e:
        print(f"there is e: {e}")
        break
    try:
        t = threading.Thread(target=airport.handle_new_client, args=[client_socket])
        t.start()
    except Exception as e:
        print(f"I try start new thread but i got Excpetion: {e}")
    client_socket.send(b"Connect sucsfull")
