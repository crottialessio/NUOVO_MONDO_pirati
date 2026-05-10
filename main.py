import random
import json

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

moltiplicatori_razioni = {"verdura": 1, "frutta": 1, "carne": 1, "acqua": 1}

merci_baratto = {
    "perla": {
        "sale":           0.5,
        "stoffa":         5,
        "coltello":       1,
        "diamanti":       2,
        "prezzo stimato": 2
    },
    "manufatti": {
        "sale":           0.5,
        "stoffa":         7,
        "coltello":       3,
        "diamanti":       4,
        "prezzo stimato": 2
    },
    "spezie": {
        "sale":           1,
        "stoffa":         3,
        "coltello":       6,
        "diamanti":       4,
        "prezzo stimato": 1
    }
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
        "perle":      0,
        "manufatti":  0,
        "spezie":     0,
    },
}

FILE_SALVATAGGIO = "salvataggio.txt"

def Salva(stato):
    f = open(FILE_SALVATAGGIO, "w")
    json.dump(stato, f)
    f.close()
    

def Carica():
    f = open(FILE_SALVATAGGIO, "r")
    stato = json.load(f)
    f.close()
    return stato
    
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
    print("  FASE 2 - ACQUISTO DEL CIBO")
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
        if nome in CATALOGO_MERCI:
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
    print("  TUTTO PRONTO - RIEPILOGO PRE-PARTENZA")
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
        if nome in CATALOGO_MERCI:
            print(f"    {nome.capitalize():<14} {qty} {CATALOGO_MERCI[nome]['unita']}")
    print()
    print(f"  Monete spese:     {stato_gioco['monete_spese']:.1f}")
    print(f"  Monete residue:   {monete_disponibili():.1f}")
    print()
    print("  Buon vento, capitano!")
    print("=" * 50)
    print()
    input("  Premi INVIO per salpare...")


colpito=None
qta_da_perdere=[0.5,0.33,0.25,0.2]
###########################################################################################à
#! FUNZIONI DI GIOCO BASE
def si_no(domanda_dec):
    corretto=False
    while corretto!=True:
        decisione_ut=input(f"{domanda_dec}(si/no)").lower().strip()
        if decisione_ut=="si":return True
        elif decisione_ut=="no":return False
        else:
            print("l'input non è stato inserito correttamente è si o no")

def conta_vivi(equipaggio_in):
    conta=0
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True:
            conta+=1
    return conta

def Min_sparo_difesa(equipaggio_in,merci_in,funz_n_vivi):
    n_armi=merci_in["armi"]
    qta_vivi=funz_n_vivi(equipaggio_in)
    tentativi=min(qta_vivi,n_armi)
    return tentativi

def ce_ruolo(equipaggio_in,ruolo_ind):
    for membro in equipaggio_in.values():
        if membro["ruolo"]==ruolo_ind and membro["vivo"]==True:
            return True
    return False
####################################################################################
def prova_unica(equipaggiamento_in,oggetto,qta_perdere_0):
    qta_persa=random.choice(qta_perdere_0)
    peso_perso=equipaggiamento_in[oggetto]*qta_persa
    equipaggiamento_in[oggetto]-=peso_perso
    return equipaggiamento_in,peso_perso

def tempesta_miracolosa(equipaggiamento_in,oggetto):
    qta_guadagnata=random.randint(11,20)
    equipaggiamento_in[oggetto]+=qta_guadagnata
    return equipaggiamento_in,qta_guadagnata

def raffiche_di_vento(equipaggio_in,settimane_int,ruolo_ind):
    presenza_ruolo=False
    for membro in equipaggio_in.values():
        if membro["ruolo"]==ruolo_ind and membro["vivo"]==True:
            presenza_ruolo=True
    if presenza_ruolo==True:
        settimane_int+=1
        return 1,settimane_int,presenza_ruolo
    else:
        sett_casuale=random.randint(2,4)
        settimane_int+=sett_casuale
        return sett_casuale,settimane_int,presenza_ruolo

def uomo_in_mare(equipaggio_in,delta_mor):
    eq_vivi=[]
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True:
            eq_vivi.append(i)
    morto=random.choice(eq_vivi)
    equipaggio_in[morto]["vivo"]=False
    delta_mor=aggiorna_DELTA_morlae(delta_mor,-10)
    return equipaggio_in[morto]['ruolo'],delta_mor

def vento_favorevole(settimane_in,equipaggio_in,delta_mor):
    morale_piu=random.randint(5,15)
    
    settimane_in-=1
    delta_mor=aggiorna_DELTA_morlae(delta_mor,morale_piu)
    return equipaggio_in,settimane_in,delta_mor,morale_piu

def avvistamento_albatro(equipaggio_in,merci_in,funz_decisione,funz_n_vivi,min_sparo,cibo_in):
    n_armi=merci_in["armi"]
    decisione_abbatimento=None
    colpito=False
    conta_armi=0
    if n_armi>=1:
        domanda="gli si vuole sparare?"
        decisione_abbatimento=funz_decisione(domanda)
        if decisione_abbatimento==True:
            tentativi_sparare=min_sparo(equipaggio_in,merci_in,funz_n_vivi)
            for i in range(int(tentativi_sparare)):#mettere int prchè sennò bug FOR MAI FLOAT
                colpito=random.randint(0,1)
                merci_in["armi"]-=1
                conta_armi+=1
                if colpito==1:
                    qta_cas_carne=random.randint(10,15)
                    cibo_in["carne"]+=qta_cas_carne
                    return True,merci_in,decisione_abbatimento,qta_cas_carne,conta_armi
            return colpito,merci_in,decisione_abbatimento,None,conta_armi
        else:
            return False,merci_in,decisione_abbatimento,None,None
    return colpito,merci_in,decisione_abbatimento,None,None

