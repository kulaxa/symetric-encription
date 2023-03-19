# Opis sustava za zaštitu lozinki


## Mogućnosti sustava
- U ovom sustavu moguća je inicijalizacija baze s glavnom zaporkom, dodavanje novih lozinki i dohvaćanje već postavljenih lozinki.

- Za svaku akciju potrebna je glavna šifra koja se postavlja pri inicijalizaciji.
### Inicijalizacija
```bash
python3 main.py init <masterPassword>
```
### Spremanje lozinke
```bash
python3 main.py put <masterPassword> <adresa> <lozinka>
```
### Dohvaćanje lozinki
```bash
python3 main.py get <masterPassword> <adresa>
```
## Opis baze
- Sustav koristi redis bazu za spremanje podataka kao parove ključeva i vrijednosti.

- Ključevi su sažete adrese, a vrijednosti enkriptirane lozinke.

- Redis omogućuje korištenje ovoga sustava s velikim brojem lozinki gdje je svaka enkriptirana svojim ključem, a dohvaćanje lozinka se odvija u `O(1)` (konstantnom) vremenu.

## Generiranje ključa i enkripcija

### Generiranje ključa
- Svaka lozinka u ovom sustavu je enkriptirana zasebnim ključem koji se generira na temelju njezine **adrese**, **glavne lozinke** i **inicijalizacijskog vektora**.

- Kod generiranje ključa koristi se  adresa lozinke zato da nije moguće dekriptirati lozinku samo na temelju glavne lozinke.

- Inicijalizacijski vektor osigurava da ekriptirana lozinka uvijek bude različita makar se radi o istoj lozinki i adresi. On se nadodaje na početak enkripirane lozinke i kod dekriptiranja se opet koristi da generiranje ključa.

```python
key = PBKDF2(bytes(master_password, 'utf-8'), bytes(address_hash, 'utf-8'), 32, count=1000, hmac_hash_module=SHA512)
```
### Enkripcija
- Enkripcija se radi na način da prvo spojimo adresu i lozinku s nekim razdvojnim znakom (ovdje se koristi `:`) i onda je proširimo do 512 bajtova i onda pomoću generiranog ključa enkriptiramo taj par adrese i lozinke.

- U ovom sustavu uz lozinku enkriptiramo i adresu da bi kasnije mogli provjeriti radi li se o lozinki za točno tu adresu koju je korisnik zatražio.

- Produljavanje zakriptiranog stringa se radi zbog toga da sve lozinke u bazi budu iste duljine i onda da nije moguće dobiti ikakve informacije o duljinama lozinki.

```python
ciphertext = cipher.encrypt(pad(bytes(address_hash + PASSWORD_DELIMITER + password, 'utf-8'), 512, style='iso7816'))
```

### Sažetak adrese
- U sustavu nije moguće doći do ikakvih informacija o adresama zato jer su samo spremljeni samo sažetci adresa.

- Dovoljno je spremati samo sažetke adresa zato jer uvijek možemo doći do sažetka adrese koju je korisnik zatražio.
```python
hash_address = SHA256.new(data=bytes(address, 'utf-8')).hexdigest()
```

### Provjera glavne lozinke
- Glavna lozinka nije nigdje pohranjena tako da nije moguće doći do nje iz podataka u bazi.

- To je ostvareno na način da se pri inicijalizaciji baze stvara jedna unaprijed određena adresa i lozinka na kojima je provedena enkripcija.

- Svaki puta kada se za bilo što koristi glavna zaporka sustav prvo proba dekriptirati tu unaprijed određenu adresu (za koju je naravno potrebna točna glavna lozinka) i ako uspije onda je glavna lozinka ispravna, inače nije.