
import time
from plane_class import Airplane

def main(airplane):
    while True:
        if airplane:
            permission_to_approach = airplane.permission_to_aproach()
            print(f"this is permission_to_approach: {permission_to_approach}")
            airplane.send_json(permission_to_approach)
            a = airplane.recieve_permission(airplane.recv_json().get("message", ''))
            print(f"this is after recieve perminssion{a}")
            while airplane.permission_granted and not airplane.airplane_flight.landed:
                print("I'm in")
                message = airplane.airplane_flight.fly_randomly()
                airplane.send_json(message)
                server_message = airplane.recv_json()
                print(f"Server has sent me this: {server_message}")
                time.sleep(1)
                message = airplane.send_permission_to_inbound()
                print(f"I have sent permission to inbound: {message}")
                airplane.send_json(message)
                server_message = airplane.recv_json()
                print(f"I have got message from server: {server_message}")
                corridor_coordinates = airplane.recieve_permisssion_for_inbounding(server_message)
                print(f"!!!!!!!!!!!!!!!: {corridor_coordinates}")
                while airplane.inbound:
                    print(f"airplane landed: {airplane.airplane_flight.landed}")
                    if airplane.airplane_flight.landed:
                        print(f"waiting two seconds {time.sleep(2)}")
                        message = {"data": "landed", "corridor": corridor_coordinates.get("data").get("x")}
                        print(f"I've created message {message}")
                        time.sleep(2)
                        airplane.send_json(message)
                        airplane.socket.close()
                        break
                    else:
                        message = airplane.airplane_flight.fly_to_corridor_numpy(corridor_coordinates.get("data").get("x"), corridor_coordinates.get("data").get("y"), corridor_coordinates.get("data").get("z"))
                        print(f"this is while inbounding: {message}")
                        airplane.send_json(message)


