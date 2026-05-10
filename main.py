import random

RUOLI = {
    "cuoco":      {"paga_settimanale": 15},
    "marinaio":   {"paga_settimanale": 10},
    "meccanico":  {"paga_settimanale": 15},
    "medico":     {"paga_settimanale": 25},
    "navigatore": {"paga_settimanale": 20},
}

CATALOGO_CIBO = {
    "verdura": {"prezzo": 0.5,  "unita": "kg", "consumo" : 0.5},
    "frutta":  {"prezzo": 1.0,  "unita": "kg", "consumo" : 1},
    "carne":   {"prezzo": 2.0,  "unita": "kg", "consumo" : 1},
    "acqua":   {"prezzo": 0.5,  "unita": "barili", "consumo" : 0.5},
}

CATALOGO_MERCI = {
    "medicinali": {"prezzo": 1.0, "unita": "bottiglie"},
    "armi":       {"prezzo": 5.0, "unita": "armi"},
    "sale":       {"prezzo": 0.5, "unita": "sacchi"},
    "stoffa":     {"prezzo": 2.0, "unita": "teli"},
    "coltelli":   {"prezzo": 0.5, "unita": "pezzi"},
    "diamanti":   {"prezzo": 1.0, "unita": "pezzi"},
}

stato_gioco = {
    "monete":       2000,
    "monete_spese": 0,
    "equipaggio":   {},
    "prossimo_id":  1,
    "cibo":         {
        "verdura": 0.0,
        "frutta":  0.0,
        "carne":   0.0,
        "acqua":   0.0,
    },
    "merci":        {
        "medicinali": 0,
        "armi":       0,
        "sale":       0,
        "stoffa":     0,
        "coltelli":   0,
        "diamanti":   0,
    },
}

def monete_disponibili():
    return stato_gioco["monete"] - stato_gioco["monete_spese"]

def crea_membro(ruolo):
    return {
        "ruolo":            ruolo,
        "paga_settimanale": RUOLI[ruolo]["paga_settimanale"],
        "morale":           100,
        "vivo":             True,
        "ingaggiato":       True,
    }

def aggiungi_membro(ruolo):
    id_ = stato_gioco["prossimo_id"]
    stato_gioco["equipaggio"][id_] = crea_membro(ruolo)
    stato_gioco["prossimo_id"] += 1

def conteggio_ruoli():
    # Sostituisce Counter: conta manualmente con un dizionario
    conteggio = {r: 0 for r in RUOLI}
    for membro in stato_gioco["equipaggio"].values():
        conteggio[membro["ruolo"]] += 1
    return conteggio
def totale_equipaggio():
    return len(stato_gioco["equipaggio"])

def paga_stimata(settimane=8):
    paghe = [m["paga_settimanale"] for m in stato_gioco["equipaggio"].values()]
    return sum(paghe) * settimane

def input_intero(prompt, minimo=None, massimo=None):
    try:
        val = int(input(prompt))
    except ValueError:
        print("  Inserisci un numero intero valido.")
        return input_intero(prompt, minimo, massimo)
    if minimo is not None and val < minimo:
        print(f"  Inserisci un valore >= {minimo}.")
        return input_intero(prompt, minimo, massimo)
    if massimo is not None and val > massimo:
        print(f"  Inserisci un valore <= {massimo}.")
        return input_intero(prompt, minimo, massimo)
    return val

def input_float(prompt, minimo=0.0):
    try:
        val = float(input(prompt))
    except ValueError:
        print("  Inserisci un numero valido.")
        return input_float(prompt, minimo)
    if val < minimo:
        print(f"  Inserisci un valore >= {minimo}.")
        return input_float(prompt, minimo)
    return val

def stampa_stato_equipaggio():
    n = totale_equipaggio()
    c = conteggio_ruoli()
    paga = paga_stimata()
    print()
    print(f"  Equipaggio: {n}/16  |  Paga stimata (8 sett.): {paga} monete")
    print()
    for ruolo, quanti in c.items():
        stato = "✓" if quanti > 0 else "✗ MANCANTE"
        print(f"    {ruolo.capitalize():<12} x{quanti}  {stato}")
    print()

