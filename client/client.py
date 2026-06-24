import socket

def send_command(command):
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 5000))
    client.send(command.encode())
    response=client.recv(1024).decode()
    client.close()
    return response

#Testing all commands
print(send_command("SET name Anamika"))
print(send_command("SET age 20"))
print(send_command("GET name"))
print(send_command("GET age"))
print(send_command("GET city"))
print(send_command("EXISTS name"))
print(send_command("DELETE name"))
print(send_command("GET name"))