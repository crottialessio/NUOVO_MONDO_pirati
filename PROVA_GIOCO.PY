import random
from collections import Counter

# --- CONFIGURAZIONE E COSTANTI ---
RUOLI = {
    "cuoco":      {"paga_settimanale": 15},
    "marinaio":   {"paga_settimanale": 10},
    "meccanico":  {"paga_settimanale": 15},
    "medico":     {"paga_settimanale": 25},
    "navigatore": {"paga_settimanale": 20},
}

QTA_DA_PERDERE = [0.5, 0.33, 0.25, 0.2]

stato_gioco = {
    "monete": 2000,
    "equipaggio": {},
    "prossimo_id": 1,
    "equipaggiamento": {
        "verdura": {"qta": 100, "prezzo": 0.5},
        "acqua": {"qta": 100, "prezzo": 0.5},
        "carne": {"qta": 100, "prezzo": 0.5},
        "frutta": {"qta": 100, "prezzo": 0.5},
        "medicinali": {"qta": 100, "prezzo": 0.5},
        "armi": {"qta": 100, "prezzo": 0.5},
        "stoffe": {"qta": 100, "prezzo": 0.5},
    }
}

# --- FUNZIONI DI GESTIONE EQUIPAGGIO ---
def crea_membro(ruolo):
    return {
        "ruolo": ruolo,
        "paga_settimanale": RUOLI[ruolo]["paga_settimanale"],
        "morale": 100,
        "vivo": True
    }

def aggiungi_membro(ruolo):
    id_ = stato_gioco["prossimo_id"]
    stato_gioco["equipaggio"][id_] = crea_membro(ruolo)
    stato_gioco["prossimo_id"] += 1

def conteggio_ruoli():
    ruoli_membri = [m["ruolo"] for m in stato_gioco["equipaggio"].values() if m["vivo"]]
    conteggio = Counter(ruoli_membri)
    return {r: conteggio.get(r, 0) for r in RUOLI}

def stampa_stato():
    c = conteggio_ruoli()
    n = sum(c.values())
    print(f"\n  Equipaggio: {n}/16")
    for ruolo, quanti in c.items():
        stato = "✓" if quanti > 0 else "✗ MANCANTE"
        print(f"    {ruolo.capitalize():<12} x{quanti}  {stato}")

def input_intero(prompt, minimo=None, massimo=None):
    try:
        val = int(input(prompt))
        if (minimo is not None and val < minimo) or (massimo is not None and val > massimo):
            raise ValueError
        return val
    except ValueError:
        print(f"  Inserisci un numero valido (min {minimo}, max {massimo}).")
        return input_intero(prompt, minimo, massimo)

# --- FUNZIONI EVENTI ---
def prova_unica(oggetto):
    qta_persa_perc = random.choice(QTA_DA_PERDERE)
    peso_perso = stato_gioco["equipaggiamento"][oggetto]["qta"] * qta_persa_perc
    stato_gioco["equipaggiamento"][oggetto]["qta"] -= peso_perso
    return round(peso_perso, 2)

def tempesta_miracolosa(oggetto):
    qta_guadagnata = random.randint(11, 20)
    stato_gioco["equipaggiamento"][oggetto]["qta"] += qta_guadagnata
    return qta_guadagnata

def raffiche_di_vento(ruolo_richiesto, durata_attuale):
    presenza_ruolo = any(m["ruolo"] == ruolo_richiesto and m["vivo"] for m in stato_gioco["equipaggio"].values())
    
    if presenza_ruolo:
        return 1, durata_attuale + 1, True
    else:
        sett_casuale = random.randint(2, 4)
        return sett_casuale, durata_attuale + sett_casuale, False

def uomo_in_mare():
    vivi = [id_ for id_, m in stato_gioco["equipaggio"].items() if m["vivo"]]
    if not vivi:
        return "Nessuno (tutti deceduti)"
    morto_id = random.choice(vivi)
    stato_gioco["equipaggio"][morto_id]["vivo"] = False
    return stato_gioco["equipaggio"][morto_id]["ruolo"].upper()

