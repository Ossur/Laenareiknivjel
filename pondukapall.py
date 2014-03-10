# -*- coding: utf-8 -*-
#import locale
#os_encoding = locale.getpreferredencoding()
#Pöndukapall
from Spilastokkur import *

#Dreg spil úr stokknum og set það í hendina
def Draga(S,H):
	if len(S)==0:
		if H.teljari>0:
			#Stokkurinn er tómur, svo það er kallað á Skipta í staðinn
			Skipta(S,H)
			#Ath, Skipta kallar á H.Syna(S,H)
		else:
			print "Kapallinn gengur ekki upp!"
	else:
		H.Halda(S.Taka())
		H.Syna(S,H)

#Tek 2 eða 4 spil af hendinni
def Kasta(S,H,num):
	#villutékk, má kasta 2 eða 4?
	#eru 4 spil eftir?
	if len(H)<4:
		if len(S)==0:
			if len(H)==0 or len(H)==2:
				print "Þú vannst!"
			else:
				if H[len(H)-1].sort!=H[len(H)-4].sort and H[len(H)-1].gildi!=H[len(H)-4].gildi and H.teljari<1:
					print "Kapallinn gengur ekki upp!"
		else:
			print "Drag"+chr(208)+"u spil"
	else:
		if num==2:
			if H[len(H)-1].sort==H[len(H)-4].sort:
				H.Henda(len(H)-2)
				H.Henda(len(H)-2)
				H.teljari=len(H)
				H.Syna(S,H)
			else:
				print "Ógildur leikur"
				H.Syna(S,H)
		elif num==4:
			if H[len(H)-1].gildi==H[len(H)-4].gildi:
				H.Henda(len(H)-1)
				H.Henda(len(H)-1)
				H.Henda(len(H)-1)
				H.Henda(len(H)-1)
				if len(S)>0:
					H.teljari=len(H)+len(S)
				else:
					H.teljari=len(H)
				H.Syna(S,H)
			else:
				print "Ógildur leikur"
				H.Syna(S,H)
		else:
			print "error"
			H.Syna(S,H)
		#búinn að vinna/tapa?
		if len(S)==0:
			if len(H)==0 or len(H)==2:
				print "Þú vannst!"
				H.teljari=0
			else:
				if H[len(H)-1].sort==H[len(H)-4].sort or H[len(H)-1].gildi==H[len(H)-4].gildi:
					return
				else:
					if H.teljari<1:
						print "Kapallinn gengur ekki upp!"

#Færi til spilin í lok leiksins
#Fallið Draga(S,H) kallar á þetta þegar að stokkurinn er tómur
def Skipta(S,H):
	if H.teljari>0:
		if len(S)==0: #and len(H)==4:
			x=[H[0].sort,H[0].gildi]
			for i in range(1,len(H)):
				H[i-1].sort=H[i].sort
				H[i-1].gildi=H[i].gildi
			H[len(H)-1].sort=x[0]
			H[len(H)-1].gildi=x[1]
			H.Syna(S,H)
			H.teljari=H.teljari-1
		else:
			print "Ógildur leikur"
			H.Syna(S,H)
	else:
		print "Kapallinn gengur ekki upp!"
			
if __name__ == "__main__":
	#Stilli upp fyrsta leiknum
	print "Pöndukapall"
	print "Gildar skipanir: Draga (d), Henda 2 (2), Henda 4 (4), Hint (h), Autoplay (a), Full-Autoplay (f), Byrja aftur (b), Hætta (q)."
	print ""
	S=Spilastokkur()
	H=Hendi()
	for i in range(4):
		H.Halda(S.Taka())
	H.Syna(S,H)

	#Leikjalykkja
	while True:
		x=raw_input()
		if x.lower()=="draga" or x.lower()=="d":
			Draga(S,H)
		elif x.lower()=="henda 2" or x=="2":
			Kasta(S,H,2)
		elif x.lower()=="henda 4" or x=="4":
			Kasta(S,H,4)
		elif x.lower()=="hint" or x=="h":
			if len(H)>=4 and H[len(H)-1].gildi==H[len(H)-4].gildi:
				print "Hentu 4"
			elif len(H)>=4 and H[len(H)-1].sort==H[len(H)-4].sort:
				print "Hentu 2"
			else:
				if H.teljari>0:
					print "Drag"+chr(208)+"u spil"
				else:
					print "Kapallinn gengur ekki upp!"
		elif x.lower()=="autoplay" or x.lower()=="a":
			if len(H)>=4 and H[len(H)-1].gildi==H[len(H)-4].gildi:
				Kasta(S,H,4)
			elif len(H)>=4 and H[len(H)-1].sort==H[len(H)-4].sort:
				Kasta(S,H,2)
			else:
				if H.teljari>=0:
					Draga(S,H)
				else:
					print "Kapallinn gengur ekki upp!"
		elif x.lower()=="full-autoplay" or x.lower()=="f" or x.lower()=="full":
			y=raw_input("Ertu viss? (Y/N) ")
			if y.lower()=="y":
				z=raw_input("Veldu hraða (0-11)")
				while H.teljari>0:
					if z=="11":
						pass
					else:
						w=21-int(z)
						j=0
						for i in range(0,pow(2,w)):
							j=j+1 #just passing the time :)
					if len(H)>=4 and H[len(H)-1].gildi==H[len(H)-4].gildi:
						Kasta(S,H,4)
					elif len(H)>=4 and H[len(H)-1].sort==H[len(H)-4].sort:
						Kasta(S,H,2)
					else:
						if H.teljari>0:
							Draga(S,H)
						else:
							print "Kapallinn gengur ekki upp!"
			else:
				H.Syna(S,H)
		elif x.lower()=="byrja aftur" or x.lower()=="byrja" or x.lower()=="b" or x.lower()=="aftur":
			del S
			del H
			print "Nýr leikur"
			S=Spilastokkur()
			H=Hendi()
			for i in range(4):
				H.Halda(S.Taka())
			H.Syna(S,H)
		elif x.lower()=="hætta" or x.lower()=="q":
			break
		else:
			print "Gildar skipanir: Draga (d), Henda 2 (2), Henda 4 (4), Hint (h), Autoplay (a), Full-Autoplay (f), Byrja aftur (b), Hætta (q)."
