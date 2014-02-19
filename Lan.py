# This Python file uses the following encoding: utf-8

from datetime import date  
import math
from dateutil.relativedelta import relativedelta

#Þetta er inn/útlána klasi. Hugmyndin er að ef þetta er útlán (skuld) þá sé upphaed 
#neikvæð tala. Það er tekið með í reikninginn í öllum prentföllum.

class Lan:
    def __init__(self,upphaed,vextir,trygging, maenadharlegInnborgun, dagur, maenudhur):
        self.upphaed=upphaed
        self.vextir=vextir #gert er ráð fyrir að þetta séu ÁRSvextir
        self.trygging=trygging
        self.maenadharlegInnborgun = maenadharlegInnborgun
        self.gjalddagi = date.today() #gjalddagi er dagurinn þar sem vextir eru teknir af láni
        while self.gjalddagi.day != dagur:
            self.gjalddagi += relativedelta(days=1)
        while self.gjalddagi.month != maenudhur :
            self.gjalddagi += relativedelta(months=1)
        while self.gjalddagi.day != dagur: #stundum lækkar day við += relativedelta(months=1)
            self.gjalddagi += relativedelta(days=1)            
        #gjalddagi er næsti dagur með mánaðardagsetninguna dagur.maenudhur


        
    def breytaGjalddaga(self, dagur, maenudhur):
        self.gjalddagi = date.today()
        while self.gjalddagi.day != dagur:
            self.gjalddagi += relativedelta(days=1)
        while self.gjalddagi.month != maenudhur :
            self.gjalddagi += relativedelta(months=1)
        while self.gjalddagi.day != dagur: 
            self.gjalddagi += relativedelta(days=1)
    
    def breytaupphaed(self):
        self.upphaed=raw_input("Sladu inn nyja upphaed a laninu: ")
    
    def breytavoxtum(self):
        self.vextir=raw_input("Sladu inn nyja vexti a laninu: ")
    
    def breytatryggingu(self):
        self.trygging=raw_input("Er lanid verd(True/False): ")
        
    def breytainnborgun(self):
        self.maenadharlegInnborgun=raw_input("Sladu inn nyja upphaed sem thu vilt borga i lanid a manudi: ")
    
    # Fall sem tekur inn markmið (krónutölu) og tíma (mánaðarfjölda)
    # Virkar fyrir bæði lán og sparnað. Markmiðið þarf þó að hafa sama formerki og vera hærri tala en self.upphaed
    # Skilar minnstu upphæð sem þarf að borga mánaðarlega til að ná markmiðinu.
    # (Skilar s.s. EKKI upphæðinni sem þarf að bæta við þá mánaðarlegu innborgun sem er fyrir)
    # Miðar við að fyrsta mánaðarlega lágmarksinnborgunin berist ÁÐUR en næstu vextir eru teknir
    def markmidhsLaegmark(self, ouskaupphajdh, maenadharfjoeldi):
        # ouskaupphajdh = upphaed*(vextir**maenadharfjoeldi) + (skil*(vextir**1) + skil*(vextir**2) +... + skil*skil*(vextir**maenadharfjoeldi)
        # ==
        # skil*(vextir**1 + vextir**2 + ... + vextir**maenadharfjoeldi) = ouskaupphajdh - upphaed*(vextir**maenadharfjoeldi)
        # ==
        # skil = (ouskaupphajdh - upphaed*(vextir**maenadharfjoeldi)) / (vextir**1 + vextir**2 + ... + vextir**maenadharfjoeldi)
        if ( self.upphaed < 0 and ouskaupphajdh > 0 ) or (self.upphaed > ouskaupphajdh) :
            print "Villa: Óskaupphæð ómöguleg eða lægri en höfuðstóll."
            return 0
        vaxtasumma = 0 
        for i in range(1,maenadharfjoeldi):
            vaxtasumma += self.vextir**i
            skil = (ouskaupphajdh - self.upphaed*(self.vextir**maenadharfjoeldi)) / vaxtasumma
        return math.ceil(skil)
    
    def prenta(self):
        print "Upphaed: " + str(abs(int(self.upphaed)))
        print "Vextir: ", self.vextir
        print "Verdtrygging: ", self.trygging
        print "Gjalddagi", self.gjalddagi
        print "Mánaðarleg Innborgun: ", self.maenadharlegInnborgun
        
