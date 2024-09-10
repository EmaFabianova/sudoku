import pygame
import sys
from random import sample
import copy

pygame.init()

#rozmery okna
sirka = 700
vyska = 540
velkost_mriezky = 540
mriezka = 9
velkost_okna = velkost_mriezky // mriezka
velkost_tlacidla = 60
medzera = 10 
vyske_textoveho_tlacidla = 40  # Výška tlačidiel s textom
sirka_textoveho_tlacidla = 130  # Šírka tlačidiel s textom



obrazovka = pygame.display.set_mode((sirka, vyska))
pygame.display.set_caption("Sudoku")

# Fonty
font = pygame.font.SysFont(None, 40)
button_font = pygame.font.SysFont(None, 30)
text_button_font = pygame.font.SysFont(None, 25)


# Základná veľkosť pre Sudoku 
zaklad = 3
strana = zaklad * zaklad
uroven=6


aktualne_cislo = None

def nakresli_mriezku():
    for riadok in range(mriezka + 1):
        hrubka = 1 if riadok % 3 != 0 else 3
        pygame.draw.line(obrazovka, 'black', (0, riadok * velkost_okna) , (velkost_mriezky, riadok * velkost_okna ), hrubka)
        pygame.draw.line(obrazovka, 'black', (riadok * velkost_okna, 0), (riadok * velkost_okna, velkost_mriezky), hrubka)

def nakresli_tlacidla(aktualne_cislo=None):
    obdlzniky_tlacidiel = []
    texty_tlacidiel = [str(i) for i in range(1, 10)] + ["X", "Nové Sudoku", "Doplň","Zadať","Vyriešiť" ]

    # Rozmery tlačidiel s číslami
    sirka_tlacidla = velkost_tlacidla
    vyska_tlacidla = velkost_tlacidla
    medzi_tlacidla = 9 # Medzera medzi tlačidlami

    # Vykreslenie tlačidiel s číslami
    for i in range(10):
        stlpec = i % 2
        riadok = i // 2
        obdlznik = pygame.Rect(velkost_mriezky + medzera + stlpec * (sirka_tlacidla + medzi_tlacidla),
                               riadok * (vyska_tlacidla + medzi_tlacidla), sirka_tlacidla, vyska_tlacidla)
        obdlzniky_tlacidiel.append(obdlznik)

        # Zmeniť farbu tlačidla, ak je aktuálne vybrané
        
        if i < 9:
            farba = 'green' if i + 1 == aktualne_cislo else 'gray'
        elif i == 9: 
            farba = 'green' if aktualne_cislo == 0 else 'gray'
        else:
            farba = 'gray'
        pygame.draw.rect(obrazovka, farba, obdlznik)
        pygame.draw.rect(obrazovka, 'black', obdlznik, 2)

        textovy_povrch = button_font.render(texty_tlacidiel[i], True, 'black')
        textovy_obdlznik = textovy_povrch.get_rect(center=obdlznik.center)
        obrazovka.blit(textovy_povrch, textovy_obdlznik)

    # Vykreslenie tlačidiel s textom
    for i, text in enumerate(texty_tlacidiel[10:], 10):
        obdlznik = pygame.Rect(velkost_mriezky + medzera,
                               vyska - (i - 10) * (vyske_textoveho_tlacidla + medzi_tlacidla) - vyske_textoveho_tlacidla - medzera ,
                               sirka_textoveho_tlacidla, vyske_textoveho_tlacidla)
        obdlzniky_tlacidiel.append(obdlznik)
        pygame.draw.rect(obrazovka, 'gray', obdlznik)
        pygame.draw.rect(obrazovka, 'black', obdlznik, 2)
        textovy_povrch = text_button_font.render(text, True, 'black')
        textovy_obdlznik = textovy_povrch.get_rect(center=obdlznik.center)
        obrazovka.blit(textovy_povrch, textovy_obdlznik)

    return obdlzniky_tlacidiel

def zamiesaj(s):
    return sample(s, len(s))

