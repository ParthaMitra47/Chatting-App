# import socket
# import threading

# clients = []
# client_names = {}

# # Function to handle each client connection
# def handle_client(client_socket):
#     client_socket.send("Enter your name: ".encode('utf-8'))
#     name = client_socket.recv(1024).decode('utf-8')
#     client_names[client_socket] = name
#     welcome_message = f"{name} has joined the chat!"
#     print(welcome_message)
#     broadcast_message(welcome_message, client_socket)

#     while True:
#         try:
#             message = client_socket.recv(1024).decode('utf-8')
#             if not message:
#                 break
#             broadcast_message(f"{name}: {message}", client_socket)
#         except ConnectionResetError:
#             break
#     client_socket.close()
#     clients.remove(client_socket)
#     goodbye_message = f"{name} has left the chat!"
#     print(goodbye_message)
#     broadcast_message(goodbye_message, client_socket)
#     del client_names[client_socket]

# def broadcast_message(message, sender_socket):
#     for client in clients:
#         if client != sender_socket:
#             try:
#                 client.send(message.encode('utf-8'))
#             except:
#                 client.close()
#                 clients.remove(client)

# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('0.0.0.0', 9999))
#     server.listen(5)
#     print("Server listening on port 9999")

#     while True:
#         client_socket, addr = server.accept()
#         clients.append(client_socket)
#         print(f"Accepted connection from {addr}")
#         client_handler = threading.Thread(target=handle_client, args=(client_socket,))
#         client_handler.start()

# if __name__ == "__main__":
#     main()


# With GUI



import socket
import threading

clients = []
client_names = {}

def handle_client(client_socket):
    name = client_socket.recv(1024).decode('utf-8')
    client_names[client_socket] = name
    welcome_message = f"{name} has joined the chat!"
    print(welcome_message)
    broadcast_message(welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast_message(f"{name}: {message}", client_socket)
        except ConnectionResetError:
            break
    client_socket.close()
    clients.remove(client_socket)
    goodbye_message = f"{name} has left the chat!"
    print(goodbye_message)
    broadcast_message(goodbye_message, client_socket)
    del client_names[client_socket]

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
