
 
















































 
















































 
















































 
















































 
















































 
















































 
















































 





















































import random

RUOLI={"cuoco":{"paga_settimanale":15},"marinaio":{"paga_settimanale":10},"meccanico":{"paga_settimanale":15},"medico":{"paga_settimanale":25},"navigatore":{"paga_settimanale":20}}
colpito=None
stato_gioco = {
    "monete":       2000,
    "monete_spese": 0,
    "equipaggio":   {
        1: {
            "ruolo": "medico",
            "paga_settimanale": 90,
            "morale": 100,
            "vivo": True,
            "ingaggiato": True
        },
        2: {
            "ruolo": "navigatore",
            "paga_settimanale": 80,
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
            "vivo": False,
            "ingaggiato": True
        },
        7: {
            "ruolo": "marinaio",
            "paga_settimanale": 10,
            "morale": 100,
            "vivo": True,
            "ingaggiato": True
        }
    },
    "prossimo_id":  8,
    "cibo":         {
        "verdura": 100.0,
        "frutta":  100.0,
        "carne":   100.0,
        "acqua":   100.0,
    },
    "merci":        {
        "medicinali": 4,
        "armi":       2,
        "sale":       100,
        "stoffa":     100,
        "coltelli":   100,
        "diamanti":   100,
    },
}
ruoli_costi={"cuoco":15,"marinaio":10,"meccanico":15,"medico":25,"navigatore":20}
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
li_eventi=[0,1,2,3,4,5,6,7,8,9,10,11,90,91,12,13,14,15,16,17]
conta_set=1
punti_ammutinamento=0
game_over=False
#>= perchè se faccio +2 verso la fine il gioco fa aanti tanto
while settimane>=conta_set and game_over!=True and punti_ammutinamento<100:
    
    if conta_vivi(stato_gioco["equipaggio"])==0:
        print("tutti i membri sono morti, il gioco finisce qui, GAME OVER")
        game_over=True
    else:

        n_evento=random.choice(li_eventi)
        
        
        print(f"⏱️⏱️-----SETTIMANA {conta_set}----- ⏱️⏱️")
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
            li_eventi.remove(n_evento)
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