def riepilogo_ingaggio():
    print()
    print("=" * 50)
    print("  EQUIPAGGIO PRONTO")
    print("=" * 50)
    stampa_stato_equipaggio()
    paga = paga_stimata()
    print(f"  Paga stimata totale: {paga} monete")
    if paga > monete_disponibili():
        print("  ⚠  La paga supera le monete! Dovrai guadagnare nel nuovo mondo.")
    print()
    input("  Premi INVIO per continuare...")

def turno_ingaggio():
    ruoli_lista = list(RUOLI.keys())
    stampa_stato_equipaggio()

    c = conteggio_ruoli()
    n = totale_equipaggio()
    ruoli_mancanti = [r for r in RUOLI if c[r] == 0]
    puo_salpare = (n >= 5 and len(ruoli_mancanti) == 0)

    print("  1) Aggiungi membri")
    if puo_salpare:
        print("  2) Prosegui")
    else:
        if ruoli_mancanti:
            mancanti_str = ""
            for r in ruoli_mancanti:
                mancanti_str += r + ", "
            mancanti_str = mancanti_str[:-2]
        else:
            mancanti_str = f"minimo 5 persone ({n}/5)"
        print(f"  2) Prosegui (non disponibile – mancano: {mancanti_str})")

    scelta = input_intero("  Scelta: ", minimo=1, massimo=2)

    if scelta == 2:
        if puo_salpare:
            riepilogo_ingaggio()
            return
        else:
            print("  Non puoi ancora proseguire.")
            turno_ingaggio()
            return

    if n >= 16:
        print("  Limite massimo raggiunto (16 persone).")
        turno_ingaggio()
        return

    print()
    print("  Scegli il ruolo:")
    for i, ruolo in enumerate(ruoli_lista, 1):
        print(f"    {i}) {ruolo.capitalize()} ({RUOLI[ruolo]['paga_settimanale']} monete/sett.)")
    print("    0) Annulla")

    scelta_ruolo = input_intero("  Ruolo: ", minimo=0, massimo=len(ruoli_lista))
    if scelta_ruolo != 0:
        ruolo_scelto = ruoli_lista[scelta_ruolo - 1]
        max_aggiungibili = 16 - n
        quanti = input_intero(
            f"  Quanti [{ruolo_scelto}]? (max {max_aggiungibili}): ",
            minimo=1,
            massimo=max_aggiungibili
        )
        for _ in range(quanti):
            aggiungi_membro(ruolo_scelto)
        print(f"  → Aggiunti {quanti} {ruolo_scelto}.")

    turno_ingaggio()

def fase_ingaggio():
    print()
    print("=" * 50)
    print("  FASE 1 – INGAGGIO DELLA FLOTTA")
    print("=" * 50)
    print()
    print(f"  Monete disponibili: {monete_disponibili()}")
    print("  Minimo 5 persone, almeno 1 per ruolo. Massimo 16.")
    print()
    print("  Paghe settimanali:")
    for ruolo, dati in RUOLI.items():
        print(f"    {ruolo.capitalize():<12} {dati['paga_settimanale']} monete/sett.")
    print()
    turno_ingaggio()



def stampa_stato_cibo():
    print()
    print("  Cibo attualmente nel carrello:")
    for nome, qty in stato_gioco["cibo"].items():
        unita = CATALOGO_CIBO[nome]["unita"]
        print(f"    {nome.capitalize():<10} {qty:.1f} {unita}")
    print(f"  Monete disponibili: {monete_disponibili():.1f}")
    print()