def avvistamento_scialuppa(funz_decisione,merci_in,ruoli_base,equipaggio_in):
    domanda="vuoi salvarli?"
    decisione=funz_decisione(domanda)
    if decisione==False:
        return decisione,None
    else:
        merce_iniziale=merci_in.copy()
        for i in range(4):
            nuovo_id=max(equipaggio_in.keys())+1
            morale_cas=random.randint(25,75)
            ruoli=list(ruoli_base.keys())
            ruolo_cas=random.choice(ruoli)
            naufrago_creato={"ruolo":ruolo_cas,"paga_settimanale":ruoli_base[ruolo_cas]["paga_settimanale"],"morale":morale_cas,"vivo":True,"ingaggiato":False}
            equipaggio_in[nuovo_id]=naufrago_creato
        for i in merci_in:
            merci_cas=random.randint(10,20)
            merci_in[i]+=merci_cas
        return decisione,merce_iniziale

def epidemia(equipaggio_in,merci_in,ce_medico,delta_mor):
    conta_malati=0
    conta_morti=0
    conta_guariti=0
    medicinali_persi=0
    presenza_med=ce_medico(equipaggio_in,"medico")
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True and equipaggio_in[i]["ruolo"]!="medico":
            ott_malattia=random.randint(1,100)
            if ott_malattia<=70:
                conta_malati+=1
                if presenza_med==True and merci_in["medicinali"]>=1:
                    equipaggio_in[i]["vivo"]=True
                    merci_in["medicinali"]-=1
                    medicinali_persi+=1
                    conta_guariti+=1
                else:
                    equipaggio_in[i]["vivo"]=False
                    conta_morti+=1
    if conta_malati>=1:
        delta_mor=aggiorna_DELTA_morlae(delta_mor,-5)
    return conta_malati,conta_morti,conta_guariti,medicinali_persi,delta_mor

def attacco_pirata(equipaggio_in,funz_conta_vivi,merci_in,funz_min_sparo,delta_mor):
    n_pirati=random.randint(3,10)
    n_vivi=funz_conta_vivi(equipaggio_in)
    n_difensori=funz_min_sparo(equipaggio_in,merci_in,funz_conta_vivi)
    merci_in["armi"]-=n_difensori
    uomini_persi=min(n_pirati-n_difensori,n_vivi)
    if uomini_persi>=1:
        delta_mor=aggiorna_DELTA_morlae(delta_mor,-5)
        eq_vivi=[]
        for i in equipaggio_in:
            if equipaggio_in[i]["vivo"]==True:
                eq_vivi.append(i)
        for j in range(uomini_persi):
            morto=random.choice(eq_vivi)
            equipaggio_in[morto]["vivo"]=False
            eq_vivi.remove(morto)
    return uomini_persi,n_pirati,n_difensori,delta_mor

def avvistamento_isola(funz_dec,albatro_morto,merci_in):
    domanda="viene avvistata un isola, ci si vuole andare??"
    risposta=funz_dec(domanda)
    if risposta==False:
        return "non raggiunta",None,None
    else:
        sett_aggiuntive=random.randint(1,2)
        prob_abit=random.randint(0,1)
        if prob_abit==0:
            return "non abitata",None,sett_aggiuntive
        else:
            ostilità=random.randint(0,1)
            if ostilità==1:
                return "ostile",None,sett_aggiuntive
            else:
                merci_prec=merci_in.copy()
                for i in merci_in:
                    if albatro_morto==False:
                        qta_cas=random.randint(20,40)
                    else:
                        qta_cas=random.randint(5,20)
                    merci_in[i]+=qta_cas
                return "abitata",merci_prec,sett_aggiuntive

def calcola_riepilogo_sc_mc(ogg,iter):
    qta=ogg[iter]
    return iter,qta

def calcola_riepilogo(merci_in,cibo_in,equipaggio_in):
    print("---->FINE SETTIMANA<----")
    print("RIEPILOGO DELLA SETTIMANA")
    print(f"\nRIEPILOGO MERCI")
    for m in merci_in:
        merce,quantità=calcola_riepilogo_sc_mc(merci_in,m)
        print(f"{merce}:{quantità}")
    print(f"\nRIEPILOGO SCORTE")
    for s in cibo_in:
        merce_sc,quantità_sc=calcola_riepilogo_sc_mc(cibo_in,s)
        if s=="acqua":
            print(f"{merce_sc}:{quantità_sc} barili")
        else:
            print(f"{merce_sc}:{quantità_sc}")
    print(f"\nRIEPILOGO EQUIPAGGIO")
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True:
            print(f"{i} {equipaggio_in[i]["ruolo"]} morale:{equipaggio_in[i]["morale"]}")

def ammutinamento(dimezzato,funz_ce_ruolo,equipaggio_in,albatro_colpito,funz_n_vivi,differenza_Setttimane):
    pt_ammunitamento=0
    num_vivi=funz_n_vivi(equipaggio_in)
    presenza_ruolo=funz_ce_ruolo(equipaggio_in,"cuoco")
    if dimezzato==True:
        pt_ammunitamento+=30
    if num_vivi>=12:
        pt_ammunitamento+=30
    if albatro_colpito==True:
        pt_ammunitamento+=30
    if albatro_colpito==False:
        pt_ammunitamento-=20
    if presenza_ruolo==False:
        pt_ammunitamento+=30
    pt_ammunitamento+=differenza_Setttimane*10
    return pt_ammunitamento

def printare_ammutinamento_cond(pt_ammutinamento):
    if 1<=pt_ammutinamento<=99:
        print("c'è un alto rischio di ammutinameto si coniglia di \n non sparare agli albatro e di affrettarsi con il viaggio")
    elif pt_ammutinamento>=100:
        print(f"HAI PERSO :( \n, il livello di ammutinamento ha raggiunto i 100 punti e gli uomini ti hanno abbandonato\n GAME OVER")


