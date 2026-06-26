import socket
import threading
import json
import os 

#file where we save our data
DATA_FILE="data/store.json"

#load existing data from file if it exists
def load_store():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save store to file
def save_store():
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(store, f)

#load data on startup
store=load_store()
print(f"Loaded {len(store)} keys from disk.")

def handle_clients(conn, addr):
    print(f"Connected: {addr}")

    while True:
        try:
            data=conn.recv(1024).decode().strip()
            if not data:
                break

            parts=data.split()
            command=parts[0].upper()

            if command=="SET":
                key=parts[1]
                value=parts[2]
                store[key]=value
                save_store()
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
                    save_store()
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
server.bind(('localhost',5000))
server.listen(5)
print("DeVault running on port 5000...")

while True:
    conn, addr=server.accept()
    thread=threading.Thread(target=handle_clients, args=(conn, addr))
    thread.start()