import sys
from Crypto.Hash import SHA256
from crypto_utils import *
from properties import *

if sys.argv[1] == 'init':
    check_num_args(sys.argv, 3)
    master_password = sys.argv[2]
    hash_address = SHA256.new(data=bytes(INIT_ADDRESS, 'utf-8')).hexdigest()
    ciphertext = encrypt(hash_address, INIT_PASSWORD, master_password)
    r.flushall()
    r.set(hash_address, ciphertext)
    print("Initialized database with master password")

if sys.argv[1] == 'put':
    check_num_args(sys.argv, 5)
    master_password = sys.argv[2]
    address = sys.argv[3]
    password = sys.argv[4]
    hash_address = SHA256.new(data=bytes(address, 'utf-8')).hexdigest()
    if check_master_password(master_password):
        ciphertext = encrypt(hash_address, password, master_password);
        r.set(hash_address, ciphertext)
        print("Stored password for ", sys.argv[3])
    else:
        print("Wrong master password provided! Or database not initialized!")
        exit(1)

if sys.argv[1] == 'get':
    check_num_args(sys.argv, 4)
    master_password = sys.argv[2]
    address = sys.argv[3]
    hash_address = SHA256.new(data=bytes(address, 'utf-8')).hexdigest()
    if check_master_password(master_password):
        if r.exists(hash_address) == 0:
            print("No password stored for ", address)
            exit(1)
        decrypted_pass = decrypt(hash_address, r.get(hash_address), master_password)
        print("Decrypted password: ", str(decrypted_pass, 'utf-8'))
    else:
        print("Wrong master password provided! Or database not initialized!")
        exit(1)