def ricalcolo_settimane(sett,equipaggio_in,funz_n_vivi):
    num_vivi=funz_n_vivi(equipaggio_in)
    conta_min_mor=0
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True and equipaggio_in[i]["morale"]<=30:
            conta_min_mor+=1
    if num_vivi//2<=conta_min_mor:
        sett+=1
    return sett

def aggiorna_DELTA_morlae(delta_mor,qta):
    delta_mor+=qta
    return delta_mor

def aggiungi_mor_equip(equipaggio_in,delta_mor):
    for m in equipaggio_in.values():
        if m["vivo"]==True:
            m["morale"]+=delta_mor
            if m["morale"]<=0:

                m["vivo"]=False
    return equipaggio_in

SETTIMANE=8
sett_vecchie=8
settimane=8
delta_morale=0
li_eventi=[0,1,2,3,4,5,6,7,8,9,10,11,90,91,12,13,14,15,16,17,18]
conta_set=1
punti_ammutinamento=0
game_over=False
#>= perchè se faccio +2 verso la fine il gioco fa aanti tanto

def Calcolo_cibo_1_sett(CATALOGO_CIBO,stato_gioco):
    membri_vivi = conta_vivi(stato_gioco["equipaggio"])
    verdura = CATALOGO_CIBO["verdura"]["consumo"] * membri_vivi
    frutta = CATALOGO_CIBO["frutta"]["consumo"] * membri_vivi
    carne = CATALOGO_CIBO["carne"]["consumo"] * membri_vivi
    acqua = CATALOGO_CIBO["acqua"]["consumo"] * membri_vivi
    return [verdura,frutta,carne,acqua]

def Sottrai_consumo_settimana(stato_gioco, cibi, moltiplicatori_razioni):
    tipi = ["verdura", "frutta", "carne", "acqua"]
    for i, tipo in enumerate(tipi):
        stato_gioco["cibo"][tipo] -= cibi[i] * moltiplicatori_razioni[tipo]
        if stato_gioco["cibo"][tipo] < 0:
            stato_gioco["cibo"][tipo] = 0

def Stato_cibo(cibo, fabbisogno_equip):
    if cibo <= 0:
        return "esaurita"
    elif cibo < fabbisogno_equip:
        return "insufficiente"
    elif cibo >= fabbisogno_equip * 2:
        return "abbondante"
    else:
        return "normale"

def Chiedi_modifica_razione(cibo, stato):
    if stato == "insufficiente":
        print(f"Attenzione: le scorte di {cibo} non bastano per le settimane restanti!")
        scelta = input("Vuoi dimezzare le razioni? (s/n): ").strip().lower()
    elif stato == "abbondante":
        print(f"Le scorte di {cibo} sono abbondanti!")
        scelta = input("Vuoi raddoppiare le razioni? (s/n): ").strip().lower()
    else:
        return "n"
    
    while scelta not in ["s", "n"]:
        print("Scelta non valida.")
        scelta = input("(s/n): ").strip().lower()
    return scelta

def Aggiorna_moltiplicatore_e_morale(cibo, stato, scelta, moltiplicatori, delta_morale):
    if stato == "esaurita":
        delta_morale -= 10
    elif stato == "insufficiente" and scelta == "s":
        moltiplicatori[cibo] *= 0.5
        delta_morale -= 5
    elif stato == "abbondante" and scelta == "s":
        moltiplicatori[cibo] *= 2
        delta_morale += 5
    return delta_morale

def Controllo_scorte(stato_gioco, CATALOGO_CIBO, settimane_restanti, moltiplicatori, delta_morale):
    
    cibi = Calcolo_cibo_1_sett(CATALOGO_CIBO, stato_gioco)
    Sottrai_consumo_settimana(stato_gioco, cibi, moltiplicatori)
    tipi = ["verdura", "frutta", "carne", "acqua"]
    
    for i, tipo in enumerate(tipi):
        fabbisogno = cibi[i] * moltiplicatori[tipo] * settimane_restanti
        stato = Stato_cibo(stato_gioco["cibo"][tipo], fabbisogno)
        scelta = Chiedi_modifica_razione(tipo, stato)
        delta_morale = Aggiorna_moltiplicatore_e_morale(tipo, stato, scelta, moltiplicatori, delta_morale)
    
    return delta_morale

def baratto_sale(merci_baratto, stato_gioco): #TODO aggiungere condizione nel mein per la chiamata di questa funzione
    print("\n--- BARATTO: SALE ---")
    print("Offrirai tutti i tuoi sacchi di sale. Scegli una sola opzione:")
    perle = stato_gioco["merci"]["sale"]//merci_baratto["perla"]["sale"]
    manufatti = stato_gioco["merci"]["sale"]//merci_baratto["manufatti"]["sale"]
    spezie = stato_gioco["merci"]["sale"]//merci_baratto["spezie"]["sale"]

    print(f"  1) {perle} perle        (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']} dobloni)")
    print(f"  2) {manufatti} manufatti   (rivendibili a {merci_baratto['manufatti']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatti']['prezzo stimato']} dobloni)")
    print(f"  3) {spezie} spezie       (rivendibili a {merci_baratto['spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['spezie']['prezzo stimato']} dobloni)")
    
    corretto = False
    while not corretto:
        scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
        
        if scelta not in ["1", "2", "3"]:
            print("  Scelta non valida, riprova.")

        elif scelta == "1":
            stato_gioco["merci"]["sale"] = 0
            stato_gioco["merci"]["perle"] += perle
            print(f"  Hai ottenuto {perle} perle!")
            corretto = True

        elif scelta == "2":
            stato_gioco["merci"]["sale"] = 0
            stato_gioco["merci"]["manufatti"] += manufatti
            print(f"  Hai ottenuto {manufatti} manufatti!")
            corretto = True
        
        elif scelta == "3":
            stato_gioco["merci"]["sale"] = 0
            stato_gioco["merci"]["spezie"] += spezie
            print(f"  Hai ottenuto {spezie} barattoli di spezie!")
            corretto = True