# Funkcia na výpočet vzoru pre vyplnenie Sudoku mriežky
def vzor(riadok, stlpec):
    return (zaklad * (riadok % zaklad) + riadok // zaklad + stlpec) % strana

# vyriesene sudoku 
def sudoku_cisla():
    zakladne_riadky = range(zaklad)
    zamiesane_riadky = []
    for i in zamiesaj(zakladne_riadky):
        for j in zamiesaj(zakladne_riadky):
            zamiesane_riadky.append(i * zaklad + j)
    zamiesane_stlpce = []
    for a in zamiesaj(zakladne_riadky):
        for b in zamiesaj(zakladne_riadky):
            zamiesane_stlpce.append(a * zaklad + b)
    cisla = zamiesaj(range(1, strana + 1))
    mriezka = []
    for r in zamiesane_riadky:
        riadok = []
        for s in zamiesane_stlpce:
            riadok.append(cisla[vzor(r, s)])
        mriezka.append(riadok)
    return mriezka
# zobrazenie cisel
def zobraz_cisla(mriezka, sudoku, obsadene, vyriesene_sudoku):
    for riadok in range(mriezka):
        for stlpec in range(mriezka):
            hodnota = sudoku[riadok][stlpec]
            if hodnota != 0:  # Ak nie je prázdne miesto
                # Ak je políčko obsadené, farba bude modrá, inak čierna
                if (riadok, stlpec) in obsadene:
                    farba = 'blue'
                elif hodnota!=vyriesene_sudoku[riadok][stlpec]:
                   farba= 'red'
                else:
                    farba='black'
                textovy_povrch = font.render(str(hodnota), True, farba)
                textovy_obdlznik = textovy_povrch.get_rect(center=(stlpec * velkost_okna + velkost_okna // 2, riadok * velkost_okna + velkost_okna // 2))
                obrazovka.blit(textovy_povrch, textovy_obdlznik)

# zobrazi par cisel, ostatne da na 0, toto je zadanie
def vybrane_cisla(sudoku):
    pocet_okienok = strana * strana
    prazdne = pocet_okienok * 3 // uroven
    for i in sample(range(pocet_okienok), prazdne):
        sudoku[i // strana][i % strana] = 0

#policka, ktore su na zaciatku obsadene
def obsadene_policka(sudoku):
    obsadene = []
    for y in range(len(sudoku)):
        for x in range(len(sudoku[y])):
            if sudoku[y][x] != 0:
                obsadene.append((y, x))
    return obsadene

def je_obsadena(sudoku, obsadene_policka, x, y):
    for bunka in obsadene_policka:
        if x==bunka[1] and y==bunka[0]: # x je stlpec, y je riadok
            return True
    return False

def nastav_bunku(sudoku, x, y, hodnota):
    sudoku[y][x] = hodnota

def kliknutie(sudoku, obsadene_policka, x, y, aktualne_cislo):
    if x <= 540:
        sudoku_x, sudoku_y = x // 60, y // 60
        if not je_obsadena(sudoku, obsadene_policka, sudoku_x, sudoku_y):
            nastav_bunku(sudoku, sudoku_x, sudoku_y, aktualne_cislo)

def dopln_cislo(sudoku, vyriesene_sudoku, obsadene, x, y):
    sudoku_x, sudoku_y = x // 60, y // 60
    if not je_obsadena(sudoku, obsadene, sudoku_x, sudoku_y):
        sudoku[sudoku_y][sudoku_x] = vyriesene_sudoku[sudoku_y][sudoku_x]

def je_sudoku_spravne(sudoku):
    # Počet zadaných čísel
    pocet_cisiel = sum(1 for riadok in sudoku for hodnota in riadok if hodnota != 0)
    if pocet_cisiel < 17:
        print(f"Počet zadaných čísel je {pocet_cisiel}, má byť aspoň 17.")
        return False

    # Skontroluj riadky
    for riadok in sudoku:
        # Ignorovať nuly pri kontrole duplicít
        if len(set(hodnota for hodnota in riadok if hodnota != 0)) != len([hodnota for hodnota in riadok if hodnota != 0]):
            print(f"V riadku {riadok} sú duplicitné čísla.")
            return False

    # Skontroluj stĺpce
    for stlpec in range(9):
        # Ignorovať nuly pri kontrole duplicít
        if len(set(sudoku[riadok][stlpec] for riadok in range(9) if sudoku[riadok][stlpec] != 0)) != len([sudoku[riadok][stlpec] for riadok in range(9) if sudoku[riadok][stlpec] != 0]):
            print(f"V stĺpci {stlpec} sú duplicitné čísla.")
            return False

    # Skontroluj bloky 3x3
    for start_riadok in range(0, 9, 3):
        for start_stlpec in range(0, 9, 3):
            blok = [sudoku[r][c] for r in range(start_riadok, start_riadok + 3)
                                  for c in range(start_stlpec, start_stlpec + 3) if sudoku[r][c] != 0]
            if len(set(blok)) != len(blok):
                print(f"V bloku {start_riadok//3},{start_stlpec//3} sú duplicitné čísla.")
                return False

    return True

def je_bezpecne(sudoku, riadok, stlpec, cislo):
    for i in range(9):
        if sudoku[riadok][i] == cislo or sudoku[i][stlpec] == cislo:
            return False

    start_riadok, start_stlpec = 3 * (riadok // 3), 3 * (stlpec // 3)
    for i in range(3):
        for j in range(3):
            if sudoku[start_riadok + i][start_stlpec + j] == cislo:
                return False

    return True

def najdi_najlepsiu_poziciu(sudoku):
    najlepsie_pole = None
    najmenej_moznosti = 10  
    
    for riadok in range(9):
        for stlpec in range(9):
            if sudoku[riadok][stlpec] == 0:
                moznosti = [cislo for cislo in range(1, 10) if je_bezpecne(sudoku, riadok, stlpec, cislo)]
                if len(moznosti) < najmenej_moznosti:
                    najmenej_moznosti = len(moznosti)
                    najlepsie_pole = (riadok, stlpec)
                    
    return najlepsie_pole

def riesenie_sudoku(sudoku):
    naj_pozicia = najdi_najlepsiu_poziciu(sudoku)
    if not naj_pozicia:
        return True   

    riadok, stlpec = naj_pozicia
    for cislo in range(1, 10):
        if je_bezpecne(sudoku, riadok, stlpec, cislo):
            sudoku[riadok][stlpec] = cislo
            if riesenie_sudoku(sudoku):
                return True
            sudoku[riadok][stlpec] = 0  

    return False
 
def hlavna():
    running = True
    sudoku = [[0 for _ in range(mriezka)] for _ in range(mriezka)]
    vyriesene_sudoku = None
    obdlzniky_tlacidiel = nakresli_tlacidla()
    obsadene = obsadene_policka(sudoku)
    aktualne_cislo = None
    dopln_aktivne = False
    zadavanie = False  

    while running:
        obrazovka.fill('white')
        nakresli_mriezku()

        if vyriesene_sudoku:
            zobraz_cisla(mriezka, sudoku, obsadene, vyriesene_sudoku)
        else:
            zobraz_cisla(mriezka, sudoku, obsadene, [[0]*mriezka for _ in range(mriezka)])

        obdlzniky_tlacidiel = nakresli_tlacidla(aktualne_cislo)
        
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                running = False
            elif udalost.type == pygame.MOUSEBUTTONDOWN:
                pozicia_mysi = pygame.mouse.get_pos()

                if pozicia_mysi[0] <= 540:  # Kliknutie do mriežky
                    if zadavanie and aktualne_cislo is not None:
                        sudoku_x, sudoku_y = pozicia_mysi[0] // velkost_okna, pozicia_mysi[1] // velkost_okna
                        nastav_bunku(sudoku, sudoku_x, sudoku_y, aktualne_cislo)
                    elif dopln_aktivne:
                        dopln_cislo(sudoku, vyriesene_sudoku, obsadene, pozicia_mysi[0], pozicia_mysi[1])
                        dopln_aktivne = False
                    elif aktualne_cislo is not None:
                        kliknutie(sudoku, obsadene, pozicia_mysi[0], pozicia_mysi[1], aktualne_cislo)

                for i, obdlznik in enumerate(obdlzniky_tlacidiel):
                    if obdlznik.collidepoint(pozicia_mysi):
                        if i < 9:
                            aktualne_cislo = i + 1
                        elif i == 9:  # Tlačidlo "X" na vymazanie
                            aktualne_cislo = 0
                        elif i == 10:  # "Nové Sudoku"
                            vyriesene_sudoku = sudoku_cisla()
                            sudoku = copy.deepcopy(vyriesene_sudoku)
                            vybrane_cisla(sudoku)
                            obsadene = obsadene_policka(sudoku)
                            aktualne_cislo = None
                        elif i == 11:  # "Doplň"
                            dopln_aktivne = True
                            aktualne_cislo = None
                        elif i == 12:  # "Zadať"
                            zadavanie = True
                            vyriesene_sudoku = None
                            sudoku = [[0 for _ in range(mriezka)] for _ in range(mriezka)]
                            obsadene = []
                            aktualne_cislo = None
                        elif i == 13:  # "Vyriešiť"
                            zadavanie = False
                            vyriesene_sudoku = copy.deepcopy(sudoku)
                            if je_sudoku_spravne(vyriesene_sudoku):
                                # Riešenie Sudoku, ak je správne zadané
                                if riesenie_sudoku(vyriesene_sudoku):
                                    sudoku = copy.deepcopy(vyriesene_sudoku)
                                    obsadene = obsadene_policka(sudoku)
                                else:
                                    print('riesenie zlyhalo')
                            else:
                                # Zobrazovanie správy, ak Sudoku nie je správne
                                print("Sudoku je zadané nesprávne alebo neobsahuje aspoň 17 čísel.")
                            aktualne_cislo = None
        pygame.display.flip()

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    hlavna()
