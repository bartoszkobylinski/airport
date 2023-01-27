
import time
from plane_class import Airplane

airplane = Airplane()

while True:

    permision_to_aproach = airplane.permission_to_aproach()
    airplane.send_json(permision_to_aproach)
    airplane.recieve_permission(airplane.recv_json().get("message",''))
    
    while airplane.permission_granted :
        message = airplane.fly_randomly()
        airplane.send_json(message)
        server_message = airplane.recv_json()
        print(f"Server has sendt me this: {server_message}")
        time.sleep(1)
        message = airplane.send_permission_to_inbound()
        print(f"I have send permission to inbound: {message}")
        airplane.send_json(message)
        server_message = airplane.recv_json()
        print(f"I have got messag fro server: {server_message}")
        cooridor_coordinates = airplane.recieve_permisssion_for_inbounding(server_message)
        print(cooridor_coordinates)
        while airplane.inbound:
            if airplane.landed:
                airplane.socket.close()
                break
            else:
                message = airplane.fly_to_corridor_numpy(cooridor_coordinates.get("data").get("x"), cooridor_coordinates.get("data").get("y"), cooridor_coordinates.get("data").get("z"))
                print(message)
                airplane.send_json(message)
        
        
    else:
        del airplane

