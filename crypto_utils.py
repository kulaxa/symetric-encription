from Crypto.Cipher import AES
from Crypto.Hash import SHA512, SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from properties import *


def check_num_args(arguments, num_of_args) -> int:
    if len(arguments) != num_of_args:
        print("Wrong number of arguments provided!")
        exit(1)


def check_master_password(master_password) -> bool:
        try:
            init_hash_address = SHA256.new(data=bytes(INIT_ADDRESS, 'utf-8')).hexdigest()
            decrypt(init_hash_address, r.get(init_hash_address), master_password)
        except:
            return False
        return True


def decrypt(address, ciphertext, master_password) -> str:
    key = PBKDF2(bytes(master_password, 'utf-8'), bytes(address, 'utf-8'), 32, count=1000, hmac_hash_module=SHA512)
    nonce = ciphertext[:16]
    tag = ciphertext[16:32]
    ciphertext = ciphertext[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext_padded = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        plaintext = unpad(plaintext_padded, AES.block_size)
    except ValueError:
        print("Key incorrect or message corrupted")
        exit(1)
    return plaintext


def encrypt(address, password, master_password) -> str:
    key = PBKDF2(bytes(master_password, 'utf-8'), bytes(address, 'utf-8'), 32, count=1000, hmac_hash_module=SHA512)
    cipher = AES.new(bytes(key), AES.MODE_EAX)
    nonce = cipher.nonce # 16 bytes
    ciphertext, tag= cipher.encrypt_and_digest(pad(bytes(password, 'utf-8'), AES.block_size))
    ciphertext = nonce + tag + ciphertext
    return ciphertext
