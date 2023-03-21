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
        init_hash_address = SHA256.new(data=bytes(INIT_ADDRESS + PASSWORD_DELIMITER + master_password, 'utf-8')).hexdigest()
        decrypt(init_hash_address, r.get(init_hash_address), master_password)
    except:
        return False
    return True


def decrypt(address_hash, ciphertext, master_password) -> str:
    key = PBKDF2(bytes(master_password, 'utf-8'), bytes(address_hash, 'utf-8'), 32, count=1000, hmac_hash_module=SHA512)
    nonce = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext_padded = cipher.decrypt(ciphertext)
    try:
        decrypted_address_hash = str(plaintext_padded).split(PASSWORD_DELIMITER)[0][2:]
    except:
        print("Key incorrect or message corrupted")
        exit(1)
    if decrypted_address_hash == address_hash:
        plaintext = unpad(plaintext_padded, 512, style='iso7816')
        decrypted_address_password = str(plaintext, 'utf-8').split(PASSWORD_DELIMITER)[1]
    else:
        print("Key incorrect or message corrupted")
        exit(1)
    return decrypted_address_password


def encrypt(address_hash, password, master_password) -> str:
    key = PBKDF2(bytes(master_password, 'utf-8'), bytes(address_hash, 'utf-8'), 32, count=1000, hmac_hash_module=SHA512)
    cipher = AES.new(bytes(key), AES.MODE_EAX)
    nonce = cipher.nonce  # 16 bytes
    ciphertext = cipher.encrypt(pad(bytes(address_hash + PASSWORD_DELIMITER + password, 'utf-8'), 512, style='iso7816'))
    ciphertext = nonce + ciphertext
    return ciphertext
