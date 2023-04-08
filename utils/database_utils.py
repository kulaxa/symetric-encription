from Crypto.Hash import SHA256

from utils.crypto_utils import encrypt, check_master_password, decrypt
from properties import INIT_ADDRESS, PASSWORD_DELIMITER, INIT_PASSWORD, r


def init_database(master_password):
    hash_address = SHA256.new(data=bytes(INIT_ADDRESS + PASSWORD_DELIMITER + master_password, 'utf-8')).hexdigest()
    ciphertext = encrypt(hash_address, INIT_PASSWORD, master_password)
    r.flushall()
    r.set(hash_address, ciphertext)
    return True


def put_in_database(master_password, address, password):
    if len(password) > 256:
        print("Password can't be longer than 256 characters")
        exit(1)
    if password.__contains__(PASSWORD_DELIMITER):
        print("You password can't contain ", PASSWORD_DELIMITER)
        exit(1)
    hash_address = SHA256.new(data=bytes(address + PASSWORD_DELIMITER + master_password, 'utf-8')).hexdigest()
    if address == INIT_ADDRESS:
        print("You can't use ", INIT_ADDRESS, " as address")
        exit(1)
    if check_master_password(master_password):
        ciphertext = encrypt(hash_address, password, master_password)
        r.set(hash_address, ciphertext)
        return True
    else:
        print("Wrong master password provided! Or database not initialized!")
        exit(1)


def get_from_database(address, master_password):
    hash_address = SHA256.new(data=bytes(address + PASSWORD_DELIMITER + master_password, 'utf-8')).hexdigest()
    if check_master_password(master_password):
        if r.exists(hash_address) == 0:
            print("No password stored for ", address)
            exit(1)
        decrypted_pass = decrypt(hash_address, r.get(hash_address), master_password)
        return decrypted_pass
    else:
        print("Wrong master password provided! Or database not initialized!")
        exit(1)
