from Cryptography import generate_key_pair
from Crypto.PublicKey import RSA
from pathlib import Path
from getpass import getuser
import ctypes
import os

user = getuser()  
directory_path = "C:/Users/{}/Hybrid Encryption".format(user)  
keys_path = "{}/DoNotDelete".format(directory_path)  

def is_keys_exist():

    return Path(keys_path).is_dir()


def is_file_exist():

    public_key_path = f"{keys_path}/public key.pem"
    private_key_path = f"{keys_path}/private key.pem"
    is_public_key_exist = os.path.isfile(public_key_path) and os.stat(public_key_path).st_size != 0
    is_private_key_exist = os.path.isfile(private_key_path) and os.stat(private_key_path).st_size != 0

    return is_public_key_exist and is_private_key_exist


def create_keys_directory():

    Path(keys_path).mkdir(parents=True, exist_ok=True)
    FILE_ATTRIBUTE_HIDDEN = 0x02
    try:
        ctypes.windll.kernel32.SetFileAttributesW(keys_path, FILE_ATTRIBUTE_HIDDEN)
    except Exception as windows_error:
        print(windows_error)


def is_encryption_directory_exist():

    return Path(directory_path).is_dir()


def create_encryption_directory():

    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
    except Exception as directory_error:
        print(directory_error)


def generating_keys():
    public_key, private_key = generate_key_pair.generate_key_pair()

    e, n = public_key
    d, a = private_key

    public_key = RSA.construct((n, e))
    private_key = RSA.construct((n, e, d))

    private_key = private_key.exportKey("PEM")
    public_key = public_key.exportKey("PEM")

    return public_key, private_key


def save_keys():
    if not is_encryption_directory_exist():
        create_encryption_directory()
        create_keys_directory()

    if not is_keys_exist():
        create_keys_directory()

    try:
        public_key, private_key = generating_keys()
        public_key_writer = open(f"{keys_path}/public key.pem", "wb")
        public_key_writer.write(public_key)
        public_key_writer.close()

        private_key_writer = open(f"{keys_path}/private key.pem", "wb")
        private_key_writer.write(private_key)
        private_key_writer.close()

    except Exception as file_error:
        print(file_error)


def get_public_key():

    path_of_public_key = f"{keys_path}/public key.pem"
    if not is_file_exist():
        save_keys()

    public_key_reader = open(path_of_public_key, "rb")
    public_key = public_key_reader.read()
    public_key_reader.close()
    return public_key


def get_private_key():

    path_of_private_key = f"{keys_path}/private key.pem"
    if not is_file_exist():
        save_keys()

    private_key_reader = open(path_of_private_key, "rb")
    private_key = private_key_reader.read()
    private_key_reader.close()
    return private_key