def baratto_stoffa(merci_baratto, stato_gioco): #TODO aggiungere condizione nel mein per la chiamata di questa funzione
    print("\n--- BARATTO: STOFFA ---")
    print("Offrirai tutti i tuoi teli di stoffa. Scegli una sola opzione:")
    perle = stato_gioco["merci"]["stoffa"]//merci_baratto["perla"]["stoffa"]
    manufatti = stato_gioco["merci"]["stoffa"]//merci_baratto["manufatti"]["stoffa"]
    spezie = stato_gioco["merci"]["stoffa"]//merci_baratto["spezie"]["stoffa"]

    print(f"  1) {perle} perle (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']} dobloni)")
    print(f"  2) {manufatti} manufatti (rivendibili a {merci_baratto['manufatti']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatti']['prezzo stimato']} dobloni)")
    print(f"  3) {spezie} barattoli di spezie (rivendibili a {merci_baratto['spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['spezie']['prezzo stimato']} dobloni)")
    
    corretto = False
    while not corretto:
        scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
        
        if scelta not in ["1", "2", "3"]:
            print("  Scelta non valida, riprova.")

        elif scelta == "1":
            stato_gioco["merci"]["stoffa"] = 0
            stato_gioco["merci"]["perle"] += perle
            print(f"  Hai ottenuto {perle} perle!")
            corretto = True

        elif scelta == "2":
            stato_gioco["merci"]["stoffa"] = 0
            stato_gioco["merci"]["manufatti"] += manufatti
            print(f"  Hai ottenuto {manufatti} manufatti!")
            corretto = True
        
        elif scelta == "3":
            stato_gioco["merci"]["stoffa"] = 0
            stato_gioco["merci"]["spezie"] += spezie
            print(f"  Hai ottenuto {spezie} barattoli di spezie!")
            corretto = True

def baratto_coltelli(merci_baratto, stato_gioco): #TODO aggiungere condizione nel mein per la chiamata di questa funzione
    print("\n--- BARATTO: COLTELLI ---")
    print("Offrirai tutti i tuoi coltelli. Scegli una sola opzione:")
    perle = stato_gioco["merci"]["coltelli"]//merci_baratto["perla"]["coltello"]
    manufatti = stato_gioco["merci"]["coltelli"]//merci_baratto["manufatti"]["coltello"]
    spezie = stato_gioco["merci"]["coltelli"]//merci_baratto["spezie"]["coltello"]

    print(f"  1) {perle} perle (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']} dobloni)")
    print(f"  2) {manufatti} manufatti (rivendibili a {merci_baratto['manufatti']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatti']['prezzo stimato']} dobloni)")
    print(f"  3) {spezie} barattoli di spezie (rivendibili a {merci_baratto['spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['spezie']['prezzo stimato']} dobloni)")
    
    corretto = False
    while not corretto:
        scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
        
        if scelta not in ["1", "2", "3"]:
            print("  Scelta non valida, riprova.")

        elif scelta == "1":
            stato_gioco["merci"]["coltelli"] = 0
            stato_gioco["merci"]["perle"] += perle
            print(f"  Hai ottenuto {perle} perle!")
            corretto = True

        elif scelta == "2":
            stato_gioco["merci"]["coltelli"] = 0
            stato_gioco["merci"]["manufatti"] += manufatti
            print(f"  Hai ottenuto {manufatti} manufatti!")
            corretto = True
        
        elif scelta == "3":
            stato_gioco["merci"]["coltelli"] = 0
            stato_gioco["merci"]["spezie"] += spezie
            print(f"  Hai ottenuto {spezie} barattoli di spezie!")
            corretto = True

def baratto_diamanti(merci_baratto, stato_gioco): #TODO aggiungere condizione nel mein per la chiamata di questa funzione
    print("\n--- BARATTO: DIAMANTI ---")
    print("Offrirai tutti i tuoi diamanti. Scegli una sola opzione:")
    perle = stato_gioco["merci"]["diamanti"]//merci_baratto["perla"]["diamanti"]
    manufatti = stato_gioco["merci"]["diamanti"]//merci_baratto["manufatti"]["diamanti"]
    spezie = stato_gioco["merci"]["diamanti"]//merci_baratto["spezie"]["diamanti"]

    print(f"  1) {perle} perle (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']} dobloni)")
    print(f"  2) {manufatti} manufatti (rivendibili a {merci_baratto['manufatti']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatti']['prezzo stimato']} dobloni)")
    print(f"  3) {spezie} barattoli di spezie (rivendibili a {merci_baratto['spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['spezie']['prezzo stimato']} dobloni)")
    
    corretto = False
    while not corretto:
        scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
        
        if scelta not in ["1", "2", "3"]:
            print("  Scelta non valida, riprova.")

        elif scelta == "1":
            stato_gioco["merci"]["diamanti"] = 0
            stato_gioco["merci"]["perle"] += perle
            print(f"  Hai ottenuto {perle} perle!")
            corretto = True

        elif scelta == "2":
            stato_gioco["merci"]["diamanti"] = 0
            stato_gioco["merci"]["manufatti"] += manufatti
            print(f"  Hai ottenuto {manufatti} manufatti!")
            corretto = True
        
        elif scelta == "3":
            stato_gioco["merci"]["diamanti"] = 0
            stato_gioco["merci"]["spezie"] += spezie
            print(f"  Hai ottenuto {spezie} barattoli di spezie!")
            corretto = True
            
