import sqlite3
import hashlib
import tkinter as tk

# Opprett en tilkobling til databasen
conn = sqlite3.connect("brukere.db")

# Opprett en peker til databasen
c = conn.cursor()

# Opprett en funksjon for å kryptere passordet
def krypter_passord(passord):
    hash_object = hashlib.sha256(passord.encode())
    kryptert_passord = hash_object.hexdigest()
    return kryptert_passord

# Opprett en funksjon for å registrere en ny bruker i databasen
def registrer():
    # Hent verdien fra inndatafeltene
    brukernavn = brukernavn_felt.get()
    passord = passord_felt.get()
    kryptert_passord = krypter_passord(passord)
    email = email_felt.get()

    # Legg inn brukeren i databasen
    c.execute("INSERT INTO brukere (brukernavn, passord, email) VALUES (?, ?, ?)", (brukernavn, kryptert_passord, email))
    conn.commit()

    # Nullstill inndatafeltene
    brukernavn_felt.delete(0, tk.END)
    passord_felt.delete(0, tk.END)
    email_felt.delete(0, tk.END)

# Opprett en funksjon for å logge inn en bruker
def logg_inn():
    # Hent verdien fra inndatafeltene
    brukernavn = brukernavn_felt.get()
    passord = passord_felt.get()
    kryptert_passord = krypter_passord(passord)

    # Sjekk om brukernavn og passord finnes i databasen
    c.execute("SELECT * FROM brukere WHERE brukernavn = ? AND passord = ?", (brukernavn, kryptert_passord))
    bruker = c.fetchone()

    if bruker:
        # Vis statusmelding for vellykket innlogging
        status_melding.config(text="Du er nå logget inn!")
    else:
        # Vis feilmelding for mislykket innlogging
        status_melding.config(text="Feil brukernavn eller passord")

    # Nullstill inndatafeltene
    brukernavn_felt.delete(0, tk.END)
    passord_felt.delete(0, tk.END)

# Opprett en funksjon for å fjerne en bruker fra databasen
def fjern_bruker():
    # Hent verdien fra inndatafeltet for brukernavn
    brukernavn = brukernavn_felt.get()

    # Fjern brukeren fra databasen
    c.execute("DELETE FROM brukere WHERE brukernavn = ?", (brukernavn,))
    conn.commit()

    # Nullstill inndatafeltene
    brukernavn_felt.delete(0, tk.END)
    passord_felt.delete(0, tk.END)
    email_felt.delete(0, tk.END)

# Opprett et tkinter-vindu
root = tk.Tk()

# Opprett inndatafelt for brukernavn, passord og e-post
brukernavn_label = tk.Label(root, text="Brukernavn:")
brukernavn_label.pack()

brukernavn_felt = tk.Entry(root)
brukernavn_felt.pack()

passord_label = tk.Label(root, text="Passord:")
passord_label.pack()

passord_felt = tk.Entry(root, show="*")
passord_felt.pack()

email_label = tk.Label(root, text="E-post:")
email_label.pack()

email_felt = tk.Entry(root)
email_felt.pack()

# Opprett en knapp for å registrere en ny bruker
registrer_knapp = tk.Button(root, text="Registrer", command=registrer)
registrer_knapp.pack()

# Opprett en knapp for å logge inn en bruker
logg_inn_knapp = tk.Button(root, text="Logg inn", command=logg_inn)
logg_inn_knapp.pack()

# Opprett en knapp for å fjerne en bruker
fjern_bruker_knapp = tk.Button(root, text="Fjern bruker", command=fjern_bruker)
fjern_bruker_knapp.pack()

# Opprett en statusmelding
status_melding = tk.Label(root, text="")
status_melding.pack()

# Start tkinter-løkken
root.mainloop()