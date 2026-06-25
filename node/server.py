import socket
import threading

#Our DataBase
store={}

def handle_client(conn, addr):
    print(f"Connected: {addr}")

    while True:
        try:
            data=conn.recv(1024).decode().strip().split('\n')[0]
            if not data:
                break

            parts=data.split()
            command=parts[0].upper()

            if command=="SET":
                key=parts[1]
                value=parts[2]
                store[key]=value
                conn.send(b"Ok\n")

            elif command=="GET":
                key=parts[1]
                if key in store:
                    conn.send(f"{store[key]}\n".encode())
                else:
                    conn.send(b"NULL\n")
                
            elif command=="DELETE":
                key=parts[1]
                if key in store:
                    del store[key]
                    conn.send(b"DELETED\n")
                else:
                    conn.send(b"NULL\n")
            
            elif command=="EXISTS":
                key=parts[1]
                if key in store:
                    conn.send(b"YES\n")
                else:
                    conn.send(b"NO\n")
            
            else:
                conn.send(b"UNKNOWN COMMAND\n")

        except Exception as e:
            print(f"Error: {e}")
            break
    
    conn.close()
    print(f"Disconnected: {addr}")

#start the server
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(5)
print("DeVault running on port 5000...")

while True:
    conn, addr=server.accept()
    thread=threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()