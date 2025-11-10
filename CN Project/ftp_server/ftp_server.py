from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

def run_ftp_server():
    upload_path = os.path.join(os.getcwd(), "ftp_uploads")
    os.makedirs(upload_path, exist_ok=True)
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", upload_path, perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("0.0.0.0", 2121), handler)
    print("FTP Server running on port 2121...")
    server.serve_forever()

if __name__ == "__main__":
    run_ftp_server()
