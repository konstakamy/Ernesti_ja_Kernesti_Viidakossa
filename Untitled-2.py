import random
import tkinter as tk
from tkinter import messagebox

# Matriisin koko
MATRIISI_KOKO = 10  # Vaihdettu 100 -> 10
leijona_pudotettu = False  # Tieto siitä, onko leijona pudotettu

def laske_etaisyys(piste1, piste2):
    """Laskee Manhattan-etäisyyden kahden pisteen välillä."""
    x1, y1 = piste1
    x2, y2 = piste2
    return abs(x1 - x2) + abs(y1 - y2)

def siirra(hahmo):
    """Liikuttaa hahmoa satunnaisesti suuntaan: ylös, alas, vasen tai oikea."""
    x, y = hahmo["sijainti"]
    suunta = random.choice(["ylös", "alas", "vasen", "oikea"])

    if suunta == "ylös" and x > 0:
        hahmo["sijainti"] = (x - 1, y)
    elif suunta == "alas" and x < MATRIISI_KOKO - 1:
        hahmo["sijainti"] = (x + 1, y)
    elif suunta == "vasen" and y > 0:
        hahmo["sijainti"] = (x, y - 1)
    elif suunta == "oikea" and y < MATRIISI_KOKO - 1:
        hahmo["sijainti"] = (x, y + 1)

def siirra_leijona(leijona, ernesti, kernesti):
    """Siirtää leijonaa kohti läheisintä ohjelmoijaa (Ernestiä tai Kernestiä)."""
    x_l, y_l = leijona["sijainti"]
    x_e, y_e = ernesti["sijainti"]
    x_k, y_k = kernesti["sijainti"]

    # Laske etäisyydet leijonan ja ohjelmoijien välillä
    etaisyys_ernesti = laske_etaisyys((x_l, y_l), (x_e, y_e))
    etaisyys_kernesti = laske_etaisyys((x_l, y_l), (x_k, y_k))

    # Valitse lähempi ohjelmoija
    kohde = ernesti if etaisyys_ernesti <= etaisyys_kernesti else kernesti
    x_tavoite, y_tavoite = kohde["sijainti"]

    # Liiku kohti kohdetta
    if x_l < x_tavoite and x_l < MATRIISI_KOKO - 1:
        leijona["sijainti"] = (x_l + 1, y_l)
    elif x_l > x_tavoite and x_l > 0:
        leijona["sijainti"] = (x_l - 1, y_l)
    elif y_l < y_tavoite and y_l < MATRIISI_KOKO - 1:
        leijona["sijainti"] = (x_l, y_l + 1)
    elif y_l > y_tavoite and y_l > 0:
        leijona["sijainti"] = (x_l, y_l - 1)

def tarkista_kohtaaminen(ernesti, kernesti):
    """Tarkistaa, ovatko Ernesti ja Kernesti samassa sijainnissa."""
    return ernesti["sijainti"] == kernesti["sijainti"]

def tarkista_leijona(hahmo, leijona):
    """Tarkistaa, ovatko Ernesti tai Kernesti kohdanneet leijonan."""
    return hahmo["sijainti"] == leijona["sijainti"]

def paivita_viidakko(viidakko, ernesti, kernesti, leijona):
    """Päivittää viidakkomatriisin Ernestin, Kernestin ja leijonan sijainnin perusteella."""
    for rivi in range(MATRIISI_KOKO):
        for sarake in range(MATRIISI_KOKO):
            viidakko[rivi][sarake] = 0

    x_e, y_e = ernesti["sijainti"]
    x_k, y_k = kernesti["sijainti"]
    viidakko[x_e][y_e] = 1  # Ernesti
    viidakko[x_k][y_k] = 2  # Kernesti

    # Päivitetään leijonan sijainti, jos se on pudotettu
    if leijona_pudotettu:
        x_l, y_l = leijona["sijainti"]
        viidakko[x_l][y_l] = 3  # Leijona

