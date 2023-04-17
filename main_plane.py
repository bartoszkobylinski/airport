
import time

def main(airplane):
    while True:
        if airplane:
            permision_to_aproach = airplane.permission_to_aproach()
            airplane.send_json(permision_to_aproach)
            airplane.recieve_permission(airplane.recv_json().get("message",''))
    
            while airplane.permission_granted and not airplane.landed :
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
                print(f"!!!!!!!!!!!!!!!: {cooridor_coordinates}")
                while airplane.inbound:
                    print(f"airplane landed: {airplane.landed}")
                    if airplane.landed:
                        print(f"waititng two seconds {time.sleep(2)}")
                        message = {"data":"landed", "cooridor": cooridor_coordinates.get("data").get("x")}
                        print(f"I've created massege {message}")
                        time.sleep(2)
                        airplane.send_json(message)
                        airplane.socket.close()
                        break
                    else:
                        message = airplane.fly_to_corridor_numpy(cooridor_coordinates.get("data").get("x"), cooridor_coordinates.get("data").get("y"), cooridor_coordinates.get("data").get("z"))
                        print(f"this is while inbounding: {message}")
                        airplane.send_json(message)

