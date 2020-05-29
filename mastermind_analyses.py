import random
import copy
import time
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

class Mastermind:

	def __init__(self, n):
		self.n = n
		self.p = 2 * n
		self.D = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		self.Dp = []
		for i in range(self.p):
			self.Dp.append(self.D[i])
		self.code_secret = []
		self.nb_tentatives = 0
		self.code_tentative = {}
		self.victoire = False
		self.states = dict()

	def create_code_secret_random(self):
		Dp_copy = self.Dp.copy()
		for i in range(self.n):
			temp = random.choice(Dp_copy)
			self.code_secret.append(temp)
			Dp_copy.remove(temp)

	def create_code_secret_random_v2(self):
		Dp_copy = self.Dp.copy()
		temp_doublons = []
		for i in range(self.n):
			temp = random.choice(Dp_copy)
			if temp in temp_doublons:
				Dp_copy.remove(temp)
			else:
				temp_doublons.append(temp)
			self.code_secret.append(temp)

	def create_code_secret(self,code):
		self.code_secret = code

	def create_code_tentative(self,tentative):
		self.nb_tentatives += 1
		self.code_tentative = tentative.copy()

	def comparaison(self):
		temp_bp = 0
		temp_mp = 0
		data = dict([(n, self.code_secret.count(n)) for n in set(self.code_secret)])
		liste_indices = []
		for i in range(len(self.code_tentative)):
			if self.code_tentative[i] == self.code_secret[i]:	
				temp_bp += 1
			else:
				if self.code_tentative[i] in self.code_secret:		
					if data[self.code_tentative[i]] == 2:
						liste_indices[:] = []
						for j,e in enumerate(self.code_secret):
							if e == self.code_tentative[i]:
								liste_indices.append(j)
						if (liste_indices[0] == self.code_secret.index(self.code_tentative[i]) or liste_indices[1] == self.code_secret.index(self.code_tentative[i])):
							temp_mp += 1
					else:
						if (self.code_secret.index(self.code_tentative[i]) not in self.code_tentative or self.code_secret[self.code_secret.index(self.code_tentative[i])] != self.code_tentative[self.code_secret.index(self.code_tentative[i])]):
							temp_mp += 1
		self.states[self.nb_tentatives] = (self.code_tentative,temp_bp,temp_mp)

	def comparaison_doublons(self):
		temp_bp = 0
		temp_mp = 0
		#data = dict([(n, self.code_secret.count(n)) for n in set(self.code_secret)])
		data = dict([(n,0) for n in set(self.code_secret)])
		#print("data :",data)
		#print("self.code_tentative :",self.code_tentative)
		#print("self.code_secret :",self.code_secret)
		for i in range(len(self.code_tentative)):
			#print("i :",i)
			#print("data :",data)
			if self.code_tentative[i] == self.code_secret[i]:	
				temp_bp += 1
				data[self.code_tentative[i]] += 1
				#print("temp_bp :",temp_bp)
			else:
				if self.code_tentative[i] in self.code_secret:
					if data[self.code_tentative[i]] == self.code_secret.count(self.code_tentative[i]):
						continue
					elif data[self.code_tentative[i]] < self.code_secret.count(self.code_tentative[i]):
						#temp_mp += 1
						data[self.code_tentative[i]] += 1
						#print(self.code_secret[self.code_secret.index(self.code_tentative[i])],self.code_tentative[self.code_secret.index(self.code_tentative[i])])
						if self.code_secret[self.code_secret.index(self.code_tentative[i])] != self.code_tentative[self.code_secret.index(self.code_tentative[i])]:
							temp_mp += 1
						elif self.code_secret.count(self.code_tentative[i]) == 2:
							temp_mp += 1
					#print("temp_mp :",temp_mp)
		self.states[self.nb_tentatives] = (self.code_tentative,temp_bp,temp_mp)

	def check_victoire(self):
		if self.states[self.nb_tentatives][1] == self.n:
			self.victoire = True

	def get_n(self):
		return self.n

	def get_p(self):
		return self.p

	def get_Dp(self):
		return self.Dp

	def get_code_secret(self):
		return self.code_secret

	def get_code_tentative(self):
		return self.code_tentative

	def get_victoire(self):
		return self.victoire

	def get_states(self):
		return self.states

	def get_nb_tentatives(self):
		return self.nb_tentatives

def compatibilite(n,states,essai):
	compatible = True
	mm_temp = Mastermind(n)
	#print("states :",states.items())
	for t,s in states.items():
		code_temp = []
		for i in s[0].values():
			code_temp.append(i)
		mm_temp.create_code_secret(code_temp) # liste
		mm_temp.create_code_tentative(essai) # dico
		mm_temp.comparaison()
		if mm_temp.get_states()[len(mm_temp.get_states())][1] != s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] != s[2]:
			compatible = False
			break
	return compatible

def compatibilite_doublons(n,states,essai):
	compatible = True
	mm_temp = Mastermind(n)
	#print("states :",states.items())
	for t,s in states.items():
		#print("t :",t,"s :",s)
		code_temp = []
		for i in s[0].values():
			code_temp.append(i)
		#print("code_temp :",code_temp)
		#print("essai :",essai)
		mm_temp.create_code_secret(code_temp) # liste
		mm_temp.create_code_tentative(essai) # dico
		mm_temp.comparaison_doublons()
		#print(mm_temp.get_states()[len(mm_temp.get_states())][1],s[1])
		#print(mm_temp.get_states()[len(mm_temp.get_states())][2],s[2])
		if mm_temp.get_states()[len(mm_temp.get_states())][1] != s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] != s[2]:
			compatible = False
			break
	return compatible