def Resoconto_baratto(merci_baratto, stato_gioco):
    print("\n" + "=" * 50)
    print("BARATTO CONCLUSO!")
    print("Ecco il resoconto, hai ottenuto:")
    print(f"  Perle:            {stato_gioco["merci"]['perle']} - totale stimato: {stato_gioco["merci"]['perle'] * merci_baratto['perla']['prezzo stimato']} dobloni")
    print(f"  Manufatti:        {stato_gioco["merci"]['manufatti']} - totale stimato: {stato_gioco["merci"]['manufatti'] * merci_baratto['manufatti']['prezzo stimato']} dobloni")
    print(f"  Barattoli spezie: {stato_gioco["merci"]['spezie']} - totale stimato: {stato_gioco["merci"]['spezie'] * merci_baratto['spezie']['prezzo stimato']} dobloni")
    print("=" * 50)

def Intro_tradimento(merci_baratto, stato_gioco): #TODO ricontrollo e se possibile semplificazione della funzione
    # Questa funzione va chiamata solo se il giocatore ha armi residue

    ricavo_ipo = stato_gioco["merci"]["armi"] * 30 * merci_baratto["perla"]["prezzo stimato"]

    print(f"\nDurante la notte un rivale del capotribù si presenta al vostro accampamento ")
    print(f"offrendovi ben 30 perle per ogni arma che avete ")
    print(f"(ricavo ipotetico di {ricavo_ipo} dobloni).")

    scelta = input("Accetti la proposta del rivale del capotribù? (s/n): ").strip().lower()
    while scelta not in ["s", "n"]:
        print("Scelta non valida, riprovare.")
        scelta = input("Accetti la proposta del rivale del capotribù? (s/n): ").strip().lower()

    return scelta

def Ricompensa(albatro): #TODO chiamare questa funzione solo se il giocatore non accetta di dare le armi al rivale
    import random
    if albatro == True:
        offerta=random.randint(5,20)
    else:
        offerta=random.randint(30,50)
    
    return offerta

def Tradimento(stato_gioco,albatro):
    import random

    stato_gioco["merci"]["perle"] += stato_gioco["merci"]["armi"] * 30
    stato_gioco["merci"]["armi"] = 0

    scoperto = False

    if albatro == True:
        scoperto = True
    elif albatro == None:
        scoperto = random.randint(1, 2) == 1

    return scoperto


def calcolo_settimane_e_rifornimento(stato_gioco,albatro, CATALOGO_CIBO):
    cibi=Calcolo_cibo_1_sett(CATALOGO_CIBO,stato_gioco)
    
    stato_gioco["cibo"]["verdura"] +=cibi[0] * 3
    stato_gioco["cibo"]["frutta"] += cibi[1] * 3
    stato_gioco["cibo"]["carne"] += cibi[2] * 3
    stato_gioco["cibo"]["acqua"] += cibi[3] * 3

    if ce_ruolo(stato_gioco["equipaggio"], "navigatore"):
        settimane_agg = 1
    else:
        settimane_agg = 2
    
    if albatro == True:
        settimane_agg+=1
    
    return settimane_agg #TODO sommare settimane aggiuntive a settimane nel main

def Profitto(stato_gioco,merci_baratto):
    import random
    oscillazione=random.choice([0.5,1,2])

    profitto = (
        stato_gioco["merci"]["perle"]*(merci_baratto["perla"]["prezzo stimato"]*oscillazione)+
        stato_gioco["merci"]["manufatti"]*(merci_baratto["manufatti"]["prezzo stimato"]*oscillazione)+
        stato_gioco["merci"]["spezie"]*(merci_baratto["spezie"]["prezzo stimato"]*oscillazione)
        )
    
    return profitto

def Calcolo_spesa_equipaggio(stato_gioco,settimane):
    
    spesa_equip=0

    for membro in stato_gioco["equipaggio"].values():
        if membro["ingaggiato"]:
            spesa_equip += membro["paga_settimanale"]*settimane

    return spesa_equip

def Stampa_situazione_economica(profitto,stato_gioco,spesa_equip):

    print(f"il profitto ricavato dalla vendita delle tue merci è di {profitto} dobloni !!!")
    stato_gioco["monete"]+=profitto
    print(f"questi si sommano ai tuoi dobloni residui e raggiungi la cospiqua somma di {stato_gioco["monete"]}")
    print(f"ricordati però che devi pagare i prodi membri del tuo equipaggio che ti hanno accompagnato nella tua avventura")
    print(f"dovrai pagare in totale una somma pari a {spesa_equip}")
    stato_gioco["monete"]-=spesa_equip
    print(f"questo è quello che ti rimane: {stato_gioco["monete"]} dobloni") #TODO nel main fare un if che se monete < 0 chiama la funzione scelta

def Scelta():
    print("Purtroppo i tuoi dobloni non bastano a coprire le spese dell'equipaggio")
    scelta=input("vuoi mettere all'asta la tua nave nel tentativo di ricavarne abbastanza per ripagare i tuoi uomini? (s/n) ").strip().lower()
    
    while scelta not in ["s","n"]:
        print("scelta non valida")
        scelta=input("vuoi mettere all'asta la tua nave nel tentativo di ricavarne abbastanza per ripagare i tuoi uomini? (s/n) ").strip().lower()
    
    return scelta #TODO nel main fare un if che se scelta == s chiama la funzione Asta, altrimenti chiama bad ending

def Asta(stato_gioco):
    import random
    valori_temp=[350,500,550,600,650,700,750,800,850,1200,350,500,550,600,650,700,750,800,850,1200]
    valori=[50,300,400,450]
    
    print("Questa è l'asta, ti verranno fatte delle offerte per la tua nave, che potrai accettare o rifiutare")

    risposta=""
    while risposta != "s":
        lista=random.randint(1,2)

        if not valori_temp:
            lista=2

        if lista == 1:
            valore=random.randint(0,len(valori_temp)-1)
            offerta=valori_temp[valore]
            print(f"un offerente ti propone {offerta} dobloni")
            risposta=input("accetti? (s/n) ").strip().lower()
            while risposta not in ["s","n"]:
                print("scelta non valida")
                risposta=input("accetti? (s/n) ").strip().lower()
            valori_temp.pop(valore)

        else:
            valore=random.randint(0,len(valori)-1)
            offerta=valori[valore]
            print(f"un offerente ti propone {offerta}")
            risposta=input("accetti? (s/n) ").strip().lower()
            while risposta not in ["s","n"]:
                print("scelta non valida")
                risposta=input("accetti? (s/n) ").strip().lower()
       
    stato_gioco["monete"]+=offerta

