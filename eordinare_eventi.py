





















equipaggio = {
    1: {
        "ruolo": "navigatore",
        "paga_settimanale": 15,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    2: {
        "ruolo": "meccanico",
        "paga_settimanale": 25,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    },
    3: {
        "ruolo": "marinaio",
        "paga_settimanale": 10,
        "morale": 100,
        "vivo": True,
        "ingaggiato": True
    }
}














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
    "armi": {"qta":100,"prezzo":0.5},
    "stoffe": {"qta":100,"prezzo":0.5},
}



#* PROVA UNICAAA------------------           questo ha messaggi persolizzati, sennò devo fare il print nell'if
def prova_unica(equipaggiamento_in,oggetto,qta_perdere_0):   #?   VERDURA
    qta_persa=random.choice(qta_perdere_0)
    print(qta_persa)
    peso_perso=equipaggiamento_in[oggetto]["qta"]*qta_persa
    equipaggiamento_in[oggetto]["qta"]-=peso_perso
    return equipaggiamento_in,peso_perso


#!prova_unica(equipaggiamento,"verdura",qta_da_perdere) QUA CHIAMATA


def tempesta_miracolosa(equipaggiamento_in,oggetto):   #? + ACQUA    # va bene anche per carne ---> modifica il nome chiave come parametro
    qta_guadagnata=random.randint(11,20)
    #print(qta_guadagnata)
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




conta_set=1
#for i in range (settimane):       #!FOR INIZIALEEEEEEEEEE
n_evento=random.randint(0,4)
#*"""        
#               TOGLI IN CASO DI DEBUG LE DUE RIGHE CON STO COLORE
n_evento=9
print(f"-----SETTIMANA {conta_set}")












n_evento=12



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
    print(f"durante la settimana di quiete l'equipaggio ha pescato {qta_pescata} kg di CARNE ") 

elif n_evento==6:
    equipaggiamento,qta_acqua=tempesta_miracolosa(equipaggiamento,"acqua")
    print(f"durante la tempesta dei coraggiosi uomini hanno riempito d'ACQUA {qta_acqua} BARILI VUOTI ")

#! 7 è venti favorevoli


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

#IN BASE A PRESENZA RUOLO
elif n_evento==11:
    giorni_in_piu,settimane,presenza_salvatore=raffiche_di_vento(equipaggio,settimane,"meccanico") 
    if presenza_salvatore==True:
        print(f"EVENTO: DANNI AL TIMONE \n l'urto con lo scoglio ha causato la rottura del timone il viaggio si allunga di {giorni_in_piu} settimana  \n GRAZIE AL MECCANICO il danno è stato riparato in fretta")
    else:
        print(f"EVENTO: DANNI AL TIMONE \n l'urto con lo scoglio ha causato la rottura del timone il viaggio si allunga di {giorni_in_piu} settimane \n per via dell'ASSENZA DEL MECCANICO il timone viene riparato mooolto lentamente")
elif n_evento==12:
    giorni_in_piu,settimane,presenza_salvatore=raffiche_di_vento(equipaggio,settimane,"navigatore") 
    if presenza_salvatore==True:
        print(f"EVENTO: RAFFICHE DI VENTO \n a causa di FORTI RAFFICHE DI VENTO la nave si allontana dalla rotta iniziale, il viaggio si allunga di {giorni_in_piu} settimana  \n GRAZIE AL NAVIGATORE la situazione è stata risolta velocemente")
    else:
        print(f"EVENTO: RAFFICHE DI VENTO \n a causa di FORTI RAFFICHE DI VENTO la nave si allontana dalla rotta iniziale, il viaggio si allunga di {giorni_in_piu} settimane  \n per via dell' ASSENZA DEL NAVIGATORE la situazione è stata risolta mooolto lentamente")


conta_set+=1 
