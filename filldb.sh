#!/bin/bash

#!/bin/bash
NUMBER_OF_PASSWORDS_STORED=100000
MASTER_PASSWORD=master-pass
start_encrypt=`date +%s`
python3 main.py init $MASTER_PASSWORD
for (( c=0; c<=NUMBER_OF_PASSWORDS_STORED; c++ ))
do
    python3 main.py put $MASTER_PASSWORD "address-$c" "password-$c"
done
end_encrypt=`date +%s`
echo "###############################"

echo runtime_encrypt=$((end_encrypt-start_encrypt))