def Good_ending(stato_gioco):

    if stato_gioco["monete"] > 2000:
        print(f"sei riuscito a portarti a casa ben {stato_gioco["monete"]} dobloni, più di quelli che avevi inizialmente congratulazioni !!!")
    
    elif 1000<= stato_gioco["monete"] <= 2000 :
        print(f"sei riuscito a portarti a casa ben {stato_gioco["monete"]} dobloni, non male !!")
    
    elif 10 < stato_gioco["monete"] < 1000:
        print(f"sei riuscito a portarti a casa {stato_gioco["monete"]} dobloni, poteva andare meglio, ma è già qualcosa !")
    
    elif 1 < stato_gioco["monete"] <= 10:
        print(f"sei riuscito a portarti a casa {stato_gioco["monete"]} dobloni, il giusto per comprati un gelato")

    else:
        print(f"sei riuscito a portarti a casa {stato_gioco["monete"]} singolo doblone, una misera consolazione")

def Neutral_ending():
    print("sei riuscito a ripagare il tuo equipaggio ma non ti è rimasto nulla...tanta fatica per niente")

def Bad_ending():
    print("non sei riuscito a ripagare nemmeno il tuo equipaggio, non è stata proprio una bella idea quella del viaggio verso il nuovo mondo")


# -------CODICE PRINCIPALE------

print("--- BENVENUTO IN NUOVO MONDO ---")

scelta = input("Vuoi caricare la partita precedente? (s/n): ").lower().strip()
if scelta == "s":
    dati_caricati = Carica()
    if dati_caricati:
        stato_gioco = dati_caricati
        print("Partita caricata con successo!")
    else:
        print("Nessun salvataggio trovato. Inizio nuova partita.")

# parte cars------------------------------------------------------------------------------------------------------------------------------------------------------




























# parte crotz------------------------------------------------------------------------------------------------------------------------------------------------------




















