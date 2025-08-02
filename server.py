import socket, threading, pickle
from encryption import encrypt_message, decrypt_message

HOST = '127.0.0.1'
PORT = 5000
clients = {}  # {conn: username}

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(pickle.dumps(message))
            except:
                client.close()
                del clients[client]

def handle_client(conn):
    while True:
        try:
            data = conn.recv(4096)
            if not data: break
            message = pickle.loads(data)
            message['text'] = encrypt_message(message['text'])
            broadcast(message, conn)
        except:
            break
    conn.close()
    if conn in clients: del clients[conn]

def receive_connections():
    server.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        username = conn.recv(1024).decode()
        clients[conn] = username
        print(f"{username} connected!")
        threading.Thread(target=handle_client, args=(conn,)).start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
receive_connections()
