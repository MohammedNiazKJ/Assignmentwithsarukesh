from cryptography.fernet import Fernet

def keygen():
    return Fernet.generate_key()

def write_key_to_file(key, filename):
    with open(filename, "wb") as key_file:
        key_file.write(key)

def load_key_from_file(filename):
    with open(filename, "rb") as key_file:
        return key_file.read()

def encrypt_file(filename, key):
    fernet = Fernet(key)
    with open(filename, "rb") as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(filename + ".encrypted", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

def decrypt_file(encrypted_filename, key):
    fernet = Fernet(key)
    with open(encrypted_filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    decrypted_filename = encrypted_filename.replace(".encrypted", "_decrypted.txt")
    with open(decrypted_filename, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

# Example usage:
def encrypt_and_decrypt_file(filename):
    key = keygen()
    write_key_to_file(key, "encryption_key.key")
    key = load_key_from_file("encryption_key.key")
    encrypt_file(filename, key)
    decrypt_file(filename + ".encrypted", key)

encrypt_and_decrypt_file("example.txt")