while settimane>=conta_set and game_over!=True and punti_ammutinamento<100:
    
    if conta_vivi(stato_gioco["equipaggio"])==0:
        print("tutti i membri sono morti, il gioco finisce qui, GAME OVER")
        game_over=True
    else:

        n_evento=random.choice(li_eventi)
        
        
        print(f"-----SETTIMANA {conta_set}-----")
        if n_evento==0:
            pg_morto,delta_morale=uomo_in_mare(stato_gioco["equipaggio"],delta_morale)
            print(f"---EVENTO UMOMO IN MARE--- \n il {pg_morto.upper()} è caduto in mare ed è MORTO")
            li_eventi.remove(0)
        
        
        elif n_evento==1:
            stato_gioco["cibo"],perdite_verdure=prova_unica(stato_gioco["cibo"],"verdura",qta_da_perdere)
            print(f"---EVENTO VERDURA IN MARE--- \n una violenta tempesta ha trasportato in mare delle casse che contenevano {perdite_verdure} Kg di VERDURE")
            li_eventi.remove(n_evento)
    
    
        elif n_evento==2:
            stato_gioco["cibo"],perdite_frutta=prova_unica(stato_gioco["cibo"],"frutta",qta_da_perdere)
            print(f"---EVENTO FRUTTA IN MARE--- \n una violenta tempesta ha trasportato in mare delle casse che contenevano {perdite_frutta} Kg di FRUTTA")
            li_eventi.remove(n_evento)
        
        
        elif n_evento==3:
            stato_gioco["cibo"],perdite_carne=prova_unica(stato_gioco["cibo"],"carne",qta_da_perdere)
            print(f"---EVENTO CARNE IN MARE--- \n una violenta tempesta ha trasportato in mare delle casse che contenevano {perdite_carne} Kg di CARNE")
            li_eventi.remove(n_evento)
        
        
        elif n_evento==4:
            stato_gioco["cibo"],perdite_acqua=prova_unica(stato_gioco["cibo"],"acqua",qta_da_perdere)
            print(f"---EVENTO ACQUA IN MARE--- \n una violenta tempesta ha trasportato in mare {perdite_acqua} BARILI D'ACQUA")
            li_eventi.remove(n_evento)
        
        
        elif n_evento==5:
            stato_gioco["cibo"],qta_pescata=tempesta_miracolosa(stato_gioco["cibo"],"carne")
            print(f"---EVENTO PESCA MIRACOLOSA--- \n durante la settimana di quiete l'equipaggio ha pescato {qta_pescata} kg di CARNE")
            li_eventi.remove(n_evento)
    
    
        elif n_evento==6:
            stato_gioco["cibo"],qta_acqua=tempesta_miracolosa(stato_gioco["cibo"],"acqua")
            print(f"---EVENTO TEMPESTA MIRACOLOSA --- \n durante la tempesta dei coraggiosi uomini hanno riempito d'ACQUA {qta_acqua} BARILI VUOTI")
            li_eventi.remove(n_evento)
    
    
        elif n_evento==7:
            stato_gioco["equipaggio"],settimane,delta_morale,morale_agg=vento_favorevole(settimane,stato_gioco["equipaggio"],delta_morale)
            print(f"---EVENTO VENTO FAVOREVOLE--- \n un vento favorevole, permette di ACCORCIARE di 1 SETTIMANA il viaggio \n ogni membro dell'equipaggio AUMENTA il MORALE di {morale_agg}")
            li_eventi.remove(n_evento)
    
    
        elif n_evento==8:
            stato_gioco["merci"],perdite_medicinali=prova_unica(stato_gioco["merci"],"medicinali",qta_da_perdere)
            print(f"---EVENTO CATTIVO TEMPO--- \n il cattivo tempo ha rovesciato {perdite_medicinali} BOTTIGLIE DI MEDICINALI")
            li_eventi.remove(n_evento)
    
    
        elif n_evento==9:
            stato_gioco["merci"],perdite_armi=prova_unica(stato_gioco["merci"],"armi",qta_da_perdere)
            print(f"---EVENTO ONDATA--- \n una onda altissima ha trasportato in mare {perdite_armi} ARMI")
            li_eventi.remove(n_evento)
        
        elif n_evento==10:
            stato_gioco["merci"],perdite_stoffe=prova_unica(stato_gioco["merci"],"stoffa",qta_da_perdere)
            print(f"---EVENTO INFESTAZIONE RATTI--- \n dei RATTI hanno mordicchiato e rovinato {perdite_stoffe} STOFFE :(")
            li_eventi.remove(n_evento)
        
        
        elif n_evento==11 or n_evento==90 or n_evento==91:
            print("---EVENTO: AVVISTAMENTO ALBATRO--- \n in cielo viene avvistato un albatro, in caso di abbattimento vi sarà un aumento della scorta di CARNE")
            colpito,stato_gioco["merci"],decisone_sparo,qta_guad,armi_utilizzate=avvistamento_albatro(stato_gioco["equipaggio"],stato_gioco["merci"],si_no,conta_vivi,Min_sparo_difesa,stato_gioco["cibo"])
            li_eventi.remove(n_evento)
            if decisone_sparo==True:
                if colpito==True:print(f"l'albatro è stato abbattuto, sono state state utilizzate {armi_utilizzate} ARMI, e l'equipaggio ha raccolto {qta_guad} di CARNE")
                else:print(f"l'albatro non è stato colpito, sono state usate/a {armi_utilizzate} ARMI")
            else:print("L'equipaggio non ha voluto sparare all'albatro, il viaggio prosegue")
        
        
        elif n_evento==12:
            print("---EVENTO: AVVISTAMENTO SCIALUPPA---\n viene avvistata una scialuppa con 4 uomini")
            li_eventi.remove(n_evento)
            deciosione_scialuppa,merci_precedente=avvistamento_scialuppa(si_no,stato_gioco["merci"],RUOLI,stato_gioco["equipaggio"])
            if deciosione_scialuppa==True:
                uomini_id=list(stato_gioco["equipaggio"].keys())
                naufraghi_id=uomini_id[-4:]
                print(f"gli uomini sono stati salvati, e hanno le seguenti caratteristiche:")
                for id in naufraghi_id:
                    print(f"{stato_gioco['equipaggio'][id]['ruolo'].upper()} con morale:{stato_gioco['equipaggio'][id]['morale']}")
                print("dai naufraghi sono stati recuperati (quantità/kg):")
                for m in stato_gioco["merci"]:
                    qta_recuperata=stato_gioco["merci"][m]-merci_precedente[m]
                    print(qta_recuperata,m)
    
    
        elif n_evento==13:
            li_eventi.remove(n_evento)
            print("---EVENTO: EPIDEMIA---\n L'epidemia si abbatte sull'equipaggio")
            n_malati,n_morti,n_guariti,medicinali_usati,delta_morale=epidemia(stato_gioco["equipaggio"],stato_gioco["merci"],ce_ruolo,delta_morale)
            print(f"l'epidemia ha portato {n_malati} MALATI, di cui {n_morti} sono MORTI")
            if n_guariti>=1:print(f"grazie alla presenza del medico, sono stati curati {n_guariti} membri, ma sono state usate {medicinali_usati} bottiglie di MEDICINALE")
        
        
        elif n_evento==14:
            li_eventi.remove(n_evento)
            n_morti_xpir,num_pirati,n_armi_usate,delta_morale=attacco_pirata(stato_gioco["equipaggio"],conta_vivi,stato_gioco["merci"],Min_sparo_difesa,delta_morale)
            print(f"---EVENTO: ATTACCO PIRATA---\n una nave composta da {num_pirati} pirati, sferra un attacco \n sono morti {n_morti_xpir} membri dell tuo equipaggio, e sono state usate {n_armi_usate} ARMI")
        
        
        elif n_evento==15:
            li_eventi.remove(n_evento)
            giorni_in_piu,settimane,presenza_salvatore=raffiche_di_vento(stato_gioco["equipaggio"],settimane,"meccanico")
            if presenza_salvatore==True:print(f"---EVENTO: DANNI AL TIMONE--- \n l'urto con lo scoglio ha causato la rottura del timone il viaggio si allunga di {giorni_in_piu} settimana \n GRAZIE AL MECCANICO il danno è stato riparato in fretta")
            else:print(f"---EVENTO: DANNI AL TIMONE--- \n l'urto con lo scoglio ha causato la rottura del timone il viaggio si allunga di {giorni_in_piu} settimane \n per via dell'ASSENZA DEL MECCANICO il timone viene riparato mooolto lentamente")
    
    
        elif n_evento==16:
            li_eventi.remove(n_evento)
            giorni_in_piu,settimane,presenza_salvatore=raffiche_di_vento(stato_gioco["equipaggio"],settimane,"navigatore")
            if presenza_salvatore==True:print(f"---EVENTO: RAFFICHE DI VENTO--- \n a causa di FORTI RAFFICHE DI VENTO la nave si allontana dalla rotta iniziale, il viaggio si allunga di {giorni_in_piu} settimana \n GRAZIE AL NAVIGATORE la situazione è stata risolta velocemente")
            else:print(f"---EVENTO: RAFFICHE DI VENTO--- \n a causa di FORTI RAFFICHE DI VENTO la nave si allontana dalla rotta iniziale, il viaggio si allunga di {giorni_in_piu} settimane \n per via dell' ASSENZA DEL NAVIGATORE la situazione è stata risolta mooolto lentamente")
        
        
        elif n_evento==17:
            li_eventi.remove(n_evento)
            dec_ab_isola,merce_precedente,sett_in_piu=avvistamento_isola(si_no,colpito,stato_gioco["merci"])
            if dec_ab_isola=="non raggiunta":print("l'equipaggio a preferito non raggiungere l'isola, il viaggio prosegue")
            elif dec_ab_isola=="non abitata":
                settimane+=sett_in_piu
                print(f"l'isola non è abitata, l'equipaggio prosegue il viaggio, esso si allunga di {sett_in_piu} SETTIMANE")
            elif dec_ab_isola=="ostile":
                settimane+=sett_in_piu
                print (f"l'isola è ostile, l'equipaggio scappa dall'isola, il viaggio si allunga di {sett_in_piu} SETTIMANE")
            elif dec_ab_isola=="abitata":
                settimane+=sett_in_piu
                print(f"l'isola è abitata,, il viaggio si allunga di {sett_in_piu} SETTIMANE... l'equipaggio riceve dalla popolazione locale i seguenti doni:")
                for m in stato_gioco["merci"]:
                    qta_recuperata=stato_gioco["merci"][m]-merce_precedente[m]
                    print(qta_recuperata,m)
        elif n_evento==18:
            print("NON SUCCEDE NULLA DI SPECIALE DURANTE LA SETTIMANA")

        input("premi qualsiasi tasto per andare avanti")
        diff_sett=settimane-SETTIMANE
        stato_gioco["equipaggio"]=aggiungi_mor_equip(stato_gioco["equipaggio"],delta_morale)
        calcola_riepilogo(stato_gioco["merci"],stato_gioco["cibo"],stato_gioco["equipaggio"])
        punti_ammutinamento=ammutinamento(True,ce_ruolo,stato_gioco["equipaggio"],colpito,conta_vivi,diff_sett)
        printare_ammutinamento_cond(punti_ammutinamento)
        sett_vecchie=settimane
        settimane=ricalcolo_settimane(settimane,stato_gioco["equipaggio"],conta_vivi)
        if settimane>sett_vecchie:print("L'equipaggio è demoralizzato e il viaggo si ALLUNGA DI 1 SETTIMANA")
        conta_set+=1












