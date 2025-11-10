import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import socket
from ftplib import FTP

from auth.auth_db import init_db, register_user, authenticate_user
from utils.encryption_utils import encrypt_file, decrypt_file


# -------------------- AUTH GUI --------------------
class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login / Register")
        self.root.geometry("300x200")

        tk.Label(root, text="Username").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=5)
        tk.Button(root, text="Register", command=self.register).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.root.destroy()
            self.on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if register_user(username, password):
            messagebox.showinfo("Success", "User registered! You can now log in.")
        else:
            messagebox.showerror("Error", "Username already exists.")


# -------------------- MAIN CHAT + FTP GUI --------------------
class ChatClientGUI:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.master.title(f"Chat Client - {username}")
        self.master.geometry("400x550")

        self.chat_frame = tk.Text(master, height=20, width=50, state='disabled')
        self.chat_frame.pack(pady=10)

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.send_message())

        self.send_btn = tk.Button(master, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        self.upload_btn = tk.Button(master, text="Upload File", command=self.upload_file)
        self.upload_btn.pack(pady=5)

        self.download_btn = tk.Button(master, text="Download Files", command=self.download_file)
        self.download_btn.pack(pady=5)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("127.0.0.1", 5555))

        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                msg = self.sock.recv(1024).decode()
                self.chat_frame.config(state='normal')
                self.chat_frame.insert(tk.END, msg + "\n")
                self.chat_frame.config(state='disabled')
                self.chat_frame.see(tk.END)
            except Exception as e:
                print(f"[ERROR] Receiving message: {e}")
                break

    def send_message(self):
        msg = self.entry.get()
        if msg:
            full_msg = f"{self.username}: {msg}"
            self.sock.send(full_msg.encode())
            self.entry.delete(0, tk.END)

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        try:
            enc_path = encrypt_file(file_path)

            ftp = FTP()
            ftp.connect("127.0.0.1", 2121)
            ftp.login("user", "12345")
            with open(enc_path, 'rb') as f:
                ftp.storbinary(f"STOR {os.path.basename(enc_path)}", f)
            ftp.quit()

            os.remove(enc_path)
            self.sock.send(f"{self.username}: Uploaded encrypted file '{os.path.basename(file_path)}'".encode())

        except Exception as e:
            self.sock.send(f"{self.username}: FTP Upload Failed - {e}".encode())

    def download_file(self):
        try:
            ftp = FTP()
            ftp.connect("127.0.0.1", 2121)
            ftp.login("user", "12345")
            files = ftp.nlst()

            enc_files = [f for f in files if f.endswith('.enc')]
            if not enc_files:
                messagebox.showinfo("Info", "No encrypted files found.")
                ftp.quit()
                return

            # Create selection window
            selector = tk.Toplevel(self.master)
            selector.title("Select Files to Download")
            selector.geometry("350x300")

            tk.Label(selector, text="Select files to download (Ctrl+Click to select multiple):").pack(pady=10)
            file_var = tk.StringVar(value=enc_files)

            listbox = tk.Listbox(selector, listvariable=file_var, height=12, selectmode=tk.MULTIPLE)
            listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

            scrollbar = tk.Scrollbar(selector)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=listbox.yview)

            def download_selected():
                selected_indices = listbox.curselection()
                if not selected_indices:
                    messagebox.showerror("Error", "No files selected.")
                    return

                os.makedirs("downloads", exist_ok=True)

                for i in selected_indices:
                    selected_file = listbox.get(i)
                    local_enc_path = os.path.join("downloads", selected_file)

                    with open(local_enc_path, 'wb') as f:
                        ftp.retrbinary(f"RETR {selected_file}", f.write)

                    decrypted_name = selected_file.replace('.enc', '')
                    decrypted_path = os.path.join("downloads", decrypted_name)
                    decrypt_file(local_enc_path, decrypted_path)

                    self.sock.send(f"{self.username}: Downloaded and decrypted '{decrypted_name}'".encode())

                ftp.quit()
                messagebox.showinfo("Success", "All selected files have been downloaded and decrypted.")
                selector.destroy()

            tk.Button(selector, text="Download Selected Files", command=download_selected).pack(pady=10)

        except Exception as e:
            self.sock.send(f"{self.username}: FTP Multi-Download Failed - {e}".encode())


# -------------------- BOOTSTRAP --------------------
def run_gui():
    def launch_chat(username):
        root = tk.Tk()
        app = ChatClientGUI(root, username)
        root.mainloop()

    init_db()
    login_root = tk.Tk()
    LoginWindow(login_root, launch_chat)
    login_root.mainloop()


if __name__ == "__main__":
    run_gui()
