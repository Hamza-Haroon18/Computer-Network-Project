
# 🖥️ Computer Network Project

This project is a **Chat + FTP Application** built for the Computer Networks course.  
It allows secure file transfer and real-time communication between multiple users using Python sockets.

---

## 🚀 Features

- 💬 **Encrypted Chat System** – Secure messaging between clients.
- 📁 **FTP File Upload & Download** – Upload and download encrypted files via a built-in FTP server.
- 🔐 **User Authentication** – Login and register with encrypted credentials.
- 🔑 **End-to-End Encryption** – Uses symmetric key encryption for both chat and file transfer.
- 🧰 **Graphical User Interface (GUI)** – Simple interface for users to interact easily.
- 🗂️ **Database Integration** – SQLite database for storing user information securely.

---

## 🧩 Project Structure

```

CN Project/
│
├── auth/                 # Handles authentication & database logic
├── chat_server/          # Chat server and client scripts
├── database/             # Database setup and user tables
├── downloads/            # Encrypted downloaded files
├── ftp_server/           # FTP server for file transfer
├── ftp_uploads/          # Encrypted uploaded files
├── gui/                  # Python GUI (main interface)
├── shared/               # Configuration files
├── utils/                # Encryption utilities
└── secret.key            # Encryption key (ignored in .gitignore)

````

---

### 2️⃣ Setup Environment

Make sure you have **Python 3.10+** installed.

Install dependencies (if any):

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Servers

Start the **Chat Server**:

```bash
python chat_server/server.py
```

Start the **FTP Server**:

```bash
python ftp_server/ftp_server.py
```

### 4️⃣ Run the GUI

```bash
python gui/main_gui.py
```

Now you can **chat** and **share encrypted files** securely 🎯

---

## 🧰 Technologies Used

* **Python 3**
* **Socket Programming**
* **SQLite**
* **Tkinter (GUI)**
* **Cryptography (Fernet Encryption)**

---

## 🧑‍💻 Author

**Muhammad Hamza Haroon**
🎓 Computer Science Student – NUCES FAST Karachi
🌐 GitHub: [Hamza-Haroon18](https://github.com/Hamza-Haroon18)

