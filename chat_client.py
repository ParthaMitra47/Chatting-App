# import socket
# import threading

# def receive_messages(client):
#     while True:
#         try:
#             message = client.recv(4096).decode('utf-8')
#             print(message)
#         except:
#             print("An error occurred. Exiting...")
#             client.close()
#             break

# def main():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect(('127.0.0.1', 9999))

#     receive_thread = threading.Thread(target=receive_messages, args=(client,))
#     receive_thread.start()

#     name = input("Enter your name: ")
#     client.send(name.encode('utf-8'))

#     while True:
#         message = input()
#         try:
#             client.send(message.encode('utf-8'))
#         except:
#             print("An error occurred. Exiting...")
#             client.close()
#             break

# if __name__ == "__main__":
#     main()


# with GUI


import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, END
import tkinter.simpledialog as simpledialog
import queue

def receive_messages(client, message_queue):
    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            message_queue.put(message)
        except:
            message_queue.put("An error occurred. Exiting...")
            client.close()
            break

def update_chat_window(chat_window, message_queue, root):
    while not message_queue.empty():
        message = message_queue.get_nowait()
        chat_window.configure(state='normal')
        chat_window.insert(END, f"{message}\n")
        chat_window.configure(state='disabled')
        chat_window.see(END)
    root.after(100, update_chat_window, chat_window, message_queue, root)

def send_message(client, entry_field):
    message = entry_field.get()
    client.send(message.encode('utf-8'))
    entry_field.delete(0, END)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))

    # Create the main window
    root = tk.Tk()
    root.title("Chat Application")

    # Create chat window
    chat_window = scrolledtext.ScrolledText(root, state='disabled', wrap='word')
    chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Create entry field for sending messages
    entry_field = tk.Entry(root)
    entry_field.pack(padx=10, pady=10, fill=tk.X, expand=True)

    # Create send button
    send_button = tk.Button(root, text="Send", command=lambda: send_message(client, entry_field))
    send_button.pack(padx=10, pady=10)

    # Create a queue to communicate between threads
    message_queue = queue.Queue()

    # Start the receive thread
    receive_thread = threading.Thread(target=receive_messages, args=(client, message_queue))
    receive_thread.start()

    # Prompt user for name and send to server
    name = simpledialog.askstring("Name", "Enter your name:")
    client.send(name.encode('utf-8'))

    # Start updating the chat window
    root.after(100, update_chat_window, chat_window, message_queue, root)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
