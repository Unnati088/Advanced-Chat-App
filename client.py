import socket, threading, tkinter as tk, tkinter.scrolledtext, pickle, os
from tkinter import filedialog, messagebox
from playsound import playsound
from encryption import decrypt_message
import database

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        client.connect((HOST, PORT))
        client.send(username.get().encode())
        threading.Thread(target=receive_messages).start()
    except:
        messagebox.showerror("Error", "Cannot connect to server!")

def receive_messages():
    while True:
        try:
            data = client.recv(4096)
            if data:
                message = pickle.loads(data)
                message['text'] = decrypt_message(message['text'])
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, f"{message['sender']}: {message['text']}\n")
                chat_box.yview(tk.END)
                chat_box.config(state=tk.DISABLED)
                playsound('notification.mp3')
        except:
            break

def send_message():
    msg = msg_entry.get()
    if msg:
        database.save_message(username.get(), msg)
        client.send(pickle.dumps({'sender': username.get(), 'text': msg}))
        msg_entry.delete(0, tk.END)

def send_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        client.send(pickle.dumps({'sender': username.get(), 'text': f"[File]: {os.path.basename(file_path)}"}))

def login():
    if database.login_user(username.get(), password.get()):
        login_window.destroy()
        build_chat_ui()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

def register():
    if database.register_user(username.get(), password.get()):
        messagebox.showinfo("Success", "Registered successfully!")
    else:
        messagebox.showerror("Error", "User already exists!")

def build_login_ui():
    global login_window, username, password
    login_window = tk.Tk()
    login_window.title("Login / Register")

    tk.Label(login_window, text="Username:").pack()
    username = tk.Entry(login_window)
    username.pack()

    tk.Label(login_window, text="Password:").pack()
    password = tk.Entry(login_window, show="*")
    password.pack()

    tk.Button(login_window, text="Login", command=login).pack()
    tk.Button(login_window, text="Register", command=register).pack()

    login_window.mainloop()

def build_chat_ui():
    global chat_box, msg_entry
    root = tk.Tk()
    root.title("Chat App")

    chat_box = tkinter.scrolledtext.ScrolledText(root, state=tk.DISABLED)
    chat_box.pack(padx=10, pady=10)

    msg_entry = tk.Entry(root)
    msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
    tk.Button(root, text="Send", command=send_message).pack(side=tk.LEFT)
    tk.Button(root, text="Send File", command=send_file).pack(side=tk.LEFT)

    connect()
    root.mainloop()

build_login_ui()
