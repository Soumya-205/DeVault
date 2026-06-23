import socket

#create the phone
client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Dial the server
client.connect(('localhost', 5000))

#say something
client.send(b"Hello server!")

#Listen for reply
response=client.recv(1024).decode()
print(f"Server replied: {response}")

client.close()