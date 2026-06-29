import socket
import sys
sys.path.append('.')
from node.consistent_hash import ConsistentHash

#Setting up the ring with the nodes
ring=ConsistentHash(replicas=3)
ring.add_node("localhost:5000")
ring.add_node("localhost:5001")

#Map node name to actual connection details
NODE_MAP={
    "localhost:5000": ("localhost", 5000),
    "localhost:5001": ("localhost", 5001)
}

def get_node(key):
    """Use consistent hashing to find the right node."""
    node_name=ring.get_node(key)
    return NODE_MAP[node_name]

def send_command(host, port, command):
    """Send the command to specific node."""
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.send(command.encode())
    response=client.recv(1024).decode().strip()
    client.close()
    return response

def start_client():
    print("Connected to DeVault cluster (Consistent Hashing enabled).")
    print("Commands: SET key value | GET key | DELETE key | EXISTS key | EXIT")

    while True:
        command=input("DeVault> ").strip()

        if command.upper()=="EXIT":
            print("Bye!")
            break
        if not command:
            continue

        parts=command.split()
        cmd=parts[0].upper()

        if cmd in ("SET", "GET", "DELETE", "EXISTS") and len(parts)>=2:
            key=parts[1]
            host, port=get_node(key)
            print(f" -> Routing to Node on port {port}")
            response=send_command(host, port, command)
            print(response)

        else:
            print("ERROR: Unknown command or missing key")

start_client()