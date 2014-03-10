# -*- coding: utf-8 -*-
import locale
os_encoding = locale.getpreferredencoding()
import random

#Spil
class Spil:
	def __init__(self, sort, gildi, path):
		self.sort=sort
		self.gildi=gildi
		self.path=path #Slóð fyrir myndina sem er notuð í GUI
		
	def __str__(self):
		return ("{0}{1}".format(self.sort,self.gildi))
		
	def __eq__(self, other):
		return self.sort == other.sort and self.gildi == other.gildi

#Spilastokkur
class Spilastokkur:
	def __init__(self):
		self.listi=[]
		p="Myndir/"
		for i in ["H","S","T","L"]:
			for j in range(1,14):
				self.listi.append(Spil(i,j,p+i+str(j)))
		self.Stokka()
	
	def __getitem__(self,num):
		return self.listi[num]
	
	def __len__(self):
		return len(self.listi)
		
	#Stokkar spilastokkinn
	def Stokka(self):	
		for i in range(52):
			self.Vixla(i,random.randint(0,51))
	
	#Fall sem víxlar tveimur spilum í stokknum
	def Vixla(self,numer1,numer2):
		breyta=[self.listi[numer1].sort,self.listi[numer1].gildi]
		self.listi[numer1].sort=self.listi[numer2].sort
		self.listi[numer1].gildi=self.listi[numer2].gildi
		self.listi[numer2].sort=breyta[0]
		self.listi[numer2].gildi=breyta[1]
	
	#Tek spil úr stokknum
	def Taka(self):
		x=self.listi[0]
		del self.listi[0]
		return x

#Hendi
class Hendi:
	def __init__(self):
		self.listi=[]
		self.teljari=52

	def __getitem__(self,num):
		return self.listi[num]
		
	def __len__(self):
		return len(self.listi)
		
	#Tek spil á hendi
	def Halda(self,spil):
		self.listi.append(spil)
	
	#Losa mig við spil
	def Henda(self,num):
		del self.listi[num]
		
	#Sýni spilin sem ég hef á hendi
	def Syna(self,S,H):
		if len(self.listi)>4:
			x=4
		else:
			x=len(self.listi)
		strengur=""
		for i in range(len(self.listi)-1,len(self.listi)-1-x,-1):
			strengur=str(self[i])+" "+strengur
		print ""
		print ""
		print strengur
		print ""
		print "Hendi: "+str(len(H))+" Stokkur: "+str(len(S))