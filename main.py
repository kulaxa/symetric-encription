import sys

from utils.crypto_utils import check_num_args
from utils.database_utils import init_database, put_in_database, get_from_database

if sys.argv[1] == 'init':
    check_num_args(sys.argv, 3)
    master_password = sys.argv[2]
    if init_database(master_password):
        print("Initialized database with master password")

if sys.argv[1] == 'put':
    check_num_args(sys.argv, 5)
    master_password = sys.argv[2]
    address = sys.argv[3]
    password = sys.argv[4]
    if put_in_database(master_password, address, password):
        print("Stored password for ", sys.argv[3])

if sys.argv[1] == 'get':
    check_num_args(sys.argv, 4)
    master_password = sys.argv[2]
    address = sys.argv[3]
    decrypted_pass = get_from_database(address, master_password)
    print("Decrypted password: ", decrypted_pass)
