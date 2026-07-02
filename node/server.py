import socket
import threading
import json
import os
import sys

#---config----------
PORT=int(sys.argv[1]) if len(sys.argv)>1 else 5000
DATA_FILE=f"data/store_{PORT}.json"

#Define which node this one replicates to
ALL_PORTS=[5000, 5001, 5002]
my_index=ALL_PORTS.index(PORT)
BACKUP_PORT=ALL_PORTS[(my_index + 1)% len(ALL_PORTS)]

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

def replicate_to_backup(command):
    """Forward a write command to the backup node."""
    try:
        backup=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backup.settimeout(2)
        backup.connect(('localhost', BACKUP_PORT))
        backup.send(f"REPLICATE {command}".encode())
        backup.recv(1024)
        backup.close()
    except Exception as e:
        print(f"Replication to {BACKUP_PORT} failed: {e}")

#----Load data on startup------------------
store=load_store()
print(f"Loaded {len(store)} keys from disk")
print(f"This node ({PORT}) replicates to port {BACKUP_PORT}")

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

            #Handle replicated commands from another node
            if command=="REPLICATE":
                parts=parts[1:] 
                command=parts[0].upper()
                if command=="SET" and len(parts)>=3:
                    store[parts[1]]=" ".join(parts[2:])
                    save_store()
                elif command=="DELETE" and len(parts)>=2:
                    if parts[1] in store:
                        del store[parts[1]]
                        save_store()
                conn.send(f"REPLICATED\n".encode())
                continue

            if command=="SET":
               if len(parts)<3:
                   conn.send(b"ERROR: Usage: SET key value\n")
                   continue
               key=parts[1]
               value=" ".join(parts[2:]) #join everything after key as value
               store[key]=value
               save_store()
               replicate_to_backup(f"SET {key} {value}")
               conn.send(b"Ok\n")

            elif command=="GET":
                if len(parts)<2:
                    conn.send(b"ERROR: Usage: GET key\n")
                    continue
                key=parts[1]
                value=store.get(key, None)
                if value is not None:
                    conn.send(f"{value}\n" .encode())
                else:
                    conn.send(b"NULL\n")

            elif command=="DELETE":
                if len(parts)<2:
                    conn.send(b"ERROR: Usage: DELETE key\n")
                    continue
                key=parts[1]
                if key in store:
                    del store[key]
                    save_store()
                    replicate_to_backup(f"DELETE {key}")
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
server.bind(('localhost', PORT))
server.listen(5)
print(f"DeVault Node running on port {PORT}...")

while True:
    conn, addr=server.accept()
    thread=threading.Thread(target=handle_client, args=(conn, addr))
    thread.daemon=True
    thread.start()
