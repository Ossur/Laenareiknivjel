# -*- coding: utf-8 -*-
import unittest
import Spilastokkur as Stokkur
import pondukapall as Kapall

class Prufur(unittest.TestCase):
	def test_Spil_Eiginleikar(self):
		spil=Stokkur.Spil("H",1,"")
		self.assertEqual(spil.sort,"H")
		self.assertEqual(spil.gildi,1)
	
	def test_Spilastokkur_Lengd(self):
		S=Stokkur.Spilastokkur()
		self.assertEqual(len(S),52)
		spil=Stokkur.Spil("H",1,"")
	
	def test_Spilastokkur_Stokka1(self):
		#Athuga hvort að öll spilin séu enn í spilastokknum eftir stokkun
		S=Stokkur.Spilastokkur()
		A=[]
		for i in ["H","S","T","L"]:
			for j in range(1,14):
				A.append(Stokkur.Spil(i,j,""))
		
		for i in range(len(S)):
			flag=False
			for j in range(len(A)):
				flag=flag or S[i]==A[j]#(S[i].sort==A[j].sort and S[i].gildi==A[j].gildi)
			self.assertTrue(flag)
		
	
	def test_Spilastokkur_Stokka2(self):
		#Athuga hvort að spilastokkurinn hafi verið stokkaður
		S=Stokkur.Spilastokkur()
		A=[]
		for i in ["H","S","T","L"]:
			for j in range(1,14):
				A.append(Stokkur.Spil(i,j,""))
		for i in range(len(S)):
			flag=True
			flag=flag and (S[i].sort==A[i].sort and S[i].gildi==A[i].gildi)
		self.assertFalse(flag)
	
	def test_Spilastokkur_Taka(self):
		S=Stokkur.Spilastokkur()
		x=[S[0].sort,S[0].gildi]
		y=S.Taka()
		self.assertEqual(x[0],y.sort)
		self.assertEqual(x[1],y.gildi)
	
	def test_Hendi_Halda(self):
		S=Stokkur.Spilastokkur()
		H=Stokkur.Hendi()
		x=[S[0].sort,S[0].gildi]
		H.Halda(S.Taka())
		self.assertEqual(x[0],H[0].sort)
		self.assertEqual(x[1],H[0].gildi)
	
	def test_Hendi_Henda(self):
		S=Stokkur.Spilastokkur()
		H=Stokkur.Hendi()
		x=[S[0].sort,S[0].gildi]
		H.Halda(S.Taka())
		H.Halda(S.Taka())
		fyrir=len(H)
		H.Henda(len(H)-1)
		eftir=len(H)
		self.assertEqual(fyrir-eftir,1)
	
	def test_Kapall_Draga(self):
		S=Stokkur.Spilastokkur()
		H=Stokkur.Hendi()
		S_fyrir=len(S)
		H_fyrir=len(H)
		Kapall.Draga(S,H)
		S_eftir=len(S)
		H_eftir=len(H)
		self.assertEqual(S_fyrir-S_eftir,1)
		self.assertEqual(H_fyrir-H_eftir,-1)
		#Athuga hvort að spilið sem ég var að draga sé enn í stokknum
		for i in range(len(S)):
			flag=True
			flag=flag and (S[i].sort==H[0].sort and S[i].gildi==H[0].gildi)
		self.assertFalse(flag)
	
	def test_Kapall_Kasta(self):
		listi=[]
		for i in ["H","S","T","L"]:
			for j in range(1,14):
				listi.append(Stokkur.Spil(i,j,""))
		
		#Prófa að kasta 2 spilum
		H=Stokkur.Hendi()
		for i in range(4):
			H.Halda(listi[i])
		H_fyrir=len(H)
		Kapall.Kasta(listi,H,2)
		H_eftir=len(H)
		self.assertEqual(H_fyrir-H_eftir,2)
		self.assertEqual(H[0].sort,"H")
		self.assertEqual(H[0].gildi,1)
		self.assertEqual(H[1].sort,"H")
		self.assertEqual(H[1].gildi,4)
		
		#Prófa að kasta 4 spilum
		H.Halda(listi[4])
		H.Halda(listi[13])
		H_fyrir=len(H)
		Kapall.Kasta(listi,H,4)
		H_eftir=len(H)
		self.assertEqual(H_fyrir-H_eftir,4)
		self.assertEqual(len(H),0)
	
	def test_Kapall_Skipta(self):
		S=Stokkur.Spilastokkur()
		H=Stokkur.Hendi()
		for i in range(6):
			H.Halda(S[i])
		#"Tæmi" stokkinn, því skipta á bara að virka þegar stokkurinn er tómur
		S=[]
		x=[H[0].sort,H[0].gildi]
		y=[H[2].sort,H[2].gildi]
		Kapall.Skipta(S,H)
		self.assertEqual(H[len(H)-1].sort,x[0])
		self.assertEqual(H[len(H)-1].gildi,x[1])
		self.assertEqual(H[1].sort,y[0])
		self.assertEqual(H[1].gildi,y[1])
			
if __name__ == '__main__':
	unittest.main(verbosity=2, exit=False)