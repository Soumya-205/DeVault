import socket

#Two nodes
NODES=[
    ('localhost', 5000),
    ('localhost', 5001)
]

def get_node(key):
    """Decide which node handles this key."""
    index=hash(key)%len(NODES)
    return NODES[index]

def send_command(host, port, command):
    """Send a command to a specific node"""
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(command.encode())
    response=client.recv(1024).decode().strip()
    client.close()
    return response

def start_client():
    print("Connected to DeVault cluster.")
    print("Commands: SET key value | GET key | EXISTS key | EXIT")

    while True:
        command=input("DeVault> ").strip()

        if command.upper()=="EXIT":
            print("BYE!")
            break;
        
        if not command:
            continue

        parts=command.split()
        cmd=parts[0].upper()

        #for key-based commands, route to correct node
        if cmd in ("SET", "GET", "DELETE", "EXISTS") and len(parts)>=2:
            key=parts[1]
            host, port=get_node(key)
            print(f" ->Routing to Node on port {port}")
            response=send_command(host, port, command)
            print(response)
        else:
            print("ERROR: Unknown command or missing key")
start_client()