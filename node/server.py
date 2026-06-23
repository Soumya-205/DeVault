import socket

#create the phone
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#pick up on port 5000
server.bind(('localhost',5000))

#start listening
server.listen(5)
print("Server is running on port 5000...")

#wait for someone to call
conn, addr=server.accept()
print(f"Someone connected from {addr}")

#receive their message
data=conn.recv(1024).decode()
print(f"They said: {data}")

#reply
conn.send(b"I got your message!")

conn.close()