#parte mila------------------------------------------------------------------------------------------------------------------------------------------------------

if not game_over:
    print("\n--- TERRA IN VISTA! ---")
    
    if stato_gioco["merci"]["armi"] > 0:
        fuoco = input("Vuoi aprire il fuoco sugli indigeni? (s/n): ").strip().lower()
        if fuoco == "s":
            print("Siete stati massacrati. GAME OVER.")
            game_over = True

    if not game_over:

        if stato_gioco["merci"]["sale"] > 0: 
            baratto_sale(merci_baratto, stato_gioco)
        else:
            print("Siccome non hai abbastanza sale si passerà subito al commercio successivo")
        
        if stato_gioco["merci"]["stoffa"] > 0: 
            baratto_stoffa(merci_baratto, stato_gioco)
        else:
            print("Siccome non hai abbastanza stoffa si passerà subito al commercio successivo")

        if stato_gioco["merci"]["coltelli"] > 0: 
            baratto_coltelli(merci_baratto, stato_gioco)
        else:
            print("Siccome non hai abbastanza coltelli si passerà subito al commercio successivo")

        if stato_gioco["merci"]["diamanti"] > 0: 
            baratto_diamanti(merci_baratto, stato_gioco)
        else:
            print("Siccome non hai abbastanza diamanti si passerà subito al commercio successivo")

        Resoconto_baratto(merci_baratto, stato_gioco)       
        
        if stato_gioco["merci"]["armi"] > 0:
            if Intro_tradimento(merci_baratto, stato_gioco) == "s":
                if Tradimento(stato_gioco, colpito):
                    print("il capovillaggio ha scoperto che hai supportato il suo rivale e ha decretato lo sterminio della tua ciurma. GAME OVER.")
                    game_over = True
            else:
                stato_gioco["merci"]["perle"] += Ricompensa(colpito)
                print(f"il capovillaggio ha saputo che non hai accettato la proposta del suo rivale e come ricompensa ti dona {Ricompensa(colpito)} perle!")
        
    if not game_over:
        print("il capotribù vi fornisce le scorte che bastano a coprire 3 settimane di viaggio per il ritorno")
        print("la destinazione non sarà la patria, ma verso l'isola civilizzata più vicina nel quale potreste rivendere le merci aquistate nel nuovo mondo")
        settimane_ritorno=calcolo_settimane_e_rifornimento(stato_gioco, colpito, CATALOGO_CIBO)
        settimane_ritorno+=conta_set
        
        if settimane_ritorno==1:
            print("Il viaggio dura solamente una settimana e riuscite ad arrivare sani e salvi all'isola più vicina !!!")

        if settimane_ritorno==2:
            print("Il viaggio dura due settimane e arrivate sull'isola più vicina piena di mercanti pronti a commerciare !!")

        if settimane_ritorno==3:
            print("Il viaggio dura tre settimane, arrivate giusti giusti con le scorte fornite dal capotribù, ma incolumi e pronti a rivendere le merci che avete accumulato! ")
        
        entrate=Profitto(stato_gioco,merci_baratto)
        costo_equip=Calcolo_spesa_equipaggio(stato_gioco,conta_set)
        Stampa_situazione_economica(entrate,stato_gioco,costo_equip)
        
           
        if stato_gioco["monete"] < 0:
            if Scelta() == "s":
                Asta(stato_gioco)
                    
        if stato_gioco["monete"] > 0:
            Good_ending(stato_gioco)
        elif stato_gioco["monete"] == 0:
            Neutral_ending()
        else:
            Bad_ending()

print("\n--- FINE PROGRAMMA ---")