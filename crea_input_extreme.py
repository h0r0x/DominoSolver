import random

def genera_tessere(num_tessere, max_valore=9):
    """Genera una lista di tessere di domino con valori casuali."""
    return [[random.randint(1, max_valore) for _ in range(3)] for _ in range(num_tessere)]

def assegna_difficoltà(id_istanza):
    """Restituisce 'extreme' per tutte le istanze."""
    return 'extreme'

def calcola_parametri_difficoltà(id_istanza):
    """Calcola numero di tessere e n in base all'ID per incrementare la difficoltà."""
    base_tessere = 15  # Numero base di tessere per le istanze extreme
    incremento_tessere = id_istanza * 2  # Incremento basato sull'ID
    
    base_n = 15  # Valore base di n per le istanze extreme
    incremento_n = id_istanza * 2  # Incremento basato sull'ID
    
    num_tessere = base_tessere + incremento_tessere
    n = base_n + incremento_n
    
    return num_tessere, n

def crea_istanze_extreme_e_salva(num_istanze, file_path):
    with open(file_path, 'w') as file:
        file.write("id,difficoltà,tessere,n\n")  # Scrive l'intestazione del file
        for id_istanza in range(1, num_istanze + 1):
            difficoltà = assegna_difficoltà(id_istanza)
            num_tessere, n = calcola_parametri_difficoltà(id_istanza)
            
            tessere = genera_tessere(num_tessere)
            # Formatta la riga da salvare
            file.write(f'{id_istanza},{difficoltà},"{tessere}",{n}\n')

for i in range(5):

    # Percorso del file in cui salvare le istanze
    file_path = f'input_extreme/extreme_input_incremental_{i}.txt'

    # Genera le istanze extreme e le salva nel file specificato
    crea_istanze_extreme_e_salva(10, file_path)

    # Restituisce il percorso del file per consentire il download
    file_path
