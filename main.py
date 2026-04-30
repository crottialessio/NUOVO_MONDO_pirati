#equipaggio: dizionario di dizionari ---> diz{cuoco:{Paga:30,Cibo:20kg,Numero:1}, ...}
#equipaggiamento (armi cibo ecc..): dizioanrio 
#merci(stoffa diamanti sale): dizionario di dizionari bettinelli molotov






















































































































































































































































merci_baratto = {
    "perla": {
        "sale":           0.5,
        "stoffa":         5,
        "coltello":       1,
        "diamanti":       2,
        "prezzo stimato": 2
    },
    "manufatto": {
        "sale":           0.5,
        "stoffa":         7,
        "coltello":       3,
        "diamanti":       4,
        "prezzo stimato": 2
    },
    "barattolo di spezie": {
        "sale":           1,
        "stoffa":         3,
        "coltello":       6,
        "diamanti":       4,
        "prezzo stimato": 1
    }
}

def baratto(merci_baratto, provviste):
    print("=" * 50)
    print("IL CAPO TRIBÙ TI OFFRE DEI COMMERCI")
    print("Rifiuta armi e medicinali: si barattano solo sale, stoffa, coltelli e diamanti.")
    print("=" * 50)
    
    if provviste["sale"] >= 0.5:
        print("\n--- BARATTO: SALE ---")
        print("Offrirai tutti i tuoi sacchi di sale. Scegli una sola opzione:")
        perle = provviste["sale"]/merci_baratto["perla"]["sale"]
        manufatti = provviste["sale"]/merci_baratto["manufatto"]["sale"]
        spezie = provviste["sale"]/merci_baratto["barattolo di spezie"]["sale"]

        print(f"  1) {perle:.0f} perle        (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']:.0f} dobloni)")
        print(f"  2) {manufatti:.0f} manufatti   (rivendibili a {merci_baratto['manufatto']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatto']['prezzo stimato']:.0f} dobloni)")
        print(f"  3) {spezie:.0f} spezie       (rivendibili a {merci_baratto['barattolo di spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['barattolo di spezie']['prezzo stimato']:.0f} dobloni)")
        
        corretto = False
        while not corretto:
            scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
            
            if scelta not in ["1", "2", "3"]:
                print("  Scelta non valida, riprova.")

            elif scelta == "1":
                provviste["sale"] = 0
                provviste["perle"] += perle
                print(f"  Hai ottenuto {perle:.0f} perle!")
                corretto = True

            elif scelta == "2":
                provviste["sale"] = 0
                provviste["manufatti"] += manufatti
                print(f"  Hai ottenuto {manufatti:.0f} manufatti!")
                corretto = True
            
            elif scelta == "3":
                provviste["sale"] = 0
                provviste["barattolo di spezie"] += spezie
                print(f"  Hai ottenuto {spezie:.0f} barattoli di spezie!")
                corretto = True

    if provviste["stoffa"] >= 3:
        print("\n--- BARATTO: STOFFA ---")
        print("Offrirai tutti i tuoi teli di stoffa. Scegli una sola opzione:")
        perle = provviste["stoffa"]/merci_baratto["perla"]["stoffa"]
        manufatti = provviste["stoffa"]/merci_baratto["manufatto"]["stoffa"]
        spezie = provviste["stoffa"]/merci_baratto["barattolo di spezie"]["stoffa"]

        print(f"  1) {perle:.0f} perle        (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']:.0f} dobloni)")
        print(f"  2) {manufatti:.0f} manufatti   (rivendibili a {merci_baratto['manufatto']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatto']['prezzo stimato']:.0f} dobloni)")
        print(f"  3) {spezie:.0f} spezie       (rivendibili a {merci_baratto['barattolo di spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['barattolo di spezie']['prezzo stimato']:.0f} dobloni)")
        
        corretto = False
        while not corretto:
            scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
            
            if scelta not in ["1", "2", "3"]:
                print("  Scelta non valida, riprova.")

            elif scelta == "1":
                provviste["stoffa"] = 0
                provviste["perle"] += perle
                print(f"  Hai ottenuto {perle:.0f} perle!")
                corretto = True

            elif scelta == "2":
                provviste["stoffa"] = 0
                provviste["manufatti"] += manufatti
                print(f"  Hai ottenuto {manufatti:.0f} manufatti!")
                corretto = True
            
            elif scelta == "3":
                provviste["stoffa"] = 0
                provviste["barattolo di spezie"] += spezie
                print(f"  Hai ottenuto {spezie:.0f} barattoli di spezie!")
                corretto = True

    if provviste["coltelli"] >= 1:
        print("\n--- BARATTO: COLTELLI ---")
        print("Offrirai tutti i tuoi coltelli. Scegli una sola opzione:")
        perle = provviste["coltelli"]/merci_baratto["perla"]["coltello"]
        manufatti = provviste["coltelli"]/merci_baratto["manufatto"]["coltello"]
        spezie = provviste["coltelli"]/merci_baratto["barattolo di spezie"]["coltello"]

        print(f"  1) {perle:.0f} perle        (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']:.0f} dobloni)")
        print(f"  2) {manufatti:.0f} manufatti   (rivendibili a {merci_baratto['manufatto']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatto']['prezzo stimato']:.0f} dobloni)")
        print(f"  3) {spezie:.0f} spezie       (rivendibili a {merci_baratto['barattolo di spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['barattolo di spezie']['prezzo stimato']:.0f} dobloni)")
        
        corretto = False
        while not corretto:
            scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
            
            if scelta not in ["1", "2", "3"]:
                print("  Scelta non valida, riprova.")

            elif scelta == "1":
                provviste["coltelli"] = 0
                provviste["perle"] += perle
                print(f"  Hai ottenuto {perle:.0f} perle!")
                corretto = True

            elif scelta == "2":
                provviste["coltelli"] = 0
                provviste["manufatti"] += manufatti
                print(f"  Hai ottenuto {manufatti:.0f} manufatti!")
                corretto = True
            
            elif scelta == "3":
                provviste["coltelli"] = 0
                provviste["barattolo di spezie"] += spezie
                print(f"  Hai ottenuto {spezie:.0f} barattoli di spezie!")
                corretto = True

    if provviste["diamanti"] >= 2:
        print("\n--- BARATTO: DIAMANTI ---")
        print("Offrirai tutti i tuoi diamanti. Scegli una sola opzione:")
        perle = provviste["diamanti"]/merci_baratto["perla"]["diamanti"]
        manufatti = provviste["diamanti"]/merci_baratto["manufatto"]["diamanti"]
        spezie = provviste["diamanti"]/merci_baratto["barattolo di spezie"]["diamanti"]

        print(f"  1) {perle:.0f} perle        (rivendibili a {merci_baratto['perla']['prezzo stimato']} dobloni l'una  - totale stimato: {perle*merci_baratto['perla']['prezzo stimato']:.0f} dobloni)")
        print(f"  2) {manufatti:.0f} manufatti   (rivendibili a {merci_baratto['manufatto']['prezzo stimato']} dobloni l'uno  - totale stimato: {manufatti*merci_baratto['manufatto']['prezzo stimato']:.0f} dobloni)")
        print(f"  3) {spezie:.0f} spezie       (rivendibili a {merci_baratto['barattolo di spezie']['prezzo stimato']} doblone l'uno  - totale stimato: {spezie*merci_baratto['barattolo di spezie']['prezzo stimato']:.0f} dobloni)")
        
        corretto = False
        while not corretto:
            scelta = input("\nQuale scambio vuoi effettuare? (1, 2 o 3): ").strip()
            
            if scelta not in ["1", "2", "3"]:
                print("  Scelta non valida, riprova.")

            elif scelta == "1":
                provviste["diamanti"] = 0
                provviste["perle"] += perle
                print(f"  Hai ottenuto {perle:.0f} perle!")
                corretto = True

            elif scelta == "2":
                provviste["diamanti"] = 0
                provviste["manufatti"] += manufatti
                print(f"  Hai ottenuto {manufatti:.0f} manufatti!")
                corretto = True
            
            elif scelta == "3":
                provviste["diamanti"] = 0
                provviste["barattolo di spezie"] += spezie
                print(f"  Hai ottenuto {spezie:.0f} barattoli di spezie!")
                corretto = True

    print("\n" + "=" * 50)
    print("BARATTO CONCLUSO!")
    print("Ecco il resoconto, hai ottenuto:")
    print(f"  Perle:            {provviste['perle']:.0f} - totale stimato: {provviste['perle'] * merci_baratto['perla']['prezzo stimato']:.0f} dobloni")
    print(f"  Manufatti:        {provviste['manufatti']:.0f} - totale stimato: {provviste['manufatti'] * merci_baratto['manufatto']['prezzo stimato']:.0f} dobloni")
    print(f"  Barattoli spezie: {provviste['barattolo di spezie']:.0f} - totale stimato: {provviste['barattolo di spezie'] * merci_baratto['barattolo di spezie']['prezzo stimato']:.0f} dobloni")
    print("=" * 50)

baratto(merci_baratto, provviste)




