# This Python file uses the following encoding: utf-8
import time
import math
import copy
from Lan import Lan
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
        
class Notandi(object):
    def __init__(self, Greidhslugeta):

        self.innlaen=[] #sparnadhur Notanda 
        self.uetlaen=[] #skuldir Notanda
        self.Greidhslugeta = Greidhslugeta
        self.Dagsetning = date.today() #dagsetning er dagsetning næstu mánaðargreiðslu
        # Þegar næsti mánuður er með færri daga og óuppfærð dagsetninginn er t.d. 31. mánaðarins 
        # uppfærist hún til síðasta dags næsta mánaðar
        
    
    # Fyrir: innlaen og uetlaen eru ekki báðir tómir
    # Eftir: Skilar vísunn á þann lan hlut með hæstu vextina - fyrir bestunarreikninga 
    def HajstuVextir(self):
        if len(self.innlaen) > 0:
            skil = self.innlaen[0]
        else:
            skil = self.uetlaen[0]
            
        for skuld in self.uetlaen:
            if skuld.vextir > skil.vextir:
                skil = skuld
        for sparnadhur in self.innlaen:
            if sparnadhur.vextir > skil.vextir:
                skil = sparnadhur
        return skil
    

    # Eftir: Fall sem reiknar stöðuna eftir ákveðinn fjölda mánuða
    # Reiknað er með að innborgun berist á undan vaxtatöku.
    # M.ö.o. er reiknað með að innborgunardagur sé mánaðardagur í self.Dagsetning
    def stoedhuUppfajrsla(self, maenudhir):
        for i in range(0, maenudhir):
            self.Dagsetning += relativedelta(months=1)
            for sparnadhur in self.innlaen:
                sparnadhur.upphaed += sparnadhur.maenadharlegInnborgun
                if sparnadhur.gjalddagi - self.Dagsetning <= timedelta(0) :
                    sparnadhur.upphaed *=  (1.0 + (sparnadhur.vextir/100.0))
                    sparnadhur.upphaed = math.floor(sparnadhur.upphaed) #better safe than sorry
                    sparnadhur.gjalddagi += relativedelta(years=1) #hér verður 29.2 að 28.2
            uppgreiddLan = [] #listi sem mun geyma index númer allra uppgreiddra lána
            umframpeningur = 0 #umframpeningurinn af mánaðrinngreiðslu, verður greiddur inn á þann Lan hlut með hæstu vextina
            for index, skuld in enumerate(self.uetlaen):
                skuld.upphaed += skuld.maenadharlegInnborgun
                if skuld.gjalddagi - self.Dagsetning <= timedelta(0) :    
                    skuld.upphaed *=  (1.0 + (skuld.vextir/100.0))
                    skuld.upphaed = math.floor(skuld.upphaed) #better safe than sorry   
                    skuld.gjalddagi += relativedelta(years=1)
                    if (skuld.upphaed >= 0 ):
                        uppgreiddLan.append(index)
                        self.Greidhslugeta += skuld.maenadharlegInnborgun
                        umframpeningur += skuld.upphaed
            for i in uppgreiddLan:
                self.eydhaUetlaeni(int(i))
            if (len(self.innlaen) + len(self.uetlaen) > 0):
                best = self.HajstuVextir()
                best.upphaed += umframpeningur

    #eftir: Skilar true ef heildarsumma innborganna stemmir við greiðslugetu
    def gengurUpp(self):
        summa = 0
        for sparnadhur in self.innlaen:
            summa += sparnadhur.maenadharlegInnborgun
        for skuld in self.uetlaen:
            summa += skuld.maenadharlegInnborgun
        return self.Greidhslugeta <= summa

    #Eftir: breytir mánaðardegi sem innborgun verður á og borgar einu sinni inná
    def breytaInnborgunardegi(self, dagur):
        while self.Dagsetning.day != dagur:
            self.Dagsetning += timedelta(days=1)    
            for sparnadhur in self.innlaen:
                sparnadhur.upphaed += sparnadhur.maenadharlegInnborgun
                if sparnadhur.gjalddagi - self.Dagsetning <= timedelta(0) :
                    sparnadhur.upphaed *=  (1.0 + (sparnadhur.vextir/100.0))
                    sparnadhur.upphaed = math.floor(sparnadhur.upphaed) #better safe than sorry
                    sparnadhur.gjalddagi += relativedelta(years=1) #hér verður 29.2 að 28.2
            uppgreiddLan = []
            umframpeningur = 0
            for i, skuld in enumerate(self.uetlaen):
                skuld.upphaed += skuld.maenadharlegInnborgun
                if skuld.gjalddagi - self.Dagsetning <= timedelta(0) :    
                    skuld.upphaed *=  (1.0 + (skuld.vextir/100.0))
                    skuld.upphaed = math.floor(skuld.upphaed) #better safe than sorry   
                    skuld.gjalddagi += relativedelta(years=1)
                    if (skuld.upphaed >= 0 ):
                        uppgreiddLan.append(i)
                        self.Greidhslugeta += skuld.maenadharlegInnborgun
                        umframpeningur += skuld.upphaed
            for i in uppgreiddLan:
                self.eydhaUetlaeni(int(i))
            if (len(self.innlaen) + len(self.uetlaen) > 0):
                best = self.HajstuVextir()
                best.upphaed += umframpeningur

                
    # Fyrir: upphajdh er jákvæð heiltala, trygging er annaðhvort True eða False
    # vextir er milli 0.0 og 1.0
    # maenadharlegInnborgun er jákvæð heiltala, dagur og maenudhur er dagsetning sem er til
    # dagur og maenudhur er gjalddagi
    def bajtaVidhUetlaeni(self, upphajdh, vextir, trygging, maenadharlegInnborgun, dagur, maenudhur):
        uetlan = Lan((-1*upphajdh),vextir,trygging,maenadharlegInnborgun,dagur,maenudhur)
        self.uetlaen.append(uetlan)  
    
    def eydhaUetlaeni(self, indexUetlaens):
        self.uetlaen.pop(int(indexUetlaens))
        
    # Fyrir: upphajdh er jákvæð heiltala, trygging er annaðhvort True eða False
    # vextir er milli 0.0 og 1.0
    # maenadharlegInnborgun er jákvæð heiltala, dagur og maenudhur er dagsetning sem er til
    # dagur og maenudhur er gjalddagi  
    def bajtaVidhInnlaeni(self, upphajdh, vextir, trygging, maenadharlegInnborgun, dagur, maenudhur):
        innlaen = Lan(upphajdh,vextir,trygging,maenadharlegInnborgun,dagur,maenudhur)
        self.innlaen.append(innlaen)  
        
    def eydhaInnlaeni(self, indexInnlaens):
        self.innlaen.pop(int(indexInnlaens))
        
    def breytaGreidhslugetu(self, nyeGeta):
        self.Greidhslugeta = nyeGeta

    # Eftir: Skilar mismun á heildarsummum skulda og sparnaða   
    def eignastadha(self):
        a = 0
        for b in self.innlaen:
            a += b.upphaed
        for c in self.uetlaen:
            a += c.upphaed
        return a

    def plottaFramtiedharStoedhu(self, maenudhir):
        plottKloun = copy.deepcopy(self)
        tiemi = []
        stadha = []
        while maenudhir > 0 :
            tiemi.append(plottKloun.Dagsetning)
            stadha.append(plottKloun.eignastadha())
            plottKloun.stoedhuUppfajrsla(1);
            maenudhir -= 1
        return zip(tiemi, stadha)
    
    #Prentar template fyrir bajtavidh föllin. Til hæginda við prófanir
    def Template(self):
        print "bajtaVidhUetlaeni bajtaVidhInnlaeni"
        print "upphæð, vextir, trygging, mán. innborgun, dagur, mánuður"

    #Prentar út stöðuna
    def prenta(self):
        print "Greidhslugeta: " + str(self.Greidhslugeta) + " kr."
        print "Dagsetning: " + str(self.Dagsetning) 
        print "\n\nSkuldir:\n"
        i = 0
        for skuld in self.uetlaen:
            print "skuld nr." + str(i)
            skuld.prenta()
            print ""
            i +=1
        i = 0
        print "\nSparnaður:\n"
        for sparnadhur in self.innlaen:
            print "Sparnadhur nr. %d" %i
            sparnadhur.prenta()
            print""
            i += 1
        print ""
        print "Eignastadha: ", self.eignastadha()

