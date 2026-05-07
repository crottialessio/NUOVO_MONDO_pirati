#equipaggio: dizionario di dizionari ---> diz{cuoco:{Paga:30,Cibo:20kg,Numero:1}, ...}
#equipaggiamento (armi cibo ecc..): dizioanrio
#merci(stoffa diamanti sale): dizionario di dizionari
 
 
#equipaggio: dizionario di dizionari ---> diz{cuoco:{Paga:30,Cibo:20kg,Numero:1}, ...}
#equipaggiamento (armi cibo ecc..): dizioanrio
#merci(stoffa diamanti sale): dizionario di dizionari
 
import random
 
RUOLI = {
    "cuoco":      {"paga_settimanale": 15},
    "marinaio":   {"paga_settimanale": 10},
    "meccanico":  {"paga_settimanale": 15},
    "medico":     {"paga_settimanale": 25},
    "navigatore": {"paga_settimanale": 20},
}
 
stato_gioco = {
    "monete":        2000,
    "monete_spese":  0,
    "equipaggio":    {},
    "prossimo_id":   1,
}
 
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
    from collections import Counter
    ruoli_membri = [m["ruolo"] for m in stato_gioco["equipaggio"].values()]
    conteggio = Counter(ruoli_membri)
    return {r: conteggio.get(r, 0) for r in RUOLI}
 
def totale_equipaggio():
    return len(stato_gioco["equipaggio"])
 
def paga_stimata(settimane=8):
    paghe = [m["paga_settimanale"] for m in stato_gioco["equipaggio"].values()]
    return sum(paghe) * settimane
 
def stampa_stato():
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
 
 
def riepilogo_finale():
    print()
    print("=" * 50)
    print("  EQUIPAGGIO PRONTO")
    print("=" * 50)
    stampa_stato()
    paga = paga_stimata()
    print(f"  Paga stimata totale: {paga} monete")
    if paga > 2000:
        print("  ⚠  La paga supera le monete! Dovrai guadagnare nel nuovo mondo.")
    print()
    input("  Premi INVIO per continuare...")
 
def turno_ingaggio():
    ruoli_lista = list(RUOLI.keys())
    stampa_stato()
 
    c = conteggio_ruoli()
    n = totale_equipaggio()
    ruoli_mancanti = [r for r in RUOLI if c[r] == 0]
    puo_salpare = (n >= 5 and len(ruoli_mancanti) == 0)
 
    print("  1) Aggiungi membri")
    if puo_salpare:
        print("  2) Salpa!")
    else:
        if ruoli_mancanti:
            mancanti_str = ""
            for r in ruoli_mancanti:
                mancanti_str += r + ", "
            mancanti_str = mancanti_str[:-2]
        else:
            mancanti_str = f"minimo 5 persone ({n}/5)"
        print(f"  2) Salpa! (non disponibile – mancano: {mancanti_str})")
 
    scelta = input_intero("  Scelta: ", minimo=1, massimo=2)
 
    if scelta == 2:
        if puo_salpare:
            riepilogo_finale()
            return
        else:
            print("  Non puoi ancora salpare.")
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
    print("INGAGGIO DELLA FLOTTA")
    print("=" * 50)
    print()
    print("  Monete disponibili: 2000")
    print("  Minimo 5 persone, almeno 1 per ruolo. Massimo 16.")
    print()
    print("  Paghe settimanali:")
    for ruolo, dati in RUOLI.items():
        print(f"    {ruolo.capitalize():<12} {dati['paga_settimanale']} monete/sett.")
    print()
    turno_ingaggio()
 
#fase_ingaggio()
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
nuovi_membri=  {
    1: {
        "ruolo": "cuoco",
        "paga_settimanale": 15,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    }
}
 
 
 