def turno_cibo(indice):
    nomi = list(CATALOGO_CIBO.keys())
    if indice >= len(nomi):
        return

    nome = nomi[indice]
    dati = CATALOGO_CIBO[nome]
    prezzo = dati["prezzo"]
    unita = dati["unita"]
    n_uomini = totale_equipaggio()

    consumi = {"verdura": 0.5, "frutta": 1.0, "carne": 1.0, "acqua": 0.5}
    consigliato = consumi[nome] * n_uomini * 8

    print(f"  {nome.upper()}  –  {prezzo} monete/{unita[:-1] if unita[-1]=='i' else unita}")
    print(f"  Quantità consigliata per 8 settimane: {consigliato:.1f} {unita}")
    print(f"  Monete disponibili: {monete_disponibili():.1f}")

    qty = input_float(f"  Quanti {unita} di {nome} vuoi comprare? (0 per saltare): ")
    costo = qty * prezzo

    if costo > monete_disponibili():
        print(f"  ✗ Non hai abbastanza monete (servono {costo:.1f}). Acquisto annullato.")
    else:
        stato_gioco["cibo"][nome] += qty
        stato_gioco["monete_spese"] += costo
        if qty > 0:
            print(f"  → Acquistati {qty:.1f} {unita} di {nome} per {costo:.1f} monete.")
    print()

    turno_cibo(indice + 1)

def fase_acquisto_cibo():
    print()
    print("=" * 50)
    print("  FASE 2 – ACQUISTO DEL CIBO")
    print("=" * 50)
    print()
    print(f"  Equipaggio: {totale_equipaggio()} persone  |  Durata stimata: 8 settimane")
    print()
    turno_cibo(0)

    print("=" * 50)
    print("  RIEPILOGO CIBO:")
    stampa_stato_cibo()
    input("  Premi INVIO per continuare...")

def stampa_stato_merci():
    print()
    print("  Merci attualmente nel carrello:")
    for nome, qty in stato_gioco["merci"].items():
        unita = CATALOGO_MERCI[nome]["unita"]
        print(f"    {nome.capitalize():<14} {qty} {unita}")
    print(f"  Monete disponibili: {monete_disponibili():.1f}")
    print()

def turno_merci(indice):
    nomi = list(CATALOGO_MERCI.keys())
    if indice >= len(nomi):
        return

    nome = nomi[indice]
    dati = CATALOGO_MERCI[nome]
    prezzo = dati["prezzo"]
    unita = dati["unita"]

    print(f"  {nome.upper()}  –  {prezzo} monete/pezzo")
    print(f"  Monete disponibili: {monete_disponibili():.1f}")

    qty = input_intero(f"  Quante unità di {nome} vuoi comprare? (0 per saltare): ", minimo=0)
    costo = qty * prezzo

    if costo > monete_disponibili():
        print(f"  ✗ Non hai abbastanza monete (servono {costo:.1f}). Acquisto annullato.")
    else:
        stato_gioco["merci"][nome] += qty
        stato_gioco["monete_spese"] += costo
        if qty > 0:
            print(f"  → Acquistate {qty} {unita} di {nome} per {costo:.1f} monete.")
    print()

    turno_merci(indice + 1)

def fase_acquisto_merci():
    print()
    print("=" * 50)
    print("  FASE 3 – ACQUISTO DELLE MERCI")
    print("=" * 50)
    print()
    print("  Le merci serviranno per il baratto nel nuovo mondo.")
    print()
    turno_merci(0)

    print("=" * 50)
    print("  RIEPILOGO MERCI:")
    stampa_stato_merci()
    input("  Premi INVIO per continuare...")


def riepilogo_pre_partenza():
    print()
    print("=" * 50)
    print("  TUTTO PRONTO – RIEPILOGO PRE-PARTENZA")
    print("=" * 50)
    print()

    print(f"  Equipaggio: {totale_equipaggio()} persone")
    print(f"  Paga stimata (8 sett.): {paga_stimata()} monete")
    print()

    print("  Cibo:")
    for nome, qty in stato_gioco["cibo"].items():
        print(f"    {nome.capitalize():<10} {qty:.1f} {CATALOGO_CIBO[nome]['unita']}")
    print()

    print("  Merci:")
    for nome, qty in stato_gioco["merci"].items():
        print(f"    {nome.capitalize():<14} {qty} {CATALOGO_MERCI[nome]['unita']}")
    print()

    print(f"  Monete spese:     {stato_gioco['monete_spese']:.1f}")
    print(f"  Monete residue:   {monete_disponibili():.1f}")
    print()
    print("  Buon vento, capitano!")
    print("=" * 50)
    print()
    input("  Premi INVIO per salpare...")

fase_ingaggio()
fase_acquisto_cibo()
fase_acquisto_merci()
riepilogo_pre_partenza()