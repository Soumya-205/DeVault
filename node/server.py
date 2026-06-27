import socket
import threading
import json
import os

#---config----------
DATA_FILE="data/store.json"

#-----Persistence---------
def load_store():
    """Load data from disk on startup."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r')as f:
            return json.load(f)
    return  {}

def save_store():
    """Save current store to disk"""
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE,'w')as f:
        json.dump(store,f,indent=2)

#----Load data on startup------------------
store=load_store()
print(f"Loaded {len(store)} keys from disk")

#----Client Handler------------------------
def handle_client(conn, addr):
    print(f"Connected: {addr}")

    while True:
        try:
            data=conn.recv(1024).decode().strip().split('\n')[0]
            if not data:
                break
            parts=data.split()
            if not parts:
                continue

            command=parts[0].upper()

            if command=="SET":
               if len(parts)<3:
                   conn.send(b"ERROR: Usage: SET key value\n")
                   continue
               key, value=parts[1], parts[2]
               store[key]=value
               save_store()
               conn.send(b"Ok\n")

            elif command=="GET":
                if len(parts)<2:
                    conn.send(b"ERROR: Usage: GET key\n")
                    continue
                key=parts[1]
                value=store.get(key, None)
                conn.send(f"{value}\n" .encode() if value else b"NULL\n")

            elif command=="DELETE":
                if len(parts)<2:
                    conn.send(b"ERROR: Usage: DELETE key\n")
                    continue
                key=parts[1]
                if key in store:
                    del store[key]
                    save_store()
                    conn.send(b"DELETED\n")
                else:
                    conn.send(b"NULL\n")
            
            elif command=="EXISTS":
                if len(parts)<2:
                    conn.send(b"ERROR: Usage: EXISTS key\n")
                    continue
                key=parts[1]
                conn.send(b"YES\n" if key in store else b"NO\n")

            elif command=="KEYS":
                if store:
                    keys=", ".join(store.keys())
                    conn.send(f"{keys}\n".encode())
                else:
                    conn.send(b"(empty)\n")
            
            else:
                conn.send(b"ERROR: Unknown command. Use SET, GET, DELETE, EXISTS, KEYS\n")

        except Exception as e:
            print(f"Error:{e}")
            break

    conn.close()
    print(f"Disconnected: {addr}")

#-----start server----------------------------
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 5000))
server.listen(5)
print("DeVault running on port 5000...")

while True:
    conn, addr=server.accept()
    thread=threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon=True
    thread.start()
