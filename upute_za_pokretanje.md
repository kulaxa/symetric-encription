# Upute za pokretanje

## Python venv
1. `python3 -m venv venv`
2. `source venv/bin/activate`


## Instalacija zavisnosti
1. `pip install -r requirements.txt`
2. Potrebna je redis baza za rad aplikacije. Instalirati je prema uputstvima na [redis.io](https://redis.io/download)

## Pokretanje
### Inicijalizacija baze
1. `python3 main.py init masterpassword`


### Dodavanje zapisa
1. `python3 main.py put masterpassword adresa1 lozinka1`

### Dohvaćanje zapisa
1. `python3 main.py get masterpassword adresa1`