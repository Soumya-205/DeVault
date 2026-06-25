import socket

def start_client():
    #open ONE connection and keep it open
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost',5000))
        print("Connect to DeVault. Type commands (SET, GET, DELETE, EXISTS) or EXIT to quit")

        while True:
            #take input from user
            command=input("DeVault> ").strip()

            #if user types EXIT, stop
            if command.upper()=="EXIT":
                print("Bye!")
                break
            #If user types nothing, skip
            if not command:
                continue

            #Send the command to the server
            client.send(command.encode())
            #get response
            response=client.recv(1024).decode().strip()
            print(response)
    
    except ConnectionRefusedError:
        print("Could not connect to DeVault. Is the server running?")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

start_client()    