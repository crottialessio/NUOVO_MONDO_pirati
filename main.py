#equipaggio: dizionario di dizionari ---> diz{cuoco:{Paga:30,Cibo:20kg,Numero:1}, ...}
#equipaggiamento (armi cibo ecc..): dizioanrio 
#merci(stoffa diamanti sale): dizionario di dizionari bettinelli molotov


















































































































































































































































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

def Calcolo_Membri(stato_gioco):
    equipaggio = stato_gioco["equipaggio"]["cuoco"] + stato_gioco["equipaggio"]["marinaio"] + stato_gioco["equipaggio"]["meccanico"] + stato_gioco["equipaggio"]["medico"] + stato_gioco["equipaggio"]["navigatore"]
    return equipaggio

def Calcolo_cibo_1_sett(CATALOGO_CIBO,stato_gioco):
    membri_vivi = Calcolo_Membri(stato_gioco)
    verdura = CATALOGO_CIBO["verdura"]["consumo"] * membri_vivi
    frutta = CATALOGO_CIBO["frutta"]["consumo"] * membri_vivi
    carne = CATALOGO_CIBO["carne"]["consumo"] * membri_vivi
    acqua = CATALOGO_CIBO["acqua"]["consumo"] * membri_vivi
    return [verdura,frutta,carne,acqua]

def Sottrai_consumo_settimana(stato_gioco, CATALOGO_CIBO, moltiplicatori_razioni):
    cibi = Calcolo_cibo_1_sett(CATALOGO_CIBO, stato_gioco)
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
    Sottrai_consumo_settimana(stato_gioco, CATALOGO_CIBO, moltiplicatori)
    
    cibi = Calcolo_cibo_1_sett(CATALOGO_CIBO, stato_gioco)
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

    if albatro is True:
        scoperto = True
    elif albatro is None:
        scoperto = random.randint(1, 2) == 1

    return scoperto


def calcolo_settimane_e_rifornimento(stato_gioco,albatro, CATALOGO_CIBO):
    cibi=Calcolo_cibo_1_sett(CATALOGO_CIBO)
    
    stato_gioco["cibo"]["verdura"] +=cibi[0] * 3
    stato_gioco["cibo"]["frutta"] += cibi[1] * 3
    stato_gioco["cibo"]["carne"] += cibi[2] * 3
    stato_gioco["cibo"]["acqua"] += cibi[3] * 3

    if stato_gioco["equipaggio"]["navigatore"] >= 1:
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

def Calcolo_spesa_equipaggio(stato_gioco,RUOLI,settimane):
    spesa_equip=(
        (stato_gioco["equipaggio"]["cuoco"]* RUOLI["cuoco"]["paga_settimanale"]*settimane)+
        (stato_gioco["equipaggio"]["marinaio"]* RUOLI["marinaio"]["paga_settimanale"]*settimane)+
        (stato_gioco["equipaggio"]["meccanico"]* RUOLI["meccanico"]["paga_settimanale"]*settimane)+
        (stato_gioco["equipaggio"]["medico"]* RUOLI["medico"]["paga_settimanale"]*settimane)+
        (stato_gioco["equipaggio"]["navigatore"]* RUOLI["navigatore"]["paga_settimanale"]*settimane)
        )
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