# --- FASI DI GIOCO ---
def fase_ingaggio():
    print("\n" + "="*30 + "\nINGAGGIO DELLA FLOTTA\n" + "="*30)
    while True:
        stampa_stato()
        c = conteggio_ruoli()
        n = sum(c.values())
        ruoli_mancanti = [r for r in RUOLI if c[r] == 0]
        puo_salpare = (n >= 5 and not ruoli_mancanti)

        print("\n1) Aggiungi membri")
        if puo_salpare:
            print("2) Salpa!")
        else:
            mancanti = ", ".join(ruoli_mancanti) if ruoli_mancanti else f"almeno 5 persone ({n}/5)"
            print(f"2) Salpa! (Mancano: {mancanti})")

        scelta = input_intero("Scelta: ", 1, 2)
        if scelta == 2 and puo_salpare:
            break
        elif scelta == 2:
            print("Non puoi ancora salpare!")
            continue

        if n >= 16:
            print("Limite massimo raggiunto!")
            continue

        print("\nScegli ruolo:")
        ruoli_lista = list(RUOLI.keys())
        for i, r in enumerate(ruoli_lista, 1):
            print(f"  {i}) {r.capitalize()}")
        
        r_scelta = input_intero("Ruolo (0 per annullare): ", 0, len(ruoli_lista))
        if r_scelta > 0:
            ruolo_selezionato = ruoli_lista[r_scelta-1]
            quanti = input_intero(f"Quanti {ruolo_selezionato}? (max {16-n}): ", 1, 16-n)
            for _ in range(quanti):
                aggiungi_membro(ruolo_selezionato)

def fase_viaggio():
    print("\n" + "="*30 + "\nINIZIO DEL VIAGGIO\n" + "="*30)
    settimana = 1
    durata_viaggio = 8 # Settimane iniziali stimata [cite: 5, 17]

    while settimana <= durata_viaggio:
        input(f"\n[INVIO] per iniziare la SETTIMANA {settimana} di {durata_viaggio}...")
        n_evento = random.randint(0, 12) 

        if n_evento == 0:
            morto = uomo_in_mare()
            print(f"--- EVENTO UOMO IN MARE --- \nIl {morto} è caduto in mare ed è MORTO!")
        elif n_evento == 1:
            p = prova_unica("verdura")
            print(f"--- EVENTO TEMPESTA --- \nPerse {p} Kg di VERDURE in mare.")
        elif n_evento == 2:
            p = prova_unica("frutta")
            print(f"--- EVENTO TEMPESTA --- \nPerse {p} Kg di FRUTTA in mare.")
        elif n_evento == 3:
            p = prova_unica("carne")
            print(f"--- EVENTO TEMPESTA --- \nPerse {p} Kg di CARNE in mare.")
        elif n_evento == 4:
            p = prova_unica("acqua")
            print(f"--- EVENTO TEMPESTA --- \nPersi {p} BARILI d'ACQUA.")
        elif n_evento == 5:
            g = tempesta_miracolosa("carne")
            print(f"Settimana di quiete: pescati {g} kg di CARNE!")
        elif n_evento == 6:
            g = tempesta_miracolosa("acqua")
            print(f"Pioggia abbondante: riempiti {g} BARILI d'ACQUA!")
        elif n_evento == 8:
            p = prova_unica("medicinali")
            print(f"--- CATTIVO TEMPO --- \nSi sono rotte {p} bottiglie di MEDICINALI.")
        elif n_evento == 9:
            p = prova_unica("armi")
            print(f"--- ONDATA ANOMALA --- \nTrasportate in mare {p} ARMI.")
        elif n_evento == 10:
            p = prova_unica("stoffe")
            print(f"--- RATTI A BORDO --- \nI ratti hanno rovinato {p} STOFFE.")
        elif n_evento == 11:
            extra, durata_viaggio, riparato = raffiche_di_vento("meccanico", durata_viaggio)
            msg = "GRAZIE AL MECCANICO riparato in fretta." if riparato else "ASSENZA MECCANICO: riparazione lenta."
            print(f"--- DANNI AL TIMONE --- \nViaggio allungato di {extra} settimane. {msg}")
        elif n_evento == 12:
            extra, durata_viaggio, risolto = raffiche_di_vento("navigatore", durata_viaggio)
            msg = "GRAZIE AL NAVIGATORE rotta ripresa." if risolto else "ASSENZA NAVIGATORE: siamo persi."
            print(f"--- FORTI RAFFICHE --- \nViaggio allungato di {extra} settimane. {msg}")
        else:
            print("Settimana tranquilla, i venti sono favorevoli.")

        settimana += 1

    print("\n" + "="*30 + "\nSIETE ARRIVATI AL NUOVO MONDO!\n" + "="*30)

# --- AVVIO GIOCO ---
if __name__ == "__main__":
    fase_ingaggio()
    fase_viaggio()