def paivita_naytto(canvas, viidakko):
    """Päivittää graafisen näytön (Tkinter canvas) viidakkomatriisin mukaan."""
    canvas.delete("all")
    size = 50  # Ruudun koko pikseleissä (suurempi, koska pienempi matriisi)
    for i in range(MATRIISI_KOKO):
        for j in range(MATRIISI_KOKO):
            if viidakko[i][j] == 1:
                # Ernesti (vihreä ruutu)
                canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill="green")
            elif viidakko[i][j] == 2:
                # Kernesti (sininen ruutu)
                canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill="blue")
            elif viidakko[i][j] == 3:
                # Leijona (punainen ruutu)
                canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill="red")

def aloita_liike():
    """Käynnistää liikkeen ja päivittää sijainnit kunnes Ernesti ja Kernesti kohtaavat."""
    # Pudotetaan Ernesti ja Kernesti satunnaisiin sijainteihin
    ernesti["sijainti"] = (random.randint(0, MATRIISI_KOKO - 1), random.randint(0, MATRIISI_KOKO - 1))
    kernesti["sijainti"] = (random.randint(0, MATRIISI_KOKO - 1), random.randint(0, MATRIISI_KOKO - 1))

    while ernesti["sijainti"] == kernesti["sijainti"]:
        kernesti["sijainti"] = (random.randint(0, MATRIISI_KOKO - 1), random.randint(0, MATRIISI_KOKO - 1))

    paivita_viidakko(viidakko, ernesti, kernesti, leijona)
    paivita_naytto(canvas, viidakko)

    # Aloitetaan liikkuminen
    liiku()

def liiku():
    """Liikuttaa Ernestiä, Kernestiä ja leijonaa satunnaisesti, kunnes he löytävät toisensa tai leijona nappaa ohjelmoijan."""
    siirra(ernesti)
    siirra(kernesti)
    
    # Leijona liikkuu vain, jos se on pudotettu
    if leijona_pudotettu:
        siirra_leijona(leijona, ernesti, kernesti)
    
    paivita_viidakko(viidakko, ernesti, kernesti, leijona)
    paivita_naytto(canvas, viidakko)

    # Tarkista kohtaaminen Ernestin ja Kernestin välillä
    if tarkista_kohtaaminen(ernesti, kernesti):
        messagebox.showinfo("Kohtaaminen", "Vau, onpa mukava nähdä taas!")
    # Tarkista kohtaako leijona Ernestin tai Kernestin
    elif tarkista_leijona(ernesti, leijona) or tarkista_leijona(kernesti, leijona):
        messagebox.showinfo("Leijona", "Slurps, olipa hyvä ohjelmoija!")
    else:
        # Jatketaan liikkumista sekunnin välein
        root.after(1000, liiku)

def pudota_leijona():
    """Pudottaa leijonan satunnaiseen sijaintiin."""
    global leijona_pudotettu
    leijona_pudotettu = True
    leijona["sijainti"] = (random.randint(0, MATRIISI_KOKO - 1), random.randint(0, MATRIISI_KOKO - 1))
    paivita_viidakko(viidakko, ernesti, kernesti, leijona)
    paivita_naytto(canvas, viidakko)

# Luodaan 10x10 matriisi, jossa kaikki arvot ovat aluksi nollia
viidakko = [[0 for _ in range(MATRIISI_KOKO)] for _ in range(MATRIISI_KOKO)]

# Luodaan sanakirjat Ernestille, Kernestille ja leijonalle
ernesti = {
    "nimi": "Ernesti",
    "sijainti": (0, 0)  # Alustetaan sijainti
}

kernesti = {
    "nimi": "Kernesti",
    "sijainti": (0, 0)  # Alustetaan sijainti
}

leijona = {
    "nimi": "Leijona",
    "sijainti": (0, 0)  # Alustetaan sijainti, mutta asetetaan myöhemmin satunnaisesti
}

# Tkinter-käyttöliittymä
root = tk.Tk()
root.title("Ernesti ja Kernesti Viidakossa")

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack()

# Pudotus-painikkeet
pudotus_button = tk.Button(root, text="Pudota Ernesti ja Kernesti viidakkoon", command=aloita_liike)
pudotus_button.pack()

leijona_button = tk.Button(root, text="Pudota Leijona viidakkoon", command=pudota_leijona)
leijona_button.pack()

root.mainloop()
