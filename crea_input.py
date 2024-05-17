import random
import os

def genera_tessere(num_tessere, max_valore):
    """Genera una lista di tessere di domino con valori casuali."""
    return [[random.randint(1, max_valore) for _ in range(3)] for _ in range(num_tessere)]

def assegna_difficoltà(id_istanza):
    """Assegna la difficoltà in base all'ID dell'istanza."""
    if 1 <= id_istanza <= 4:
        return 'easy'
    elif 5 <= id_istanza <= 8:
        return 'medium'
    else:  # hard
        return 'hard'

def crea_istanze_e_salva(num_istanze, file_path):
    with open(file_path, 'w') as file:
        file.write("id,difficoltà,tessere,n\n")  # Scrive l'intestazione del file
        for id_istanza in range(1, num_istanze + 1):
            difficoltà = assegna_difficoltà(id_istanza)
            # Aumenta il numero di tessere in base alla difficoltà
            if difficoltà == 'easy':
                num_tessere = random.randint(2, 6)
                max_valore = random.randint(3, 6)
                n = random.randint(2, 5)
            elif difficoltà == 'medium':
                num_tessere = random.randint(6, 10)
                max_valore = random.randint(3, 10)
                n = random.randint(6, 10)
            else:  # hard
                num_tessere = random.randint(10, 20)
                max_valore = random.randint(3, 15)
                n = random.randint(10, 20)
                
            tessere = genera_tessere(num_tessere,max_valore)
            
            # Formatta la riga da salvare
            file.write(f'{id_istanza},{difficoltà},"{tessere}",{n}\n')

def genera_e_salva_vari_input(num_input, cartella):
    # Assicurati che la cartella esista
    if not os.path.exists(cartella):
        os.makedirs(cartella)
    
    # Genera i file di input
    for i in range(1, num_input + 1):
        file_path = os.path.join(cartella, f'input{i}.txt')
        n_istanze = 10  # Numero di istanze per file
        crea_istanze_e_salva(n_istanze, file_path)  # Assumi che ogni file abbia 10 istanze

# Chiamata alla funzione per generare 10 file di input nella cartella "input/"
genera_e_salva_vari_input(10, "input/")