def einingaProuf():
    N = Notandi(8000)
    N.prenta()
    print ""
    print "\nNæst verður bætt við lánum og sparnöðum."
    a = raw_input("Ýt á eitthvað til að halda áfram\n")
    print ""
    N.bajtaVidhUetlaeni(100000, 5.19, True, 2000, 1,1)
    N.bajtaVidhUetlaeni(200000, 33.15, False, 500, 28,9)
    N.bajtaVidhInnlaeni(5000, 12.5, False, 5500, 11,11)
    N.bajtaVidhInnlaeni(2540000, 3.2, True, 0, 1,1)
    N.prenta()
    print ""
    print "\nNú líða 5 mánuðir."
    a = raw_input("Ýt á eitthvað til að halda áfram\n")
    print ""
    N.stoedhuUppfajrsla(5)
    N.prenta()
    print ""
    print "\nNú líða 7 mánuðir."
    a = raw_input("Ýt á eitthvað til að halda áfram\n")
    print ""
    N.stoedhuUppfajrsla(7)
    N.prenta()
    print ""
    print "\nNú líða 6 ár."
    a = raw_input("Ýt á eitthvað til að halda áfram\n")
    print ""
    N.stoedhuUppfajrsla(6*12)
    N.prenta()
    print ""
    print "\nBætist 2000 við greiðslugetu. Og það sett á \"besta\" reikninginn (með hæstu vextina)."
    a = raw_input("Ýt á eitthvað til að halda áfram\n")
    print ""
    N.Greidhslugeta += 2000
    a = N.HajstuVextir()
    a.maenadharlegInnborgun += 2000
    N.prenta()
    print ""
    print "\nPrenta út framtíðarspá um 2 ár."
    a = raw_input("Ýt á eitthvað til að halda áfram\n")
    print ""
    print N.plottaFramtiedharStoedhu(2*12)
    
