from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    try:
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return generate_key()

def encrypt_file(filepath):
    key = load_key()
    fernet = Fernet(key)

    with open(filepath, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)
    encrypted_path = filepath + ".enc"

    with open(encrypted_path, 'wb') as enc_file:
        enc_file.write(encrypted)

    return encrypted_path

def decrypt_file(encrypted_path, output_path):
    key = load_key()
    fernet = Fernet(key)

    with open(encrypted_path, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(output_path, 'wb') as dec_file:
        dec_file.write(decrypted)