equipaggio ={
    1: {
        "ruolo": "medico",
        "paga_settimanale": 25,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    2: {
        "ruolo": "navigatore",
        "paga_settimanale": 20,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    3: {
        "ruolo": "meccanico",
        "paga_settimanale": 15,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    4: {
        "ruolo": "cuoco",
        "paga_settimanale": 15,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    5: {
        "ruolo": "marinaio",
        "paga_settimanale": 10,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    6: {
        "ruolo": "marinaio",
        "paga_settimanale": 10,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    7: {
        "ruolo": "marinaio",
        "paga_settimanale": 10,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    }
}
 
 
 
 
 
 
merci={"medicinali":4,"armi":2,"sale":100,"stoffa":100,"coltelli":100 ,"diamanti":100}
 
 
 
 
 
 
import random
#si potrebbe fare una lista con all'interno ogni evento, e per ogni if si elimina poi l'evento dalla lista, facendo di volta in volta i-1 per trovare quello della settimana successiva
 
settimane=8
"""
equipaggio = [
    {"ruolo": "meccanicoxx", "morale": 100},
    {"ruolo": "meccanicoa", "morale": 100},
    {"ruolo": "cuoco",     "morale": 100},
    {"ruolo": "marinaio",  "morale": 100},
]
"""
ruoli_costi={"cuoco":15,"marinaio":10,"meccanico":15,"medico":25,"navigatore":20}
"""
equipaggiamento={"verdura":100,"carne":100,"acqua":100,"frutta":100,"medicinali":100,"armi":100,"stoffe":100}"""
qta_da_perdere=[0.5, 0.33 ,0.25, 0.2 ]
 
 
equipaggiamento={
    "verdura": {"qta":100,"prezzo":0.5},
    "acqua": {"qta":100,"prezzo":0.5},
    "carne": {"qta":100,"prezzo":0.5},
    "frutta": {"qta":100,"prezzo":0.5},
 
 
    "medicinali": {"qta":100,"prezzo":0.5},
    "armi": {"qta":1,"prezzo":0.5},
    "stoffe": {"qta":100,"prezzo":0.5},
}
 
 
 
#!!############################à       FUNZIONI FUNZIONALI GAMEPLAY
def si_no(domanda_dec):
   corretto=False
   while corretto!=True:
       decisione_ut=input(f"{domanda_dec} (si/no)").lower().strip()
       if decisione_ut=="si": return True
       elif decisione_ut=="no":return False
       else:
           print("l'input non è stato inserito correttamente   è si o no")
 
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
        if membro["ruolo"] == ruolo_ind and membro["vivo"]==True:
            presenza_ruolo=True
            return presenza_ruolo
ris=ce_ruolo(equipaggio,"medico")
print(ris,"aaaaaa")
#!!############################à #!!############################à #!!############################à
 
 
 
 
 
 
 
 
 
 
 
#?FUNZIONIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
 
 
 
#TODO _________________________ ATTENTO QUA MILA è PER ALBATRO
colpito=None
 
 
#* PROVA UNICAAA------------------           questo ha messaggi persolizzati, sennò devo fare il print nell'if
def prova_unica(equipaggiamento_in,oggetto,qta_perdere_0):   #?   VERDURA
    qta_persa=random.choice(qta_perdere_0)
    peso_perso=equipaggiamento_in[oggetto]["qta"]*qta_persa
    equipaggiamento_in[oggetto]["qta"]-=peso_perso
    return equipaggiamento_in,peso_perso
   
 
 
#!prova_unica(equipaggiamento,"verdura",qta_da_perdere) QUA CHIAMATA
 
 
def tempesta_miracolosa(equipaggiamento_in,oggetto):   #? + ACQUA    # va bene anche per carne ---> modifica il nome chiave come parametro
    qta_guadagnata=random.randint(11,20)
    equipaggiamento_in[oggetto]["qta"]+=qta_guadagnata
    return equipaggiamento_in,qta_guadagnata
 
#!tempesta_miracolosa(equipaggiamento,"acqua")        QUA CHIAMATA
 
 
 
 
#------------------------------------EVENTI    RIGIUARDANTI SETTIMANE
#? BOZZA PER SE C'è EQUIPAGGIO x ...
def raffiche_di_vento(equipaggio_in,settimane_int,ruolo_ind):   #!!
    presenza_ruolo=False
    for membro in equipaggio_in.values():
        if membro["ruolo"] == ruolo_ind and membro["vivo"]==True:
            presenza_ruolo=True
           
           
    if presenza_ruolo==True:
        settimane_int+=1
        #RICORDA SCRITTA IN BASE A CHIAMATA
        #print("aaa")
        return 1,settimane_int,presenza_ruolo
    else:
        sett_casuale=random.randint(2,4)
        settimane_int+=sett_casuale
        #RICORDA SCRITTA IN BASE A CHIAMATA
        print(settimane_int)
        #print("bbbb")
        return sett_casuale,settimane_int,presenza_ruolo
 
 
 
 
 
 
def uomo_in_mare(equipaggio_in):
    eq_vivi=[]
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True:
            eq_vivi.append(i)
    morto=random.choice(eq_vivi)
    equipaggio_in[morto]["vivo"]=False
   
    #print(eq_vivi)
    return f"{equipaggio_in[morto]["ruolo"]}"
 
 
 
def vento_favorevole(settimane_in,equipaggio_in):
    morale_piu=random.randint(5,15)
    #print(morale_piu,"aaaaaaa")
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True:
            equipaggio_in[i]["morale"]+=morale_piu
           
    settimane_in-=1        
    return equipaggio_in,settimane_in,morale_piu
 
 
 
 
 
 
#ALBATROOO
def avvistamento_albatro(equipaggio_in,merci_in, funz_decisione,funz_n_vivi,min_sparo,equipaggiamento_in):
    n_armi=merci_in["armi"]
    colpito=False
    conta_armi=0
    if n_armi>=1:
        domanda=f"gli si vuole sparare? "
        decisione_abbatimento=funz_decisione(domanda)
        if decisione_abbatimento==True:
            tentativi_sparare=min_sparo(equipaggio_in,merci_in,funz_n_vivi)
            for i in range(tentativi_sparare):
                colpito=random.randint(0,1)
                merci_in["armi"]-=1
                conta_armi+=1
                if colpito==1:
                    qta_cas_carne=random.randint(10,15)
                    equipaggiamento_in["carne"]["qta"]+=qta_cas_carne
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
        for i in range (4):
            
            nuovo_id=max(equipaggio_in.keys())+1
            morale_cas=random.randint(25,75)
            ruoli=list(ruoli_base.keys())
            ruolo_cas=random.choice(ruoli)
            
            naufrago_creato={
            "ruolo":ruolo_cas,
            "paga_settimanale":ruoli_base[ruolo_cas],
            "morale":morale_cas,
            "vivo":True,
            "ingaggiato":False
            }
            equipaggio_in[nuovo_id]=naufrago_creato
        for i in merci_in:
            merci_cas=random.randint(10,20)
            merci_in[i]+=merci_cas
        return decisione,merce_iniziale


def epidemia(equipaggio_in,merci_in,ce_medico):
    conta_malati=0
    conta_morti=0
    conta_guariti=0
    medicinali_persi=0
    presenza_med=ce_medico(equipaggio_in,"medico")
    for i in equipaggio_in:
        if equipaggio_in[i]["vivo"]==True and equipaggio_in[i]["ruolo"] != "medico":
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
    return conta_malati,conta_morti,conta_guariti,medicinali_persi

def attacco_pirata(equipaggio_in,funz_conta_vivi,merci_in,funz_min_sparo):
    n_pirati=random.randint(3,10)
    n_vivi=funz_conta_vivi(equipaggio_in)
    n_difensori=funz_min_sparo(equipaggio_in, merci_in, funz_conta_vivi)
    merci_in["armi"]-=n_difensori
    uomini_persi=min(n_pirati-n_difensori,n_vivi)
    #print(uomini_persi,n_pirati)
    
    if uomini_persi>=1:
        eq_vivi=[]
        for i in equipaggio_in:
            if equipaggio_in[i]["vivo"]==True:
                eq_vivi.append(i)
        for j in range(uomini_persi):
            morto=random.choice(eq_vivi)
            equipaggio_in[morto]["vivo"]=False
            eq_vivi.remove(morto)
    
    return uomini_persi,n_pirati,n_difensori



def avvistamento_isola(funz_dec,albatro_morto,merci_in):
    domanda="viene avvistata un isola, ci si vuole andare??"
    risposta=funz_dec(domanda)
    if risposta==False:
        return "non raggiunta",None,None
    else:
        sett_aggiuntive=random.randint(1,2)
        prob_abit=random.randint(0,1)
        if prob_abit==0:
            return "non abitata",None,sett_aggiuntive  #* ABITATA-OSTILE-MERCI_PREC
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
    



#for i in range (settimane):       #!FOR INIZIALEEEEEEEEEE
#n_evento=random.randint(0,12)
#*"""        
#               TOGLI IN CASO DI DEBUG LE DUE RIGHE CON STO COLORE

#n_evento=13  #*TOGLIERE IN CASO DEBUG
 
conta_set=0
while settimane!=conta_set:

    n_evento=random.randint(0,18)
    print(f"⏱️⏱️-----SETTIMANA {conta_set}----- ⏱️⏱️")
    
    if  n_evento==0:
        pg_morto=uomo_in_mare(equipaggio)
        print(f"---EVENTO UMOMO IN MARE--- \n  il {pg_morto.upper()} è caduto in mare ed è MORTO")
    elif n_evento==1:
        equipaggiamento,perdite_verdure=prova_unica(equipaggiamento,"verdura",qta_da_perdere)
        print(f"---EVENTO VERDURA IN MARE--- \n   una violenta tempesta ha trasportato in mare delle casse che contenevano {perdite_verdure} Kg di VERDURE  ")
    elif n_evento==2:
        equipaggiamento,perdite_frutta=prova_unica(equipaggiamento,"frutta",qta_da_perdere)
        print(f"---EVENTO FRUTTA IN MARE--- \n   una violenta tempesta ha trasportato in mare delle casse che contenevano {perdite_frutta} Kg di FRUTTA  ")
    elif n_evento==3:
        equipaggiamento,perdite_carne=prova_unica(equipaggiamento,"carne",qta_da_perdere)
        print(f"---EVENTO CARNE IN MARE--- \n   una violenta tempesta ha trasportato in mare delle casse che contenevano {perdite_carne} Kg di CARNE  ")
    
    elif n_evento==4:
        equipaggiamento,perdite_acqua=prova_unica(equipaggiamento,"acqua",qta_da_perdere)
        print(f"---EVENTO ACQUA IN MARE--- \n   una violenta tempesta ha trasportato in mare  {perdite_acqua} BARILI D'ACQUA  ")
    # piu materiale
    elif n_evento==5:
        equipaggiamento,qta_pescata=tempesta_miracolosa(equipaggiamento,"carne")
        print(f"---EVENTO APESCA MIRACOLOSA--- \n durante la settimana di quiete l'equipaggio ha pescato {qta_pescata} kg di CARNE ")
    
    elif n_evento==6:
        equipaggiamento,qta_acqua=tempesta_miracolosa(equipaggiamento,"acqua")
        print(f"---EVENTO TEMPESTA MIRACOLOSA --- \n durante la tempesta dei coraggiosi uomini hanno riempito d'ACQUA {qta_acqua} BARILI VUOTI ")
    # PIU MORALE E MENO 1 SETT
    elif n_evento==7:
        equipaggio,settimane,morale_agg=vento_favorevole(settimane,equipaggio)
        print(f"---EVENTO VENTO FAVOREVOLE--- \n un vento favorevole, permette di ACCORCIARE di 1 SETTIMANA il viaggio \n ogni membro dell'equipaggio AUMENTA il MORALE di {morale_agg}")
        #print(equipaggio)
    
    #perdita mat utilizzabile
    elif n_evento==8:
        equipaggiamento,perdite_medicinali=prova_unica(equipaggiamento,"medicinali",qta_da_perdere)
        print(f"---EVENTO CATTIVO TEMPO--- \n   il cattivo tempo ha rovesciato {perdite_medicinali} BOTTIGLIE DI MEDICINALI")
    elif n_evento==9:
        equipaggiamento,perdite_armi=prova_unica(equipaggiamento,"armi",qta_da_perdere)
        print(f"---EVENTO ONDATA--- \n   una onda altissima ha trasportato in mare {perdite_armi} ARMI")
    elif n_evento==10:
        equipaggiamento,perdite_stoffe=prova_unica(equipaggiamento,"stoffe",qta_da_perdere)
        print(f"---EVENTO INFESTAZIONE RATTI--- \n   dei RATTI hanno mordicchiato e rovinato {perdite_stoffe} STOFFE  :(")
    


    elif n_evento==11:#!ALBATRO
        print(f"---EVENTO: AVVISTAMENTO ALBATRO--- \n in cielo viene avvistato un albatro, in caso di abbattimento vi sarà un aumento della scorta di CARNE ")
        colpito,merci,decisone_sparo,qta_guad,armi_utilizzate=avvistamento_albatro(equipaggio,merci,si_no,conta_vivi,Min_sparo_difesa,equipaggiamento)
        if decisone_sparo==True:
            if colpito==True:
                print(f"l'albatro è stato abbattuto, sono state state utilizzate {armi_utilizzate} ARMI, e l'equipaggio ha raccolto {qta_guad} di CARNE")
            else:print(f"l'albatro non è stato colpito, sono state usate/a {armi_utilizzate} ARMI")
        else:print("L'equipaggio non ha voluto sparare all'albatro, il viaggio prosegue")


    elif n_evento==12: #!SCIALUPPA
        print(f"---EVENTO: AVVISTAMENTO SCIALUPPA---\n  viene avvistata una scialuppa con 4 uomini")
        deciosione_scialuppa,merci_precedente=avvistamento_scialuppa(si_no,merci,RUOLI,equipaggio)
        if deciosione_scialuppa==True:
            uomini_id=list(equipaggio.keys())
            naufraghi_id=uomini_id[-4:]
            print(naufraghi_id)

            print(f"gli uomini sono stati salvati, e hanno le seguenti caratteristiche:")
            for id in naufraghi_id:
                
                print(f"{equipaggio[id]["ruolo"].upper()} con morale: {equipaggio[id]["morale"]}")
            print("dai naufraghi sono stati recuperati (quantità/kg):")
            for m in merci:
                qta_recuperata=merci[m]-merci_precedente[m]
                print(qta_recuperata,m )


    elif n_evento==13: #!EPIDEMIA
        print(f"---EVENTO: EPIDEMIA---\n  L'epidemia si abbatte sull'equipaggio")
        n_malati,n_morti,n_guariti,medicinali_usati=epidemia(equipaggio,merci,ce_ruolo)
        print(f"l'epidemia ha portato {n_malati} MALATI, di cui {n_morti} sono MORTI")
        if n_guariti>=1:
            print(f"grazie alla presenza del medico, sono stati curati {n_guariti} membri, ma sono state usate {medicinali_usati} bottiglie di MEDICINALE")

    elif n_evento==14:
        n_morti_xpir,num_pirati,n_armi_usate=attacco_pirata(equipaggio, conta_vivi,merci,Min_sparo_difesa)
        print(f"---EVENTO: ATTACCO PIRATA---\n  una nave composta da {num_pirati} pirati, sferra un attacco \n sono morti {n_morti_xpir} membri dell tuo equipaggio, e sono state usate {n_armi_usate} ARMI"  )

    elif n_evento==15:
        giorni_in_piu,settimane,presenza_salvatore=raffiche_di_vento(equipaggio,settimane,"meccanico")
        if presenza_salvatore==True:
            print(f"---EVENTO: DANNI AL TIMONE--- \n l'urto con lo scoglio ha causato la rottura del timone il viaggio si allunga di {giorni_in_piu} settimana  \n GRAZIE AL MECCANICO il danno è stato riparato in fretta")
        else:
            print(f"---EVENTO: DANNI AL TIMONE--- \n l'urto con lo scoglio ha causato la rottura del timone il viaggio si allunga di {giorni_in_piu} settimane \n per via dell'ASSENZA DEL MECCANICO il timone viene riparato mooolto lentamente")

    elif n_evento==16:
        giorni_in_piu,settimane,presenza_salvatore=raffiche_di_vento(equipaggio,settimane,"navigatore")
        if presenza_salvatore==True:
            print(f"---EVENTO: RAFFICHE DI VENTO--- \n a causa di FORTI RAFFICHE DI VENTO la nave si allontana dalla rotta iniziale, il viaggio si allunga di {giorni_in_piu} settimana  \n GRAZIE AL NAVIGATORE la situazione è stata risolta velocemente")
        else:
            print(f"---EVENTO: RAFFICHE DI VENTO--- \n a causa di FORTI RAFFICHE DI VENTO la nave si allontana dalla rotta iniziale, il viaggio si allunga di {giorni_in_piu} settimane  \n per via dell' ASSENZA DEL NAVIGATORE la situazione è stata risolta mooolto lentamente")


    elif n_evento==17:
        dec_ab_isola,merce_precedente,sett_in_piu=avvistamento_isola(si_no,colpito,merci)
        
        if dec_ab_isola=="non raggiunta":
            print("l'equipaggio a preferito non raggiungere l'isola, il viaggio prosegue")
        elif dec_ab_isola=="non abitata":
            settimane += sett_in_piu
            print(f"l'isola non è abitata, l'equipaggio prosegue il viaggio, esso si allunga di {sett_in_piu} SETTIMANE")

        elif dec_ab_isola=="ostile":
            settimane += sett_in_piu
            print(f"l'isola è ostile, l'equipaggio scappa dall'isola, il viaggio si allunga di {sett_in_piu} SETTIMANE ")
        elif dec_ab_isola=="abitata":
            settimane += sett_in_piu
            print(f"l'isola è abitata,, il viaggio si allunga di {sett_in_piu} SETTIMANE... l'equipaggio riceve dalla popolazione locale i seguenti doni:  ")
            for m in merci:
                qta_recuperata=merci[m]-merce_precedente[m]
                print(qta_recuperata,m )

    elif n_evento==18:
        print("NON SUCCEDE NULLA DI SPECIALE DURANTE LA SETTIMANA")
    conta_set+=1
    p=input("premi qualsiasi tasto per andare avanti")
    #*"""

    #TODO   RICORDA DI METTER APPROSSIMAZIONE DEI VALORI Kg PERSI perchè fa tipo 9.000000000001   se capita
    #TODO SE COLPITO ALBATRO=AMMUTINAMENTO EGLIO METTERLO IN PROG PRINCIPALE O FARE FUNZIONE PER ESSO
 