def engendrer_et_tester(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	nbreVar : nombre de variables restantes à instancier
	D : domaine des variables
	n, states : contraintes
	'''
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds
	else:
		nbreVar -= 1
		for v in D:
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre		
			nbre_noeuds += 1
			if n == len(noeud):
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				if compatibilite_doublons(n,states,i_dico) and len(noeud) == len(set(noeud)): # si le code est compatible, on le prend
					return i_dico,nbre_noeuds
			res, nbre_noeuds_temp = engendrer_et_tester(i+list(v),nbreVar,D,n,states)
			nbre_noeuds += nbre_noeuds_temp
			if len(res) == n and compatibilite_doublons(n,states,res) and len(noeud) == len(set(noeud)):
				i = res
				break
	return i,nbre_noeuds

def RAC(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n et states : les contraintes
	'''
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds
	else:
		nbreVar -= 1
		for v in D:
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			nbre_noeuds += 1	
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				if n == len(noeud):
					i_dico = {}
					for j in range(len(noeud)):
						i_dico[j] = noeud[j]
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico,nbre_noeuds
				res,nbre_noeuds_temp = RAC(i+list(v),nbreVar,D,n,states)
				nbre_noeuds += nbre_noeuds_temp
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i,nbre_noeuds

def RAC_forward_checking(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n et states : les contraintes
	'''
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds
	else:
		nbreVar -= 1
		for v in D:
			D_bis = D.copy()
			D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			nbre_noeuds += 1
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				if n == len(noeud):
					i_dico = {}
					for j in range(len(noeud)):
						i_dico[j] = noeud[j]
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico,nbre_noeuds
				res,nbre_noeuds_temp = RAC_forward_checking(i+list(v),nbreVar,D_bis,n,states)
				nbre_noeuds += nbre_noeuds_temp
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i,nbre_noeuds

def RAC_forward_checking_doublons(i,nbreVar,D,n,states,nbre_occurences):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n, states, nbre_occurences : les contraintes
	'''
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds
	else:
		nbreVar -= 1
		for j in range(len(D)):
			nbre_occurences_bis = nbre_occurences.copy()
			v = D[j]
			nbre_occurences_bis[j] += 1
			D_bis = D.copy()
			if nbre_occurences_bis[j] == 2:
				D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			nbre_noeuds += 1
			if n == len(noeud):
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				cd = compatibilite_doublons(n,states,i_dico)
				if cd: # si le code est compatible, on le prend
					return i_dico,nbre_noeuds
			res,nbre_noeuds_temp = RAC_forward_checking_doublons(i+list(v),nbreVar,D_bis,n,states,nbre_occurences_bis)
			nbre_noeuds += nbre_noeuds_temp
			if len(res) == n and compatibilite_doublons(n,states,res):
				i = res
				break
	return i,nbre_noeuds

def RAC_forward_checking_ameliore(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n, states : les contraintes
	'''
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds
	else:
		nbreVar -= 1
		for v in D:
			D_bis = D.copy()
			D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			nbre_noeuds += 1
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				if n == len(noeud): # code complet			
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico,nbre_noeuds
				else:
					compatible = True
					mm_temp = Mastermind(n)
					for t,s in states.items():
						code_temp = []
						for j in s[0].values():
							code_temp.append(j)
						mm_temp.create_code_secret(code_temp) # liste
						mm_temp.create_code_tentative(i_dico) # dico
						mm_temp.comparaison()
						if mm_temp.get_states()[len(mm_temp.get_states())][1] > s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] > s[2]:
							compatible = False
							break
					if compatible == False:
						continue
				res,nbre_noeuds_temp = RAC_forward_checking_ameliore(i+list(v),nbreVar,D_bis,n,states)
				nbre_noeuds += nbre_noeuds_temp
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i,nbre_noeuds

def LasVegas(D,n,states):
	'''
	D : domaine des variables
	n, states : contraintes
	'''
	nbre_noeuds = 0
	while True:
		res = {}
		D_temp = D.copy()
		for i in range(n):
			temp = random.choice(D_temp)
			res[i] = temp
			D_temp.remove(temp) # améliore l'algo en évitant les doublons
			nbre_noeuds += 1
			#print("noeud :",res) # permet de voir tous les noeuds de l'arbre
		if compatibilite(n,states,res):
			break
	return res,nbre_noeuds

def RAC_forward_checking_ameliore_LasVegas(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n, states : les contraintes
	'''
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds
	else:
		nbreVar -= 1
		D_LasVegas = D.copy()
		for lv in range(len(D_LasVegas)):
			v = random.choice(D_LasVegas)
			D_LasVegas.remove(v)
			D_bis = D.copy()
			D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			nbre_noeuds += 1
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				if n == len(noeud): # code complet			
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico,nbre_noeuds
				else:
					compatible = True
					mm_temp = Mastermind(n)
					for t,s in states.items():
						code_temp = []
						for j in s[0].values():
							code_temp.append(j)
						mm_temp.create_code_secret(code_temp) # liste
						mm_temp.create_code_tentative(i_dico) # dico
						mm_temp.comparaison()
						if mm_temp.get_states()[len(mm_temp.get_states())][1] > s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] > s[2]:
							compatible = False
							break
					if compatible == False:
						continue
				res,nbre_noeuds_temp = RAC_forward_checking_ameliore_LasVegas(i+list(v),nbreVar,D_bis,n,states)
				nbre_noeuds += nbre_noeuds_temp
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i,nbre_noeuds

def RAC_forward_checking_ameliore_AG(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n, states : les contraintes
	'''
	compatible = False
	nbre_noeuds = 0
	if nbreVar == 0:
		return i,nbre_noeuds,False
	else:
		nbreVar -= 1
		for v in D:
			D_bis = D.copy()
			D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			nbre_noeuds += 1
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				if n == len(noeud): # code complet			
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico,nbre_noeuds,True
					else:
						return i_dico,nbre_noeuds,False
				elif n > len(noeud):
					compatible = True
					mm_temp = Mastermind(n)
					for t,s in states.items():
						code_temp = []
						for j in s[0].values():
							code_temp.append(j)
						mm_temp.create_code_secret(code_temp) # liste
						mm_temp.create_code_tentative(i_dico) # dico
						mm_temp.comparaison()
						if mm_temp.get_states()[len(mm_temp.get_states())][1] > s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] > s[2]:
							compatible = False
							break
					if compatible == False:
						continue
					else:
						compatible = True
				else:
					break
				res,nbre_noeuds_temp,compatible = RAC_forward_checking_ameliore_AG(i+list(v),nbreVar,D_bis,n,states)
				nbre_noeuds += nbre_noeuds_temp
				if len(res) == n and compatibilite(n,states,res):
					i = res
					compatible = True
					break
	return i,nbre_noeuds,compatible

def run(n=4,joueur=0,code_secret=['0','1','2','3'],premiere_tentative={0: '0', 1: '1', 2: '2', 3: '3'},strategie_algo_genetique=0,maxsize=10,maxgen=105,popsize=50,CXPB=0.6,MUTPB=0.4):

	nbre_noeuds = 0
	if (joueur == 0):
		print("Ok.")
	else:
		mastermind = Mastermind(n)

		mastermind.create_code_secret(code_secret)

		#reponse = mastermind.get_code_secret()
		reponse = code_secret
		#print("La réponse est :",reponse)

		D = mastermind.get_Dp().copy()

		while(True):
			'''
			if(mastermind.get_nb_tentatives() > 0):
				for i in mastermind.get_states():
					print("Tentative",i,":",mastermind.get_states()[i][0],"bien placés :",mastermind.get_states()[i][1],"mal placés :",mastermind.get_states()[i][2])
			
			print("Tentative courante",mastermind.get_nb_tentatives()+1,":")
			'''
			'''
			if(mastermind.get_nb_tentatives() > 0):
				print("Tentative",len(mastermind.get_states()),":",mastermind.get_states()[len(mastermind.get_states())][0],"bien placés :",mastermind.get_states()[len(mastermind.get_states())][1],"mal placés :",mastermind.get_states()[len(mastermind.get_states())][2])	
			'''
			#################################################################################################################################################################################################
			
			if (joueur == 0):
				res = []
				print("Veuillez saisir votre code contenant",mastermind.get_n(),"caractères distincts :")
				while(True):
					temp_str = str(input())
					if len(temp_str) == n:
						break
					else:
						print("Veuillez ressaisir votre code contenant",mastermind.get_n(),"caractères distincts :")
				for i in temp_str:
					res.append(i)

			#################################################################################################################################################################################################

			elif (joueur == 1): # engendrer et tester
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res,nbre_noeuds_temp = engendrer_et_tester(i,nbreVar,D,n,states)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 2): # retour arrière chronologique sans forward checking
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res,nbre_noeuds_temp = RAC(i,nbreVar,D,n,states)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 3): # retour arrière chronologique AVEC forward checking SANS doublons
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res,nbre_noeuds_temp = RAC_forward_checking(i,nbreVar,D,n,states)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 4): # retour arrière chronologique AVEC forward checking AVEC doublons
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					nbre_occurences = [0] * mastermind.get_p()
					res,nbre_noeuds_temp = RAC_forward_checking_doublons(i,nbreVar,D,n,states,nbre_occurences)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 5): # retour arrière chronologique AVEC forward checking SANS doublon, AMELIORE
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res,nbre_noeuds_temp = RAC_forward_checking_ameliore(i,nbreVar,D,n,states)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 6): # bonus : Las Vegas naïf
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					states = mastermind.get_states()
					res,nbre_noeuds_temp = LasVegas(D,n,states)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 7): # bonus : A5 version Las Vegas
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					res = premiere_tentative
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res,nbre_noeuds_temp = RAC_forward_checking_ameliore_LasVegas(i,nbreVar,D,n,states)
					nbre_noeuds += nbre_noeuds_temp
					#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
					#input()

			#################################################################################################################################################################################################

			elif (joueur == 8): # algorithme génétique

				E = [] # ensemble de codes compatibles
				res = {}
				
				if mastermind.get_nb_tentatives() == 0:
					D_temp = D.copy()
					for i in range(n):
						temp = random.choice(D_temp)
						res[i] = temp
						D_temp.remove(temp)

				else:
					# Evaluation de l'historique en fonction du secret
					population = []
					nouvelle_population = []

					start_time = time.time()

					continuer = True
					while(continuer):
						for gen in range(maxgen):
							#print("Génération",gen,":")
							if gen > 0:
								parents = []
								population_temp = deepcopy(population)
								for i in range( int(len(population)/2) ):
									temp = min(population_temp, key = lambda t: t[1])
									parents.append(temp)
									population_temp.remove(temp)
										
							nouvelle_population[:] = []
							for p in range(popsize):
								#print("La population grandit, de taille",p+1)
								individu = {}
								if gen == 0:
									D_temp = D.copy()
									for i in range(n):
										temp = random.choice(D_temp)
										individu[i] = temp
										D_temp.remove(temp)
								else:
									parents_temp = deepcopy(parents)
									children = []
									if random.random() < 0.5:
										if random.random() < CXPB and len(parents_temp) >= 2:
											separation = random.randint(1, n-1) # point du crossover
											for i in range(2):
												temp = random.choice(parents_temp)
												temp2 = []
												for k,v in temp[0].items():
													temp2.append(v)
												if i == 0:
													child = temp2[:separation]
												else:
													child = temp2[separation:]	
												children.append(child)
												parents_temp.remove(temp)
											fusion = children[0] + children[1]
											for i in range(n):
												individu[i] = fusion[i]
										else:
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]
									else:
										if random.random() < MUTPB:
											temp_rand = random.random()
											if temp_rand < 0.33: # mutation classique
												child = random.choice(parents_temp)
												alea = random.randint(0,len(child[0]))
												child[0][alea] = random.choice(D)
												for i in range(n):
													individu[i] = child[0][i]
											elif temp_rand < 0.66: # inversion de séquence
												child = random.choice(parents_temp)
												alea0 = random.randint(0,len(child[0])-1)
												alea1 = random.randint(0,len(child[0]))
												#print("avant child :",child,"alea0 :",alea0,"alea1:",alea1)
												while(alea1-1 <= alea0):
													alea0 = random.randint(0,len(child[0])-1)
													alea1 = random.randint(0,len(child[0]))
												#print("avant child :",child,"alea0 :",alea0,"alea1:",alea1)
												temp = []
												for k,v in child[0].items():
													temp.append(v)
												temp = temp[alea0:alea1]
												temp.reverse()
												#print("temp :",temp)
												temp_indice = 0
												for i in range(alea0,alea1):
													child[0][i] = temp[temp_indice]
													temp_indice += 1
												#print("apres child :",child)
												for i in range(n):
													individu[i] = child[0][i]
												#input()
											else: # permutation
												child = random.choice(parents_temp)
												alea0 = random.randint(0,len(child[0])-1)
												alea1 = random.randint(0,len(child[0])-1)
												#print("avant child :",child,"alea0 :",alea0,"alea1:",alea1)
												while(alea1 == alea0):
													alea1 = random.randint(0,len(child[0])-1)
												temp0 = child[0][alea0]
												temp1 = child[0][alea1]
												child[0][alea0] = temp1
												child[0][alea1] = temp0
												#print("apres child :",child)
												for i in range(n):
													individu[i] = child[0][i]
										else:
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]

								# Test de l'individu par rapport aux tentatives
								mm_temp = Mastermind(n)
								fitness = 0
								for t,s in mastermind.get_states().items():
									code_temp = []
									for i in s[0].values():
										code_temp.append(i)
									mm_temp.create_code_secret(code_temp)
									mm_temp.create_code_tentative(individu)
									mm_temp.comparaison()
									#fitness += (mm_temp.get_n()*2) * mm_temp.get_states()[mm_temp.get_nb_tentatives()][1] + mm_temp.get_states()[mm_temp.get_nb_tentatives()][2]
									fitness += abs(mastermind.get_states()[t][1] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][1]) + abs(mastermind.get_states()[t][2] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][2])
									#fitness += abs(mastermind.get_states()[t][1] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][1]) + abs(mastermind.get_states()[t][2] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][2])								
								nouvelle_population.append((individu,fitness))

							# Nouvelle population :

							# remplacer entièrement
							population[:] = nouvelle_population
							'''
							# prendre les 50% meilleures
							if gen > 0:
								meilleure_population = [] # enfants
								copie_population = deepcopy(nouvelle_population)
								for i in range(int(popsize/2)):
									enfant_individu,enfant_fitness = min(copie_population, key = lambda t: t[1])
									meilleure_population.append((enfant_individu,enfant_fitness))
									copie_population.remove((enfant_individu,enfant_fitness))
								for i in range((popsize-int(popsize/2))):
									parent_individu,parent_fitness = max(population, key = lambda t: t[1])
									enfant_individu,enfant_fitness = min(meilleure_population, key = lambda t: t[1])
									if parent_fitness < enfant_fitness:
										population.remove((parent_individu,parent_fitness))
										population.append((enfant_individu,enfant_fitness))
										meilleure_population.remove((enfant_individu,enfant_fitness))
									else:
										break
							else:
								population[:] = nouvelle_population
							'''
							#print("population :",population)

							# sélectif du hall of fame compatible à mettre dans E
							population_copie = deepcopy(population)
							for i in range(len(population_copie)):
								hof_individu,hof_fitness = min(population_copie, key = lambda t: t[1])								
								if hof_fitness != 0: # ça ne sert à rien de continuer
									break
								population_copie.remove((hof_individu,hof_fitness))	
								if (hof_individu,hof_fitness) in E: # évite de remettre le même code dans E
									continue
								# vérification de la consistance locale (caractères uniques)
								uniques_values = []
								for key, d in hof_individu.items():
								    if d[0] not in uniques_values:
								        uniques_values.append(d[0])
								if len(uniques_values) == len(hof_individu): # si caractères uniques alors on append
									E.append((hof_individu,hof_fitness))
									if len(E) >= maxsize: # si on dépasse maxsize après l'append, on break
										break

							if len(E) >= maxsize:
								break

						#print("dernière population :",population)
						#print("E :",E)
						if len(E) == 0:
							temp_time = (time.time() - start_time)
							#print("E vide : Temps d'exécution : %s secondes ---" % temp_time)
							if temp_time > 300:
								continuer = False
								print("Echec de l'algorithme génétique. \n")
								'''
								res = {}
								if mastermind.get_nb_tentatives() == 0:
									res = premiere_tentative
								else: # algorithme CSP qui prend le relai en cas d'échec
									i = []
									nbreVar = n
									states = mastermind.get_states()
									res,nbre_noeuds_temp = RAC_forward_checking_ameliore(i,nbreVar,D,n,states)
									nbre_noeuds += nbre_noeuds_temp
									#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
									#input()
								'''
						else:
							#print("E :",E)
							#print("taille de E :",len(E))
							if strategie_algo_genetique == 0:													
								res,res_individu_fitness = random.choice(E) # random
							elif strategie_algo_genetique == 1:
								# Choix du code présentant le plus de similarité avec les autres codes compatibles.
								similaires = []
								for c in E:
									E_copy = deepcopy(E)
									while c in E_copy:
										E_copy.remove(c)
									temp_similarite = 0
									for c_etoile in E_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										temp_similarite += mm_temp.get_states()[len(mm_temp.get_states())][1] + mm_temp.get_states()[len(mm_temp.get_states())][2]
									similaires.append(temp_similarite)
								res,res_individu_fitness = E[similaires.index(max(similaires))] # le plus de similarités
							elif strategie_algo_genetique == 2:
								# Choix du code présentant le moins de similarité avec les autres codes compatibles.
								similaires = []
								for c in E:
									E_copy = deepcopy(E)
									while c in E_copy:
										E_copy.remove(c)
									temp_similarite = 0
									for c_etoile in E_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										temp_similarite += mm_temp.get_states()[len(mm_temp.get_states())][1] + mm_temp.get_states()[len(mm_temp.get_states())][2]
									similaires.append(temp_similarite)
								res,res_individu_fitness = E[similaires.index(min(similaires))] # le moins de similarités

							elif strategie_algo_genetique == 3:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								longueur_S = len(E)
								#longueur_S = 10
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
									E_copy.remove(temp)
									S.append(temp)
								for c in E:
									remain = 0
									S_copy = deepcopy(S)
									while c in S_copy:
										S_copy.remove(c)
									for c_etoile in S_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										S_copy_bis = deepcopy(S_copy)
										while c_etoile in S_copy_bis:
											S_copy_bis.remove(c_etoile)
										for other_code in S_copy_bis:
											mm_temp0 = Mastermind(n)
											code_temp = []
											for i in c[0].values():
												code_temp.append(i)
											mm_temp0.create_code_secret(code_temp) #liste
											mm_temp0.create_code_tentative(other_code[0]) #dico
											mm_temp0.comparaison()
											S_copy_bis = deepcopy(S_copy)
											if mm_temp.get_states()[len(mm_temp.get_states())][1] == mm_temp0.get_states()[len(mm_temp.get_states())][1] and mm_temp.get_states()[len(mm_temp.get_states())][2] == mm_temp0.get_states()[len(mm_temp.get_states())][2]:
												remain += 1
									estimations.append(remain)
								#print("estimations :",estimations)
								res,res_individu_fitness = E[estimations.index(min(estimations))]
							elif strategie_algo_genetique == 4:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								longueur_S = len(E)
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
									E_copy.remove(temp)
									S.append(temp)
								for c in E:
									remain = 0
									S_copy = deepcopy(S)
									while c in S_copy:
										S_copy.remove(c)
									for c_etoile in S_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										S_copy_bis = deepcopy(S_copy)
										while c_etoile in S_copy_bis:
											S_copy_bis.remove(c_etoile)
										for other_code in S_copy_bis:
											mm_temp0 = Mastermind(n)
											code_temp = []
											for i in c[0].values():
												code_temp.append(i)
											mm_temp0.create_code_secret(code_temp) #liste
											mm_temp0.create_code_tentative(other_code[0]) #dico
											mm_temp0.comparaison()
											S_copy_bis = deepcopy(S_copy)
											if mm_temp.get_states()[len(mm_temp.get_states())][1] == mm_temp0.get_states()[len(mm_temp.get_states())][1] and mm_temp.get_states()[len(mm_temp.get_states())][2] == mm_temp0.get_states()[len(mm_temp.get_states())][2]:
												remain += 1
									estimations.append(remain)
								#print("estimations :",estimations)
								res,res_individu_fitness = E[estimations.index(max(estimations))]
							continuer = False
				#print("res :",res)

			#################################################################################################################################################################################################

			elif (joueur == 9): # algorithme hybride

				E = [] # ensemble de codes compatibles
				res = {}
				
				if mastermind.get_nb_tentatives() == 0:
					D_temp = D.copy()
					for i in range(n):
						temp = random.choice(D_temp)
						res[i] = temp
						D_temp.remove(temp)

				else:
					# Evaluation de l'historique en fonction du secret
					population = []
					nouvelle_population = []

					start_time = time.time()

					continuer = True
					while(continuer):
						for gen in range(maxgen):
							#print("Génération",gen,":")
							if gen > 0:
								parents = []
								population_temp = deepcopy(population)
								for i in range( int(len(population)/2) ):
									temp = min(population_temp, key = lambda t: t[1])
									parents.append(temp)
									population_temp.remove(temp)
										
							nouvelle_population[:] = []
							for p in range(popsize):
								#print("La population grandit, de taille",p+1)
								individu = {}
								if gen == 0:
									D_temp = D.copy()
									for i in range(n):
										temp = random.choice(D_temp)
										individu[i] = temp
										D_temp.remove(temp)
								else:
									parents_temp = deepcopy(parents)
									children = []
									if random.random() < 0.5:
										if random.random() < CXPB and len(parents_temp) >= 2:
											separation = random.randint(1, n-1) # point du crossover
											for i in range(2):
												temp = random.choice(parents_temp)
												temp2 = []
												for k,v in temp[0].items():
													temp2.append(v)
												if i == 0:
													child = temp2[:separation]
												else:
													child = temp2[separation:]	
												children.append(child)
												parents_temp.remove(temp)
											fusion = children[0] + children[1]
											for i in range(n):
												individu[i] = fusion[i]
										else:
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]
									else:
										if random.random() < MUTPB:
											temp_rand = random.random()
											if temp_rand < 0.33: # mutation classique
												child = random.choice(parents_temp)
												alea = random.randint(0,len(child[0]))
												child[0][alea] = random.choice(D)
												for i in range(n):
													individu[i] = child[0][i]
											elif temp_rand < 0.66: # inversion de séquence
												child = random.choice(parents_temp)
												alea0 = random.randint(0,len(child[0])-1)
												alea1 = random.randint(0,len(child[0]))
												#print("avant child :",child,"alea0 :",alea0,"alea1:",alea1)
												while(alea1-1 <= alea0):
													alea0 = random.randint(0,len(child[0])-1)
													alea1 = random.randint(0,len(child[0]))
												#print("avant child :",child,"alea0 :",alea0,"alea1:",alea1)
												temp = []
												for k,v in child[0].items():
													temp.append(v)
												temp = temp[alea0:alea1]
												temp.reverse()
												#print("temp :",temp)
												temp_indice = 0
												for i in range(alea0,alea1):
													child[0][i] = temp[temp_indice]
													temp_indice += 1
												#print("apres child :",child)
												for i in range(n):
													individu[i] = child[0][i]
												#input()
											else: # permutation
												child = random.choice(parents_temp)
												alea0 = random.randint(0,len(child[0])-1)
												alea1 = random.randint(0,len(child[0])-1)
												#print("avant child :",child,"alea0 :",alea0,"alea1:",alea1)
												while(alea1 == alea0):
													alea1 = random.randint(0,len(child[0])-1)
												temp0 = child[0][alea0]
												temp1 = child[0][alea1]
												child[0][alea0] = temp1
												child[0][alea1] = temp0
												#print("apres child :",child)
												for i in range(n):
													individu[i] = child[0][i]
										else:
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]

								# Test de l'individu par rapport aux tentatives
								mm_temp = Mastermind(n)
								fitness = 0
								'''
								difference_max_avant = 0
								difference_max_apres = 0
								'''
								for t,s in mastermind.get_states().items():
									code_temp = []
									for i in s[0].values():
										code_temp.append(i)
									mm_temp.create_code_secret(code_temp)
									mm_temp.create_code_tentative(individu)
									mm_temp.comparaison()								
									fitness += abs(mastermind.get_states()[t][1] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][1]) + abs(mastermind.get_states()[t][2] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][2])
									'''
									difference_max_avant = abs(mastermind.get_states()[t][1] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][1]) + abs(mastermind.get_states()[t][2] - mm_temp.get_states()[mm_temp.get_nb_tentatives()][2])
									if difference_max_avant > difference_max_apres:
										difference_max_apres = difference_max_avant
									'''
								nouvelle_population.append((individu,fitness))

							# Nouvelle population :

							# remplacer entièrement
							population[:] = nouvelle_population
							'''
							# prendre les 50% meilleures
							if gen > 0:
								meilleure_population = [] # enfants
								copie_population = deepcopy(nouvelle_population)
								for i in range(int(popsize/2)):
									enfant_individu,enfant_fitness = min(copie_population, key = lambda t: t[1])
									meilleure_population.append((enfant_individu,enfant_fitness))
									copie_population.remove((enfant_individu,enfant_fitness))
								for i in range((popsize-int(popsize/2))):
									parent_individu,parent_fitness = max(population, key = lambda t: t[1])
									enfant_individu,enfant_fitness = min(meilleure_population, key = lambda t: t[1])
									if parent_fitness < enfant_fitness:
										population.remove((parent_individu,parent_fitness))
										population.append((enfant_individu,enfant_fitness))
										meilleure_population.remove((enfant_individu,enfant_fitness))
									else:
										break
							else:
								population[:] = nouvelle_population
							'''
							#print("population :",population)

							# sélectif du hall of fame compatible à mettre dans E
							population_copie = deepcopy(population)
							for i in range(len(population_copie)):
								hof_individu,hof_fitness = min(population_copie, key = lambda t: t[1])								
								if hof_fitness != 0: # ça ne sert à rien de continuer
									break
								population_copie.remove((hof_individu,hof_fitness))	
								if (hof_individu,hof_fitness) in E: # évite de remettre le même code dans E
									continue
								# vérification de la consistance locale (caractères uniques)
								uniques_values = []
								for key, d in hof_individu.items():
									if d[0] not in uniques_values:
										uniques_values.append(d[0])
								if len(uniques_values) == len(hof_individu): # si caractères uniques alors on append
									E.append((hof_individu,hof_fitness))
									if len(E) >= maxsize: # si on dépasse maxsize après l'append, on break
										break

							if len(E) >= maxsize:
								break

							# CSP mi génétique
							if len(E) < maxsize: # seuil facultatif, à mettre inférieur à maxsize pour l'annuler
								for pc in range(int(len(population_copie)/10)):
									#print(pc)
									individu_dico,fitness = min(population_copie, key = lambda t: t[1])
									population_copie.remove((individu_dico,fitness))
									#print(individu_dico,fitness)
									individu_liste = []
									for key, d in individu_dico.items():
										individu_liste.append(d[0])
									#print("code_secret :",code_secret)
									#print("states :",mastermind.get_states())
									#print("avant individu_liste :",individu_liste)
									#print("difference_max_apres :",difference_max_apres)
									#for fit in range(1,fitness+1):
									for fit in range(1,int(n/2)):
									#for fit in range(1,difference_max_apres+1):
										#print("fit :",fit)
										del individu_liste[-1]
									#print("apres individu_liste :",individu_liste)
									while len(set(individu_liste)) != len(individu_liste):
										fit += 1
										del individu_liste[-1]
									i = individu_liste
									nbreVar = len(individu_liste) - fit
									D_CSP = D.copy()
									for dcsp in individu_liste:
										D_CSP.remove(dcsp)
									individu,nbre_noeuds_temp,compatible = RAC_forward_checking_ameliore_AG(i,nbreVar,D_CSP,n,mastermind.get_states())
									nbre_noeuds += nbre_noeuds_temp
									if compatible == True and (individu,0) not in E:
										#print("j'ajoute dans E le code",individu)
										#input()
										E.append((individu,0))
										#print(E)
										if len(E) >= maxsize:
											break

							if len(E) >= maxsize:
								break

						#print("dernière population :",population)
						#print("E :",E)
						if len(E) == 0:
							temp_time = (time.time() - start_time)
							#print("E vide : Temps d'exécution : %s secondes ---" % temp_time)
							if temp_time > 300:
								continuer = False
								print("Echec de l'algorithme génétique. \n")
								# On pourrait donner la main à l'algorithme A5 (ou A7) ici
								'''
								res = {}
								if mastermind.get_nb_tentatives() == 0:
									res = premiere_tentative
								else:
									i = []
									nbreVar = n
									states = mastermind.get_states()
									res,nbre_noeuds_temp = RAC_forward_checking_ameliore(i,nbreVar,D,n,states)
									nbre_noeuds += nbre_noeuds_temp
									#print("Nombre de noeuds (en comptant les précédents) :",nbre_noeuds)
									#input()
								'''
						else:
							#print("E :",E)
							#print("taille de E :",len(E))
							if strategie_algo_genetique == 0:													
								res,res_individu_fitness = random.choice(E) # random
							elif strategie_algo_genetique == 1:
								# Choix du code présentant le plus de similarité avec les autres codes compatibles.
								similaires = []
								for c in E:
									E_copy = deepcopy(E)
									while c in E_copy:
										E_copy.remove(c)
									temp_similarite = 0
									for c_etoile in E_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										temp_similarite += mm_temp.get_states()[len(mm_temp.get_states())][1] + mm_temp.get_states()[len(mm_temp.get_states())][2]
									similaires.append(temp_similarite)
								res,res_individu_fitness = E[similaires.index(max(similaires))] # le plus de similarités
							elif strategie_algo_genetique == 2:
								# Choix du code présentant le moins de similarité avec les autres codes compatibles.
								similaires = []
								for c in E:
									E_copy = deepcopy(E)
									while c in E_copy:
										E_copy.remove(c)
									temp_similarite = 0
									for c_etoile in E_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										temp_similarite += mm_temp.get_states()[len(mm_temp.get_states())][1] + mm_temp.get_states()[len(mm_temp.get_states())][2]
									similaires.append(temp_similarite)
								res,res_individu_fitness = E[similaires.index(min(similaires))] # le moins de similarités

							elif strategie_algo_genetique == 3:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								longueur_S = len(E)
								#longueur_S = 10
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
									E_copy.remove(temp)
									S.append(temp)
								for c in E:
									remain = 0
									S_copy = deepcopy(S)
									while c in S_copy:
										S_copy.remove(c)
									for c_etoile in S_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										S_copy_bis = deepcopy(S_copy)
										while c_etoile in S_copy_bis:
											S_copy_bis.remove(c_etoile)
										for other_code in S_copy_bis:
											mm_temp0 = Mastermind(n)
											code_temp = []
											for i in c[0].values():
												code_temp.append(i)
											mm_temp0.create_code_secret(code_temp) #liste
											mm_temp0.create_code_tentative(other_code[0]) #dico
											mm_temp0.comparaison()
											S_copy_bis = deepcopy(S_copy)
											if mm_temp.get_states()[len(mm_temp.get_states())][1] == mm_temp0.get_states()[len(mm_temp.get_states())][1] and mm_temp.get_states()[len(mm_temp.get_states())][2] == mm_temp0.get_states()[len(mm_temp.get_states())][2]:
												remain += 1
									estimations.append(remain)
								#print("estimations :",estimations)
								res,res_individu_fitness = E[estimations.index(min(estimations))]
							elif strategie_algo_genetique == 4:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								longueur_S = len(E)
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
									E_copy.remove(temp)
									S.append(temp)
								for c in E:
									remain = 0
									S_copy = deepcopy(S)
									while c in S_copy:
										S_copy.remove(c)
									for c_etoile in S_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										S_copy_bis = deepcopy(S_copy)
										while c_etoile in S_copy_bis:
											S_copy_bis.remove(c_etoile)
										for other_code in S_copy_bis:
											mm_temp0 = Mastermind(n)
											code_temp = []
											for i in c[0].values():
												code_temp.append(i)
											mm_temp0.create_code_secret(code_temp) #liste
											mm_temp0.create_code_tentative(other_code[0]) #dico
											mm_temp0.comparaison()
											S_copy_bis = deepcopy(S_copy)
											if mm_temp.get_states()[len(mm_temp.get_states())][1] == mm_temp0.get_states()[len(mm_temp.get_states())][1] and mm_temp.get_states()[len(mm_temp.get_states())][2] == mm_temp0.get_states()[len(mm_temp.get_states())][2]:
												remain += 1
									estimations.append(remain)
								#print("estimations :",estimations)
								res,res_individu_fitness = E[estimations.index(max(estimations))]
							continuer = False
				#print("res :",res)
			
			#################################################################################################################################################################################################
			if len(res) == 0:
				#print("seuil :",seuil)
				#print("dernière population :",population)
				if(mastermind.get_nb_tentatives() > 0):
					print("\nRésumé de toutes les tentatives :")
					for i in mastermind.get_states():
						print("Tentative",i,":",mastermind.get_states()[i][0],"bien placés :",mastermind.get_states()[i][1],"mal placés :",mastermind.get_states()[i][2])
				print("\nTemps limite atteint : aucun code compatible de trouvé. \n")
				print("Arrêt sans victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				print("La bonne réponse était :",reponse,"\n")
				#input()
				break

			mastermind.create_code_tentative(res) # on incrémente ici le nombre de tentatives
			
			#print("Code saisi par le joueur :",mastermind.get_code_tentative())
			if joueur == 4 or joueur == 1:
				mastermind.comparaison_doublons()
			else:
				mastermind.comparaison()

			mastermind.check_victoire()

			if mastermind.get_victoire():
				'''
				if(mastermind.get_nb_tentatives() > 0):
					print("##############################################################################")
					print("Résumé de toutes les tentatives :")
					for i in mastermind.get_states():
						print("Tentative",i,":",mastermind.get_states()[i][0],"bien placés :",mastermind.get_states()[i][1],"mal placés :",mastermind.get_states()[i][2])
					print("##############################################################################")
					#input()
				
				print("################################## VICTOIRE ##################################")
				print("La réponse était bien :",reponse)
				print("Victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				'''
				break
			'''
			if mastermind.get_nb_tentatives() == 10: # ATTENTION : à limiter à 10 pour tracer les courbes, sinon temps beaucoup trop long
				#print("Arrêt sans victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				break
			'''
			
	if joueur != 0:
		return mastermind.get_nb_tentatives(),nbre_noeuds

#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

def graphe1_1(tailles_n,nbre_instances):
	x = []
	yA1_temps = []
	yA2_temps = []
	yA3_temps = []
	yA1_nb_tentatives = []
	yA2_nb_tentatives = []
	yA3_nb_tentatives = []
	yA1_nb_noeuds = []
	yA2_nb_noeuds = []
	yA3_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A1 = 0
		temps_A2 = 0
		temps_A3 = 0
		nb_tentatives_A1 = 0
		nb_tentatives_A2 = 0
		nb_tentatives_A3 = 0
		nb_noeuds_A1 = 0
		nb_noeuds_A2 = 0
		nb_noeuds_A3 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA1,nb_noeudsA1 = run(n,1,code_secret,premiere_tentative)
			temps_A1 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA2,nb_noeudsA2 = run(n,2,code_secret,premiere_tentative) 
			temps_A2 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time
			nb_tentatives_A1 += nb_tentativesA1
			nb_tentatives_A2 += nb_tentativesA2
			nb_tentatives_A3 += nb_tentativesA3
			nb_noeuds_A1 += nb_noeudsA1
			nb_noeuds_A2 += nb_noeudsA2
			nb_noeuds_A3 += nb_noeudsA3
		yA1_temps.append(temps_A1/nbre_instances)
		yA2_temps.append(temps_A2/nbre_instances)
		yA3_temps.append(temps_A3/nbre_instances)
		yA1_nb_tentatives.append(nb_tentatives_A1/nbre_instances)
		yA2_nb_tentatives.append(nb_tentatives_A2/nbre_instances)
		yA3_nb_tentatives.append(nb_tentatives_A3/nbre_instances)
		yA1_nb_noeuds.append(nb_noeuds_A1/nbre_instances)
		yA2_nb_noeuds.append(nb_noeuds_A2/nbre_instances)
		yA3_nb_noeuds.append(nb_noeuds_A3/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA1_temps, c="green", label="A1")
	plt.plot(x, yA2_temps, c="blue", label="A2")
	plt.plot(x, yA3_temps, c="red", label="A3")
	plt.legend()
	plt.grid()
	plt.savefig("1_1_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA1_nb_tentatives, c="green", label="A1")
	plt.plot(x, yA2_nb_tentatives, c="blue", label="A2")
	plt.plot(x, yA3_nb_tentatives, c="red", label="A3")
	plt.legend()
	plt.grid()
	plt.savefig("1_1_nb_tentatives.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA1_nb_noeuds, c="green", label="A1")
	plt.plot(x, yA2_nb_noeuds, c="blue", label="A2")
	plt.plot(x, yA3_nb_noeuds, c="red", label="A3")
	plt.legend()
	plt.grid()
	plt.savefig("1_1_nb_noeuds.png")
	plt.show()

#################################################################################################################################################################################################

def graphe1_2(tailles_n,nbre_instances):
	x = []
	yA3_temps = []
	yA4_temps = []
	yA3_nb_tentatives = []
	yA4_nb_tentatives = []
	yA3_nb_noeuds = []
	yA4_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A3 = 0
		temps_A4 = 0
		nb_tentatives_A3 = 0
		nb_tentatives_A4 = 0
		nb_noeuds_A3 = 0
		nb_noeuds_A4 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()

			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA4,nb_noeudsA4 = run(n,4,code_secret,premiere_tentative)
			temps_A4 += time.time() - start_time
			nb_tentatives_A3 += nb_tentativesA3
			nb_tentatives_A4 += nb_tentativesA4
			nb_noeuds_A3 += nb_noeudsA3
			nb_noeuds_A4 += nb_noeudsA4
		yA3_temps.append(temps_A3/nbre_instances)
		yA4_temps.append(temps_A4/nbre_instances)
		yA3_nb_tentatives.append(nb_tentatives_A3/nbre_instances)
		yA4_nb_tentatives.append(nb_tentatives_A4/nbre_instances)
		yA3_nb_noeuds.append(nb_noeuds_A3/nbre_instances)
		yA4_nb_noeuds.append(nb_noeuds_A4/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")

	plt.scatter(x, yA3_temps, c="green", label="A3")
	plt.scatter(x, yA4_temps, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.savefig("1_2_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.scatter(x, yA3_nb_tentatives, c="green", label="A3")
	plt.scatter(x, yA4_nb_tentatives, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.savefig("1_2_nb_tentatives.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.scatter(x, yA3_nb_noeuds, c="green", label="A3")
	plt.scatter(x, yA4_nb_noeuds, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.savefig("1_2_nb_noeuds.png")
	plt.show()

def graphe1_2_bis(tailles_n,nbre_instances):
	x = []
	yA3_temps = []
	yA4_temps = []
	yA3_nb_tentatives = []
	yA4_nb_tentatives = []
	yA3_nb_noeuds = []
	yA4_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A3 = 0
		temps_A4 = 0
		nb_tentatives_A3 = 0
		nb_tentatives_A4 = 0
		nb_noeuds_A3 = 0
		nb_noeuds_A4 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()

			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time

			mm_temp2 = Mastermind(n)
			mm_temp2.create_code_secret_random()
			code_secret = mm_temp2.get_code_secret()

			mm_temp3 = Mastermind(n)
			mm_temp3.create_code_secret_random()
			premiere_tentative_liste = mm_temp3.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]

			start_time = time.time()
			nb_tentativesA4,nb_noeudsA4 = run(n,4,code_secret,premiere_tentative)
			temps_A4 += time.time() - start_time

			nb_tentatives_A3 += nb_tentativesA3
			nb_tentatives_A4 += nb_tentativesA4
			nb_noeuds_A3 += nb_noeudsA3
			nb_noeuds_A4 += nb_noeudsA4
		yA3_temps.append(temps_A3/nbre_instances)
		yA4_temps.append(temps_A4/nbre_instances)
		yA3_nb_tentatives.append(nb_tentatives_A3/nbre_instances)
		yA4_nb_tentatives.append(nb_tentatives_A4/nbre_instances)
		yA3_nb_noeuds.append(nb_noeuds_A3/nbre_instances)
		yA4_nb_noeuds.append(nb_noeuds_A4/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")

	plt.scatter(x, yA3_temps, c="green", label="A3")
	plt.scatter(x, yA4_temps, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.savefig("1_2_temps_bis.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.scatter(x, yA3_nb_tentatives, c="green", label="A3")
	plt.scatter(x, yA4_nb_tentatives, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.savefig("1_2_nb_tentatives_bis.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.scatter(x, yA3_nb_noeuds, c="green", label="A3")
	plt.scatter(x, yA4_nb_noeuds, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.savefig("1_2_nb_noeuds_bis.png")
	plt.show()

#################################################################################################################################################################################################

def graphe1_3(tailles_n,nbre_instances):
	x = []
	yA3_temps = []
	yA5_temps = []
	yA3_nb_tentatives = []
	yA5_nb_tentatives = []
	yA3_nb_noeuds = []
	yA5_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A3 = 0
		temps_A5 = 0
		nb_tentatives_A3 = 0
		nb_tentatives_A5 = 0
		nb_noeuds_A3 = 0
		nb_noeuds_A5 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()

			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative)
			temps_A5 += time.time() - start_time
			nb_tentatives_A3 += nb_tentativesA3
			nb_tentatives_A5 += nb_tentativesA5
			nb_noeuds_A3 += nb_noeudsA3
			nb_noeuds_A5 += nb_noeudsA5
		yA3_temps.append(temps_A3/nbre_instances)
		yA5_temps.append(temps_A5/nbre_instances)
		yA3_nb_tentatives.append(nb_tentatives_A3/nbre_instances)
		yA5_nb_tentatives.append(nb_tentatives_A5/nbre_instances)
		yA3_nb_noeuds.append(nb_noeuds_A3/nbre_instances)
		yA5_nb_noeuds.append(nb_noeuds_A5/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA3_temps, c="green", label="A3")
	plt.plot(x, yA5_temps, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.savefig("1_3_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA3_nb_tentatives, c="green", label="A3")
	plt.plot(x, yA5_nb_tentatives, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.savefig("1_3_nb_tentatives.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA3_nb_noeuds, c="green", label="A3")
	plt.plot(x, yA5_nb_noeuds, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.savefig("1_3_nb_noeuds.png")
	plt.show()

#################################################################################################################################################################################################

def graphe1_4(tailles_n,nbre_instances):
	x = []
	yA5_temps = []
	yA6_temps = []
	yA7_temps = []
	yA5_nb_tentatives = []
	yA6_nb_tentatives = []
	yA7_nb_tentatives = []
	yA5_nb_noeuds = []
	yA6_nb_noeuds = []
	yA7_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A5 = 0
		temps_A6 = 0
		temps_A7 = 0
		nb_tentatives_A5 = 0
		nb_tentatives_A6 = 0
		nb_tentatives_A7 = 0
		nb_noeuds_A5 = 0
		nb_noeuds_A6 = 0
		nb_noeuds_A7 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative)
			temps_A5 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA6,nb_noeudsA6 = run(n,6,code_secret,premiere_tentative) 
			temps_A6 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA7,nb_noeudsA7 = run(n,7,code_secret,premiere_tentative)
			temps_A7 += time.time() - start_time
			nb_tentatives_A5 += nb_tentativesA5
			nb_tentatives_A6 += nb_tentativesA6
			nb_tentatives_A7 += nb_tentativesA7
			nb_noeuds_A5 += nb_noeudsA5
			nb_noeuds_A6 += nb_noeudsA6
			nb_noeuds_A7 += nb_noeudsA7
		yA5_temps.append(temps_A5/nbre_instances)
		yA6_temps.append(temps_A6/nbre_instances)
		yA7_temps.append(temps_A7/nbre_instances)
		yA5_nb_tentatives.append(nb_tentatives_A5/nbre_instances)
		yA6_nb_tentatives.append(nb_tentatives_A6/nbre_instances)
		yA7_nb_tentatives.append(nb_tentatives_A7/nbre_instances)
		yA5_nb_noeuds.append(nb_noeuds_A5/nbre_instances)
		yA6_nb_noeuds.append(nb_noeuds_A6/nbre_instances)
		yA7_nb_noeuds.append(nb_noeuds_A7/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA5_temps, c="green", label="A5")
	plt.plot(x, yA6_temps, c="blue", label="A6")
	plt.plot(x, yA7_temps, c="red", label="A7")
	plt.legend()
	plt.grid()
	plt.savefig("1_4_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA5_nb_tentatives, c="green", label="A5")
	plt.plot(x, yA6_nb_tentatives, c="blue", label="A6")
	plt.plot(x, yA7_nb_tentatives, c="red", label="A7")
	plt.legend()
	plt.grid()
	plt.savefig("1_4_nb_tentatives.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA5_nb_noeuds, c="green", label="A5")
	plt.plot(x, yA6_nb_noeuds, c="blue", label="A6")
	plt.plot(x, yA7_nb_noeuds, c="red", label="A7")
	plt.legend()
	plt.grid()
	plt.savefig("1_4_nb_noeuds.png")
	plt.show()

def graphe1_4_bis(tailles_n,nbre_instances):
	x = []
	yA5_temps = []
	yA7_temps = []
	yA5_nb_tentatives = []
	yA7_nb_tentatives = []
	yA5_nb_noeuds = []
	yA7_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A5 = 0
		temps_A7 = 0
		nb_tentatives_A5 = 0
		nb_tentatives_A7 = 0
		nb_noeuds_A5 = 0
		nb_noeuds_A7 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative)
			temps_A5 += time.time() - start_time
			start_time = time.time()
			nb_tentativesA7,nb_noeudsA7 = run(n,7,code_secret,premiere_tentative)
			temps_A7 += time.time() - start_time
			nb_tentatives_A5 += nb_tentativesA5
			nb_tentatives_A7 += nb_tentativesA7
			nb_noeuds_A5 += nb_noeudsA5
			nb_noeuds_A7 += nb_noeudsA7
		yA5_temps.append(temps_A5/nbre_instances)
		yA7_temps.append(temps_A7/nbre_instances)
		yA5_nb_tentatives.append(nb_tentatives_A5/nbre_instances)
		yA7_nb_tentatives.append(nb_tentatives_A7/nbre_instances)
		yA5_nb_noeuds.append(nb_noeuds_A5/nbre_instances)
		yA7_nb_noeuds.append(nb_noeuds_A7/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA5_temps, c="green", label="A5")
	plt.plot(x, yA7_temps, c="red", label="A7")
	plt.legend()
	plt.grid()
	plt.savefig("1_4_temps_bis.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA5_nb_tentatives, c="green", label="A5")
	plt.plot(x, yA7_nb_tentatives, c="red", label="A7")
	plt.legend()
	plt.grid()
	plt.savefig("1_4_nb_tentatives_bis.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA5_nb_noeuds, c="green", label="A5")
	plt.plot(x, yA7_nb_noeuds, c="red", label="A7")
	plt.legend()
	plt.grid()
	plt.savefig("1_4_nb_noeuds_bis.png")
	plt.show()

#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

def graphe2_1_mutpb(tailles_n,nbre_instances,maxsize,maxgen,popsize,cxpb):
	liste_mutpb = np.linspace(0.0, 1.0, 11)
	liste_n_temps = []
	liste_n_nb_tentatives = []
	for n in tailles_n:
		yAG_temps = []
		yAG_nb_tentatives = []
		liste_codes_secrets = []
		liste_premieres_tentatives = []
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			liste_codes_secrets.append(mm_temp.get_code_secret())
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			liste_premieres_tentatives.append(mm_temp0.get_code_secret())
		for mutpb in liste_mutpb:
			temps_AG = 0
			nb_tentatives_AG = 0
			for i in range(nbre_instances):
				code_secret = liste_codes_secrets[i]
				premiere_tentative_liste = liste_premieres_tentatives[i]
				premiere_tentative = {}
				for i in range(len(premiere_tentative_liste)):
					premiere_tentative[i] = premiere_tentative_liste[i]
				start_time = time.time()
				nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
				temps_AG += time.time() - start_time
				nb_tentatives_AG += nb_tentativesAG
			yAG_temps.append(temps_AG/nbre_instances)
			yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)
		liste_n_temps.append(yAG_temps)
		liste_n_nb_tentatives.append(yAG_nb_tentatives)

	titre = "Evolution du temps moyen de résolution en fonction de mutpb"
	plt.title(titre)
	plt.xlabel("Probabilité de mutation")
	plt.ylabel("Temps moyen en secondes")	
	for i in range(len(liste_n_temps)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_mutpb, liste_n_temps[i], label=titre)
	plt.legend()
	plt.grid()
	plt.savefig("2_1_temps_mutpb.png")
	plt.show()

	titre = "Evolution du nombre moyen d’essais nécessaires en fonction de mutpb"
	plt.title(titre)
	plt.xlabel("Probabilité de mutation")
	plt.ylabel("Nombre moyen d’essais")	
	for i in range(len(liste_n_nb_tentatives)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_mutpb, liste_n_nb_tentatives[i], label=titre)	
	plt.legend()
	plt.grid()
	plt.savefig("2_1_nb_tentatives_mutpb.png")
	plt.show()

#################################################################################################################################################################################################

def graphe2_1_cxpb(tailles_n,nbre_instances,maxsize,maxgen,popsize,mutpb):
	liste_cxpb = np.linspace(0.0, 1.0, 11)
	liste_n_temps = []
	liste_n_nb_tentatives = []
	for n in tailles_n:
		yAG_temps = []
		yAG_nb_tentatives = []
		liste_codes_secrets = []
		liste_premieres_tentatives = []
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			liste_codes_secrets.append(mm_temp.get_code_secret())
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			liste_premieres_tentatives.append(mm_temp0.get_code_secret())
		for cxpb in liste_cxpb:
			temps_AG = 0
			nb_tentatives_AG = 0
			for i in range(nbre_instances):
				code_secret = liste_codes_secrets[i]
				premiere_tentative_liste = liste_premieres_tentatives[i]
				premiere_tentative = {}
				for i in range(len(premiere_tentative_liste)):
					premiere_tentative[i] = premiere_tentative_liste[i]
				start_time = time.time()
				nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
				temps_AG += time.time() - start_time
				nb_tentatives_AG += nb_tentativesAG
			yAG_temps.append(temps_AG/nbre_instances)
			yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)
		liste_n_temps.append(yAG_temps)
		liste_n_nb_tentatives.append(yAG_nb_tentatives)

	titre = "Evolution du temps moyen de résolution en fonction de cxpb"
	plt.title(titre)
	plt.xlabel("Probabilité de crossover")
	plt.ylabel("Temps moyen en secondes")	
	for i in range(len(liste_n_temps)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_cxpb, liste_n_temps[i], label=titre)
	plt.legend()
	plt.grid()
	plt.savefig("2_1_temps_cxpb.png")
	plt.show()

	titre = "Evolution du nombre moyen d’essais nécessaires en fonction de cxpb"
	plt.title(titre)
	plt.xlabel("Probabilité de crossover")
	plt.ylabel("Nombre moyen d’essais")	
	for i in range(len(liste_n_nb_tentatives)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_cxpb, liste_n_nb_tentatives[i], label=titre)	
	plt.legend()
	plt.grid()
	plt.savefig("2_1_nb_tentatives_cxpb.png")
	plt.show()

#################################################################################################################################################################################################

def graphe2_1_maxsize(tailles_n,nbre_instances,maxgen,popsize,cxpb,mutpb):
	liste_maxsize = np.linspace(0.0, 100.0, 11)
	liste_n_temps = []
	liste_n_nb_tentatives = []
	for n in tailles_n:
		yAG_temps = []
		yAG_nb_tentatives = []
		liste_codes_secrets = []
		liste_premieres_tentatives = []
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			liste_codes_secrets.append(mm_temp.get_code_secret())
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			liste_premieres_tentatives.append(mm_temp0.get_code_secret())
		for maxsize in liste_maxsize:
			temps_AG = 0
			nb_tentatives_AG = 0
			for i in range(nbre_instances):
				code_secret = liste_codes_secrets[i]
				premiere_tentative_liste = liste_premieres_tentatives[i]
				premiere_tentative = {}
				for i in range(len(premiere_tentative_liste)):
					premiere_tentative[i] = premiere_tentative_liste[i]
				start_time = time.time()
				nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
				temps_AG += time.time() - start_time
				nb_tentatives_AG += nb_tentativesAG
			yAG_temps.append(temps_AG/nbre_instances)
			yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)
		liste_n_temps.append(yAG_temps)
		liste_n_nb_tentatives.append(yAG_nb_tentatives)

	titre = "Evolution du temps moyen de résolution en fonction de maxsize"
	plt.title(titre)
	plt.xlabel("Taille de E")
	plt.ylabel("Temps moyen en secondes")	
	for i in range(len(liste_n_temps)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_maxsize, liste_n_temps[i], label=titre)
	plt.legend()
	plt.grid()
	plt.savefig("2_1_temps_maxsize.png")
	plt.show()

	titre = "Evolution du nombre moyen d’essais nécessaires en fonction de maxsize"
	plt.title(titre)
	plt.xlabel("Taille de E")
	plt.ylabel("Nombre moyen d’essais")	
	for i in range(len(liste_n_nb_tentatives)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_maxsize, liste_n_nb_tentatives[i], label=titre)	
	plt.legend()
	plt.grid()
	plt.savefig("2_1_nb_tentatives_maxsize.png")
	plt.show()

#################################################################################################################################################################################################

def graphe2_1_popsize(tailles_n,nbre_instances,maxsize,maxgen,cxpb,mutpb):
	liste_popsize = []
	for i in range(1,11):
		liste_popsize.append(i*10)
	liste_n_temps = []
	liste_n_nb_tentatives = []
	for n in tailles_n:
		yAG_temps = []
		yAG_nb_tentatives = []
		liste_codes_secrets = []
		liste_premieres_tentatives = []
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			liste_codes_secrets.append(mm_temp.get_code_secret())
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			liste_premieres_tentatives.append(mm_temp0.get_code_secret())
		for popsize in liste_popsize:
			#print("popsize :",popsize)
			temps_AG = 0
			nb_tentatives_AG = 0
			for i in range(nbre_instances):
				code_secret = liste_codes_secrets[i]
				premiere_tentative_liste = liste_premieres_tentatives[i]
				premiere_tentative = {}
				for i in range(len(premiere_tentative_liste)):
					premiere_tentative[i] = premiere_tentative_liste[i]
				start_time = time.time()
				nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
				temps_AG += time.time() - start_time
				nb_tentatives_AG += nb_tentativesAG
			yAG_temps.append(temps_AG/nbre_instances)
			yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)
		liste_n_temps.append(yAG_temps)
		liste_n_nb_tentatives.append(yAG_nb_tentatives)

	titre = "Evolution du temps moyen de résolution en fonction de popsize"
	plt.title(titre)
	plt.xlabel("Taille de la population")
	plt.ylabel("Temps moyen en secondes")	
	for i in range(len(liste_n_temps)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_popsize, liste_n_temps[i], label=titre)
	plt.legend()
	plt.grid()
	plt.savefig("2_1_temps_popsize.png")
	plt.show()

	titre = "Evolution du nombre moyen d’essais nécessaires en fonction de popsize"
	plt.title(titre)
	plt.xlabel("Taille de la population")
	plt.ylabel("Nombre moyen d’essais")	
	for i in range(len(liste_n_nb_tentatives)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_popsize, liste_n_nb_tentatives[i], label=titre)	
	plt.legend()
	plt.grid()
	plt.savefig("2_1_nb_tentatives_popsize.png")
	plt.show()

#################################################################################################################################################################################################

def graphe2_1_maxgen(tailles_n,nbre_instances,maxsize,popsize,cxpb,mutpb):
	liste_maxgen = []
	for i in range(1,11):
		liste_maxgen.append(i*10)
	liste_n_temps = []
	liste_n_nb_tentatives = []
	for n in tailles_n:
		yAG_temps = []
		yAG_nb_tentatives = []
		liste_codes_secrets = []
		liste_premieres_tentatives = []
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			liste_codes_secrets.append(mm_temp.get_code_secret())
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			liste_premieres_tentatives.append(mm_temp0.get_code_secret())
		for maxgen in liste_maxgen:
			#print("maxgen :",maxgen)
			temps_AG = 0
			nb_tentatives_AG = 0
			for i in range(nbre_instances):
				code_secret = liste_codes_secrets[i]
				premiere_tentative_liste = liste_premieres_tentatives[i]
				premiere_tentative = {}
				for i in range(len(premiere_tentative_liste)):
					premiere_tentative[i] = premiere_tentative_liste[i]
				start_time = time.time()
				nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,popsize=maxgen,CXPB=cxpb,MUTPB=mutpb) 
				temps_AG += time.time() - start_time
				nb_tentatives_AG += nb_tentativesAG
			yAG_temps.append(temps_AG/nbre_instances)
			yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)
		liste_n_temps.append(yAG_temps)
		liste_n_nb_tentatives.append(yAG_nb_tentatives)

	titre = "Evolution du temps moyen de résolution en fonction de maxgen"
	plt.title(titre)
	plt.xlabel("Nombre de générations")
	plt.ylabel("Temps moyen en secondes")	
	for i in range(len(liste_n_temps)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_maxgen, liste_n_temps[i], label=titre)
	plt.legend()
	plt.grid()
	plt.savefig("2_1_temps_maxgen.png")
	plt.show()

	titre = "Evolution du nombre moyen d’essais nécessaires en fonction de maxgen"
	plt.title(titre)
	plt.xlabel("Nombre de générations")
	plt.ylabel("Nombre moyen d’essais")	
	for i in range(len(liste_n_nb_tentatives)):
		titre = "n = "+str(tailles_n[i])
		plt.plot(liste_maxgen, liste_n_nb_tentatives[i], label=titre)	
	plt.legend()
	plt.grid()
	plt.savefig("2_1_nb_tentatives_maxgen.png")
	plt.show()

#################################################################################################################################################################################################

def graphe2_2(tailles_n,nbre_instances,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yAG0_temps = [] # random
	yAG1_temps = [] # plus de similarités
	yAG2_temps = [] # moins de similarités
	yAG3_temps = [] # moins de codes compatibles restants
	yAG4_temps = [] # plus de codes compatibles restants
	yAG0_nb_tentatives = [] # random
	yAG1_nb_tentatives = [] # plus de similarités
	yAG2_nb_tentatives = [] # moins de similarités
	yAG3_nb_tentatives = [] # moins de codes compatibles restants
	yAG4_nb_tentatives = [] # plus de codes compatibles restants
	for n in tailles_n:
		x.append(n)
		temps_AG0 = 0
		temps_AG1 = 0
		temps_AG2 = 0
		temps_AG3 = 0
		temps_AG4 = 0
		nb_tentatives_AG0 = 0
		nb_tentatives_AG1 = 0
		nb_tentatives_AG2 = 0
		nb_tentatives_AG3 = 0
		nb_tentatives_AG4 = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesAG0,nb_noeudsAG0 = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG0 += time.time() - start_time
			start_time = time.time()
			nb_tentativesAG1,nb_noeudsAG1 = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=1,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG1 += time.time() - start_time
			start_time = time.time()
			nb_tentativesAG2,nb_noeudsAG2 = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=2,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG2 += time.time() - start_time
			start_time = time.time()
			nb_tentativesAG3,nb_noeudsAG3 = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=3,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG3 += time.time() - start_time
			start_time = time.time()
			nb_tentativesAG4,nb_noeudsAG4 = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=4,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG4 += time.time() - start_time
			nb_tentatives_AG0 += nb_tentativesAG0
			nb_tentatives_AG1 += nb_tentativesAG1
			nb_tentatives_AG2 += nb_tentativesAG2
			nb_tentatives_AG3 += nb_tentativesAG3
			nb_tentatives_AG4 += nb_tentativesAG4
		yAG0_temps.append(temps_AG0/nbre_instances)
		yAG1_temps.append(temps_AG1/nbre_instances)
		yAG2_temps.append(temps_AG2/nbre_instances)
		yAG3_temps.append(temps_AG3/nbre_instances)
		yAG4_temps.append(temps_AG4/nbre_instances)
		yAG0_nb_tentatives.append(nb_tentatives_AG0/nbre_instances)
		yAG1_nb_tentatives.append(nb_tentatives_AG1/nbre_instances)
		yAG2_nb_tentatives.append(nb_tentatives_AG2/nbre_instances)
		yAG3_nb_tentatives.append(nb_tentatives_AG3/nbre_instances)
		yAG4_nb_tentatives.append(nb_tentatives_AG4/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yAG0_temps, label="AG0")
	plt.plot(x, yAG1_temps, label="AG1")
	plt.plot(x, yAG2_temps, label="AG2")
	plt.plot(x, yAG3_temps, label="AG3")
	plt.plot(x, yAG4_temps, label="AG4")
	plt.legend()
	plt.grid()
	plt.savefig("2_2_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yAG0_nb_tentatives, label="AG0")
	plt.plot(x, yAG1_nb_tentatives, label="AG1")
	plt.plot(x, yAG2_nb_tentatives, label="AG2")
	plt.plot(x, yAG3_nb_tentatives, label="AG3")
	plt.plot(x, yAG4_nb_tentatives, label="AG4")
	plt.legend()
	plt.grid()
	plt.savefig("2_2_nb_tentatives.png")
	plt.show()

#################################################################################################################################################################################################

def graphe2_3(tailles_n,nbre_instances,meilleure_strategie_partie_1,strategie_algo_genetique,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yA_temps = []
	yAG_temps = []
	yA_nb_tentatives = []
	yAG_nb_tentatives = []
	for n in tailles_n:
		x.append(n)
		temps_A = 0
		temps_AG = 0
		nb_tentatives_A = 0
		nb_tentatives_AG = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA,nb_noeudsA = run(n,meilleure_strategie_partie_1,code_secret,premiere_tentative)
			temps_A += time.time() - start_time
			start_time = time.time()
			nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=strategie_algo_genetique,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
			temps_AG += time.time() - start_time
			nb_tentatives_A += nb_tentativesA
			nb_tentatives_AG += nb_tentativesAG
		yA_temps.append(temps_A/nbre_instances)
		yAG_temps.append(temps_AG/nbre_instances)
		yA_nb_tentatives.append(nb_tentatives_A/nbre_instances)
		yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA_temps, c="green", label="A")
	plt.plot(x, yAG_temps, c="red", label="AG")
	plt.legend()
	plt.grid()
	plt.savefig("2_3_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA_nb_tentatives, c="green", label="A")
	plt.plot(x, yAG_nb_tentatives, c="red", label="AG")
	plt.legend()
	plt.grid()
	plt.savefig("2_3_nb_tentatives.png")
	plt.show()

#################################################################################################################################################################################################

def graphe3(tailles_n,nbre_instances,meilleure_strategie_partie_1,strategie_algo_genetique,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yA_temps = []
	yAG_temps = []
	yAH_temps = []
	yA_nb_tentatives = []
	yAG_nb_tentatives = []
	yAH_nb_tentatives = []
	yA_nb_noeuds = []
	yAH_nb_noeuds = []
	for n in tailles_n:
		x.append(n)
		temps_A = 0
		temps_AG = 0
		temps_AH = 0
		nb_tentatives_A = 0
		nb_tentatives_AG = 0
		nb_tentatives_AH = 0
		nb_noeuds_A = 0
		nb_noeuds_AH = 0
		for i in range(nbre_instances):
			mm_temp = Mastermind(n)
			mm_temp.create_code_secret_random()
			code_secret = mm_temp.get_code_secret()
			mm_temp0 = Mastermind(n)
			mm_temp0.create_code_secret_random()
			premiere_tentative_liste = mm_temp0.get_code_secret()
			premiere_tentative = {}
			for i in range(len(premiere_tentative_liste)):
				premiere_tentative[i] = premiere_tentative_liste[i]
			start_time = time.time()
			nb_tentativesA,nb_noeudsA = run(n,meilleure_strategie_partie_1,code_secret,premiere_tentative)
			temps_A += time.time() - start_time
			start_time = time.time()
			nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=8,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=strategie_algo_genetique,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
			temps_AG += time.time() - start_time
			start_time = time.time()
			nb_tentativesAH,nb_noeudsAH = run(n=n,joueur=9,code_secret=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=strategie_algo_genetique,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
			temps_AH += time.time() - start_time
			nb_tentatives_A += nb_tentativesA
			nb_tentatives_AG += nb_tentativesAG
			nb_tentatives_AH += nb_tentativesAH
			nb_noeuds_A += nb_noeudsA
			nb_noeuds_AH += nb_noeudsAH
		yA_temps.append(temps_A/nbre_instances)
		yAG_temps.append(temps_AG/nbre_instances)
		yAH_temps.append(temps_AH/nbre_instances)
		yA_nb_tentatives.append(nb_tentatives_A/nbre_instances)
		yAG_nb_tentatives.append(nb_tentatives_AG/nbre_instances)
		yAH_nb_tentatives.append(nb_tentatives_AH/nbre_instances)
		yA_nb_noeuds.append(nb_noeuds_A/nbre_instances)
		yAH_nb_noeuds.append(nb_noeuds_AH/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA_temps, c="green", label="A")
	plt.plot(x, yAG_temps, c="red", label="AG")
	plt.plot(x, yAH_temps, c="blue", label="AH")
	plt.legend()
	plt.grid()
	plt.savefig("3_temps.png")
	plt.show()

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA_nb_tentatives, c="green", label="A")
	plt.plot(x, yAG_nb_tentatives, c="red", label="AG")
	plt.plot(x, yAH_nb_tentatives, c="blue", label="AH")
	plt.legend()
	plt.grid()
	plt.savefig("3_nb_tentatives.png")
	plt.show()

	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA_nb_noeuds, c="green", label="A")
	plt.plot(x, yAH_nb_noeuds, c="blue", label="AH")
	plt.legend()
	plt.grid()
	plt.savefig("3_nb_noeuds.png")
	plt.show()

#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

# Tests :

'''
n = 4
joueur = 5
strategie_algo_genetique = 0
maxsize = 10
maxgen = 105
popsize = 50
CXPB = 0.6
MUTPB = 0.4

mm_temp = Mastermind(n)
mm_temp.create_code_secret_random()
code_secret = mm_temp.get_code_secret()

#print("code_secret :",code_secret)

mm_temp0 = Mastermind(n)
mm_temp0.create_code_secret_random()
premiere_tentative_liste = mm_temp0.get_code_secret()
premiere_tentative_dico = {}
for i in range(len(premiere_tentative_liste)):
	premiere_tentative_dico[i] = premiere_tentative_liste[i]

#print("premiere_tentative_dico :",premiere_tentative_dico)
'''

'''
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
'''

'''
print("n =",n)
print("premiere tentative :",premiere_tentative_liste)
#print("code_secret sans doublon :",code_secret)
joueur = 1
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 2
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 3
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 4
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 5
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 6
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 7
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")
joueur = 8
start_time = time.time()
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds,"; Temps d'exécution :",time.time() - start_time,"secondes.")

print("Le fichier s'est chargé sans problème. Prêt à tracer les courbes.")
'''

# Tests sur 1000 runs pour essayer toutes les situations
'''
for i in range(1000):
	print("Run",i)
	mm_temp = Mastermind(n)
	mm_temp.create_code_secret_random()
	code_secret = mm_temp.get_code_secret()
	mm_temp0 = Mastermind(n)
	mm_temp0.create_code_secret_random()
	premiere_tentative_liste = mm_temp0.get_code_secret()
	premiere_tentative_dico = {}
	for i in range(len(premiere_tentative_liste)):
		premiere_tentative_dico[i] = premiere_tentative_liste[i]
	nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
'''