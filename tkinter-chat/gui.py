import tkinter as tk
from tkinter import messagebox
import requests
import threading
import socketio

# Flask 서버 URL
SERVER_URL = "http://127.0.0.1:5000"
sio = socketio.Client()

# 회원가입 창
def register_window():
    def handle_register():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            response = requests.post(f"{SERVER_URL}/register", json={"username": username, "password": password})
            data = response.json()
            if response.status_code == 200:
                messagebox.showinfo("Success", data.get("message", "Registered successfully!"))
                register_win.destroy()
            else:
                messagebox.showerror("Error", data.get("error", "Failed to register."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    register_win = tk.Toplevel()
    register_win.title("Register")
    register_win.geometry("400x300")

    tk.Label(register_win, text="Register", font=("Helvetica", 16, "bold")).pack(pady=20)
    tk.Label(register_win, text="Username:", font=("Helvetica", 12)).pack(pady=5)
    username_entry = tk.Entry(register_win, width=30)
    username_entry.pack(pady=5)
    tk.Label(register_win, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    password_entry = tk.Entry(register_win, width=30, show="*")
    password_entry.pack(pady=5)
    tk.Button(register_win, text="Register", font=("Helvetica", 12), command=handle_register).pack(pady=20)

# 채팅룸 창
def chatroom_window(root, username):
    root.withdraw()  # 메인 창 숨기기

    def connect_to_server():
        try:
            sio.connect(SERVER_URL)
            sio.emit("join", {"username": username})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def send_message():
        message = message_entry.get()
        if not message:
            return

        sio.emit("send_message", {"message": message, "username": username})
        message_entry.delete(0, tk.END)

    def receive_message(data):
        chat_frame.config(state=tk.NORMAL)
        if data['username'] == username:
            chat_frame.insert(
                tk.END,
                f"\n    {data['message']}\n",
                "self_message"
            )
        else:
            chat_frame.insert(
                tk.END,
                f"{data['username']}\n{data['message']}\n",
                "other_message"
            )
        chat_frame.see(tk.END)  # 스크롤을 가장 아래로 이동
        chat_frame.config(state=tk.DISABLED)

    sio.on("receive_message", receive_message)

    chat_win = tk.Toplevel()
    chat_win.title("Chat Room")
    chat_win.geometry("500x500")

    tk.Label(chat_win, text=f"Logged in as: {username}", font=("Helvetica", 12)).pack(pady=10)

    chat_area = tk.Frame(chat_win)
    chat_area.pack(fill=tk.BOTH, expand=True)

    chat_scrollbar = tk.Scrollbar(chat_area)
    chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_frame = tk.Text(
        chat_area,
        height=20,
        width=50,
        state=tk.DISABLED,
        yscrollcommand=chat_scrollbar.set,
        wrap="word",
        font=("Arial", 12)
    )
    chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    chat_frame.tag_config("self_message", foreground="black", background="#D1FFD6", justify="right")
    chat_frame.tag_config("other_message", foreground="black", background="#FFFFFF", justify="left")

    chat_scrollbar.config(command=chat_frame.yview)

    message_entry = tk.Entry(chat_win, width=40)
    message_entry.pack(side=tk.LEFT, padx=5, pady=10)
    tk.Button(chat_win, text="Send", command=send_message).pack(side=tk.RIGHT, padx=5, pady=10)

    threading.Thread(target=connect_to_server, daemon=True).start()
    chat_win.protocol("WM_DELETE_WINDOW", lambda: (sio.disconnect(), chat_win.destroy(), root.destroy()))

# 로그인 창
def login_window():
    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            response = requests.post(f"{SERVER_URL}/login", json={"username": username, "password": password})
            data = response.json()
            if response.status_code == 200:
                messagebox.showinfo("Success", data.get("message", "Login successful!"))
                chatroom_window(login_win, username)
            else:
                messagebox.showerror("Error", data.get("error", "Login failed."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    login_win = tk.Tk()
    login_win.title("Chat App")
    login_win.geometry("400x400")

    tk.Label(login_win, text="Chat App", font=("Helvetica", 24, "bold")).pack(pady=50)

    tk.Label(login_win, text="Username:", font=("Helvetica", 12)).pack(pady=5)
    username_entry = tk.Entry(login_win, width=30)
    username_entry.pack(pady=5)

    tk.Label(login_win, text="Password:", font=("Helvetica", 12)).pack(pady=5)
    password_entry = tk.Entry(login_win, width=30, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_win, text="Login", font=("Helvetica", 12), command=handle_login).pack(pady=20)
    tk.Button(login_win, text="Register", font=("Helvetica", 12), command=register_window).pack(pady=5)

    login_win.mainloop()

if __name__ == "__main__":
    login_window()
