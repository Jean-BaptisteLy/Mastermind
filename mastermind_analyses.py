import random
import copy
import time
from copy import deepcopy
#import numpy as np
#import matplotlib.pyplot as plt

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
		self.code_tentative = deepcopy(tentative)

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
	n : contrainte
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
		if compatibilite(n,states,res):
			break
	return res,nbre_noeuds

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
			
			if (joueur == 9):
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

			elif (joueur == 6): # bonus : Las Vegas
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

			elif (joueur == 7): # algorithme génétique

				E = [] # ensemble de codes compatibles
				res = {}
				
				if mastermind.get_nb_tentatives() == 0:
					D_temp = D.copy()
					for i in range(n):
						temp = random.choice(D_temp)
						res[i] = temp
						D_temp.remove(temp)
					historique = {}

				else:
					# Evaluation de l'historique en fonction du secret
					fitness = (mastermind.get_n()*2) * mastermind.get_states()[mastermind.get_nb_tentatives()][1] + mastermind.get_states()[mastermind.get_nb_tentatives()][2]
					historique[mastermind.get_nb_tentatives()] = fitness
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
											child = random.choice(parents_temp)
											alea = random.randint(0,len(child)-1)
											child[0][alea] = random.choice(D)
											for i in range(n):
												individu[i] = child[0][i]
										else:
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]

								# Test de l'individu par rapport à l'historique
								mm_temp = Mastermind(n)
								fitnessN = 0
								for t,s in mastermind.get_states().items():
									code_temp = []
									for i in s[0].values():
										code_temp.append(i)
									mm_temp.create_code_secret(code_temp)
									mm_temp.create_code_tentative(individu)
									mm_temp.comparaison()
									fitness = (mm_temp.get_n()*2) * mm_temp.get_states()[mm_temp.get_nb_tentatives()][1] + mm_temp.get_states()[mm_temp.get_nb_tentatives()][2]
									
									if mastermind.get_nb_tentatives() > 0:
										fitnessN += abs(fitness - historique[t])
									else:
										fitnessN = fitness
								nouvelle_population.append((individu,fitnessN))

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
							seuil = 99999999999999 # facultatif : à mettre très grand pour que ça devienne inexistant
							population_copie = deepcopy(population)
							for i in range(len(population_copie)):
								hof_individu,hof_fitness = min(population_copie, key = lambda t: t[1])
								if hof_fitness > seuil: # ça ne sert à rien de continuer
									break
								uniques_values = []
								for key, d in hof_individu.items():
								    if d[0] not in uniques_values:
								        uniques_values.append(d[0])
								if len(uniques_values) == len(hof_individu):
									if hof_fitness < seuil:	# réussite
										code_temp = []
										for i in hof_individu.values():
											code_temp.append(i)
										if compatibilite(mastermind.get_n(),mastermind.get_states(),code_temp):
											E.append((hof_individu,hof_fitness))
											#print(hof_individu,hof_fitness)
											break
								else:
									population_copie.remove((hof_individu,hof_fitness))

							if len(E) == maxsize:
								break

						#print("dernière population :",population)
						#print("E :",E)
						if len(E) == 0:
							temp_time = (time.time() - start_time)
							#print("Temps d'exécution : %s secondes ---" % temp_time)
							if temp_time > 300:
								continuer = False
								print("Echec de l'algorithme génétique. \n")
						else:
							if strategie_algo_genetique == 0:													
								res,res_individu_fitness = random.choice(E) # random
							elif strategie_algo_genetique == 1:
								res,res_individu_fitness = min(E, key = lambda t: t[1]) # sélectionne la meilleure fitness
							elif strategie_algo_genetique == 2:
								res,res_individu_fitness = max(E, key = lambda t: t[1]) # sélectionne la pire fitness
							elif strategie_algo_genetique == 3:
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
							elif strategie_algo_genetique == 4:
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

							elif strategie_algo_genetique == 5:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								longueur_S = len(E)
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
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
								res,res_individu_fitness = E[estimations.index(min(estimations))]
							elif strategie_algo_genetique == 6:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								longueur_S = len(E)
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
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
								res,res_individu_fitness = E[estimations.index(max(estimations))]
							continuer = False
			
			#################################################################################################################################################################################################
			if len(res) == 0:
				#print("seuil :",seuil)
				#print("dernière population :",population)
				if(mastermind.get_nb_tentatives() > 0):
					print("\nRésumé de toutes les tentatives :")
					for i in mastermind.get_states():
						print("Tentative",i,":",mastermind.get_states()[i][0],"bien placés :",mastermind.get_states()[i][1],"mal placés :",mastermind.get_states()[i][2])
				print("\nAucun code compatible de trouvé. \n")
				print("Arrêt sans victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				print("La bonne réponse était :",reponse,"\n")
				input()
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
			if mastermind.get_nb_tentatives() == 10:
				print("Arrêt sans victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				break
			'''
	if joueur != 0:
		return mastermind.get_nb_tentatives(),nbre_noeuds

#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

def graphe1_1_evolution_temps(tailles_n,nbre_instances):
	x = []
	yA1 = []
	yA2 = []
	yA3 = []
	for n in tailles_n:
		x.append(n)
		temps_A1 = 0
		temps_A2 = 0
		temps_A3 = 0
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
			run(n,1,code_secret,premiere_tentative)
			temps_A1 += time.time() - start_time
			start_time = time.time()
			run(n,2,code_secret,premiere_tentative)
			temps_A2 += time.time() - start_time
			start_time = time.time()
			run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time
		yA1.append(temps_A1/nbre_instances)
		yA2.append(temps_A2/nbre_instances)
		yA3.append(temps_A3/nbre_instances)
	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA1, c="green", label="A1")
	plt.plot(x, yA2, c="blue", label="A2")
	plt.plot(x, yA3, c="red", label="A3")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_1_evolution_nbre_essais(tailles_n,nbre_instances):
	x = []
	yA1 = []
	yA2 = []
	yA3 = []
	for n in tailles_n:
		x.append(n)
		nb_tentatives_A1 = 0
		nb_tentatives_A2 = 0
		nb_tentatives_A3 = 0
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
			nb_tentativesA1,nb_noeudsA1 = run(n,1,code_secret,premiere_tentative)
			nb_tentativesA2,nb_noeudsA2 = run(n,2,code_secret,premiere_tentative) 
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			nb_tentatives_A1 += nb_tentativesA1
			nb_tentatives_A2 += nb_tentativesA2
			nb_tentatives_A3 += nb_tentativesA3
		yA1.append(nb_tentatives_A1/nbre_instances)
		yA2.append(nb_tentatives_A2/nbre_instances)
		yA3.append(nb_tentatives_A3/nbre_instances)
	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA1, c="green", label="A1")
	plt.plot(x, yA2, c="blue", label="A2")
	plt.plot(x, yA3, c="red", label="A3")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_1_evolution_nbre_noeuds(tailles_n,nbre_instances):
	x = []
	yA1 = []
	yA2 = []
	yA3 = []
	for n in tailles_n:
		x.append(n)
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
			nb_tentativesA1,nb_noeudsA1 = run(n,1,code_secret,premiere_tentative)
			nb_tentativesA2,nb_noeudsA2 = run(n,2,code_secret,premiere_tentative) 
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			nb_noeuds_A1 += nb_noeudsA1
			nb_noeuds_A2 += nb_noeudsA2
			nb_noeuds_A3 += nb_noeudsA3
		yA1.append(nb_noeuds_A1/nbre_instances)
		yA2.append(nb_noeuds_A2/nbre_instances)
		yA3.append(nb_noeuds_A3/nbre_instances)
	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA1, c="green", label="A1")
	plt.plot(x, yA2, c="blue", label="A2")
	plt.plot(x, yA3, c="red", label="A3")
	plt.legend()
	plt.grid()
	plt.show()

#################################################################################################################################################################################################

def graphe1_2_evolution_temps(tailles_n,nbre_instances):
	x = []
	yA3 = []
	yA4 = []
	for n in tailles_n:
		x.append(n)
		temps_A3 = 0
		temps_A4 = 0
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
			run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time

			start_time = time.time()
			run(n,4,code_secret,premiere_tentative)
			temps_A4 += time.time() - start_time

		yA3.append(temps_A3/nbre_instances)
		yA4.append(temps_A4/nbre_instances)
	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	'''
	plt.plot(x, yA3, c="green", label="A3")
	plt.plot(x, yA4, c="red", label="A4")
	'''
	plt.scatter(x, yA3, c="green", label="A3")
	plt.scatter(x, yA4, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_2_evolution_nbre_essais(tailles_n,nbre_instances):
	x = []
	yA3 = []
	yA4 = []
	for n in tailles_n:
		x.append(n)
		nb_tentatives_A3 = 0
		nb_tentatives_A4 = 0
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

			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			nb_tentativesA4,nb_noeudsA4 = run(n,4,code_secret,premiere_tentative)

			nb_tentatives_A3 += nb_tentativesA3
			nb_tentatives_A4 += nb_tentativesA4
		yA3.append(nb_tentatives_A3/nbre_instances)
		yA4.append(nb_tentatives_A4/nbre_instances)
	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	'''
	plt.plot(x, yA3, c="green", label="A3")
	plt.plot(x, yA4, c="red", label="A4")
	'''
	plt.scatter(x, yA3, c="green", label="A3")
	plt.scatter(x, yA4, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_2_evolution_nbre_noeuds(tailles_n,nbre_instances):
	x = []
	yA3 = []
	yA4 = []
	for n in tailles_n:
		x.append(n)
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

			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			nb_tentativesA4,nb_noeudsA4 = run(n,4,code_secret,premiere_tentative) 

			nb_noeuds_A3 += nb_noeudsA3
			nb_noeuds_A4 += nb_noeudsA4
		yA3.append(nb_noeuds_A3/nbre_instances)
		yA4.append(nb_noeuds_A4/nbre_instances)
	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	'''
	plt.plot(x, yA3, c="green", label="A3")
	plt.plot(x, yA4, c="red", label="A4")
	'''
	plt.scatter(x, yA3, c="green", label="A3")
	plt.scatter(x, yA4, c="red", label="A4")
	plt.legend()
	plt.grid()
	plt.show()

#################################################################################################################################################################################################

def graphe1_3_evolution_temps(tailles_n,nbre_instances):
	x = []
	yA3 = []
	yA5 = []
	for n in tailles_n:
		x.append(n)
		temps_A3 = 0
		temps_A5 = 0
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
			run(n,3,code_secret,premiere_tentative)
			temps_A3 += time.time() - start_time
			start_time = time.time()
			run(n,5,code_secret,premiere_tentative)
			temps_A5 += time.time() - start_time
		yA3.append(temps_A3/nbre_instances)
		yA5.append(temps_A5/nbre_instances)
	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA3, c="green", label="A3")
	plt.plot(x, yA5, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_3_evolution_nbre_essais(tailles_n,nbre_instances):
	x = []
	yA3 = []
	yA5 = []
	for n in tailles_n:
		x.append(n)
		nb_tentatives_A3 = 0
		nb_tentatives_A5 = 0
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
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative) 
			nb_tentatives_A3 += nb_tentativesA3
			nb_tentatives_A5 += nb_tentativesA5
		yA3.append(nb_tentatives_A3/nbre_instances)
		yA5.append(nb_tentatives_A5/nbre_instances)
	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA3, c="green", label="A3")
	plt.plot(x, yA5, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_3_evolution_nbre_noeuds(tailles_n,nbre_instances):
	x = []
	yA3 = []
	yA5 = []
	for n in tailles_n:
		x.append(n)
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
			nb_tentativesA3,nb_noeudsA3 = run(n,3,code_secret,premiere_tentative)
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative) 
			nb_noeuds_A3 += nb_noeudsA3
			nb_noeuds_A5 += nb_noeudsA5
		yA3.append(nb_noeuds_A3/nbre_instances)
		yA5.append(nb_noeuds_A5/nbre_instances)
	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA3, c="green", label="A3")
	plt.plot(x, yA5, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.show()

#################################################################################################################################################################################################

def graphe1_4_evolution_temps(tailles_n,nbre_instances):
	x = []
	yA1 = []
	yA5 = []
	for n in tailles_n:
		x.append(n)
		temps_A1 = 0
		temps_A5 = 0
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
			run(n,1,code_secret,premiere_tentative)
			temps_A1 += time.time() - start_time
			start_time = time.time()
			run(n,5,code_secret,premiere_tentative)
			temps_A5 += time.time() - start_time
		yA1.append(temps_A1/nbre_instances)
		yA5.append(temps_A5/nbre_instances)
	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA1, c="green", label="A1")
	plt.plot(x, yA5, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_4_evolution_nbre_essais(tailles_n,nbre_instances):
	x = []
	yA1 = []
	yA5 = []
	for n in tailles_n:
		x.append(n)
		nb_tentatives_A1 = 0
		nb_tentatives_A5 = 0
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
			nb_tentativesA1,nb_noeudsA1 = run(n,1,code_secret,premiere_tentative)
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative) 
			nb_tentatives_A1 += nb_tentativesA1
			nb_tentatives_A5 += nb_tentativesA5
		yA1.append(nb_tentatives_A1/nbre_instances)
		yA5.append(nb_tentatives_A5/nbre_instances)
	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA1, c="green", label="A1")
	plt.plot(x, yA5, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.show()

def graphe1_4_evolution_nbre_noeuds(tailles_n,nbre_instances):
	x = []
	yA1 = []
	yA5 = []
	for n in tailles_n:
		x.append(n)
		nb_noeuds_A1 = 0
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
			nb_tentativesA1,nb_noeudsA1 = run(n,1,code_secret,premiere_tentative)
			nb_tentativesA5,nb_noeudsA5 = run(n,5,code_secret,premiere_tentative) 
			nb_noeuds_A1 += nb_noeudsA1
			nb_noeuds_A5 += nb_noeudsA5
		yA1.append(nb_noeuds_A1/nbre_instances)
		yA5.append(nb_noeuds_A5/nbre_instances)
	plt.title("Evolution du nombre moyen de noeuds lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen de noeuds")
	plt.plot(x, yA1, c="green", label="A1")
	plt.plot(x, yA5, c="red", label="A5")
	plt.legend()
	plt.grid()
	plt.show()

#################################################################################################################################################################################################

#################################################################################################################################################################################################
#################################################################################################################################################################################################

def graphe2_2_evolution_temps(tailles_n,nbre_instances,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yAG0 = [] # random
	yAG1 = [] # meilleure fitness
	yAG2 = [] # pire fitness
	yAG3 = [] # plus de similarités
	yAG4 = [] # moins de similarités
	yAG5 = [] # moins de codes compatibles restants
	yAG6 = [] # plus de codes compatibles restants
	for n in tailles_n:
		x.append(n)
		temps_AG0 = 0
		temps_AG1 = 0
		temps_AG2 = 0
		temps_AG3 = 0
		temps_AG4 = 0
		temps_AG5 = 0
		temps_AG6 = 0
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
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG0 += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=1,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG1 += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=2,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG2 += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=3,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG3 += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=4,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG4 += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=5,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG5 += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=6,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			temps_AG6 += time.time() - start_time
		yAG0.append(temps_AG0/nbre_instances)
		yAG1.append(temps_AG1/nbre_instances)
		yAG2.append(temps_AG2/nbre_instances)
		yAG3.append(temps_AG3/nbre_instances)
		yAG4.append(temps_AG4/nbre_instances)
		yAG5.append(temps_AG5/nbre_instances)
		yAG6.append(temps_AG6/nbre_instances)

	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yAG0, label="AG0")
	plt.plot(x, yAG1, label="AG1")
	plt.plot(x, yAG2, label="AG2")
	plt.plot(x, yAG3, label="AG3")
	plt.plot(x, yAG4, label="AG4")
	plt.plot(x, yAG5, label="AG5")
	plt.plot(x, yAG6, label="AG6")
	plt.legend()
	plt.grid()
	plt.show()

def graphe2_2_evolution_nbre_essais(tailles_n,nbre_instances,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yAG0 = [] # random
	yAG1 = [] # meilleure fitness
	yAG2 = [] # pire fitness
	yAG3 = [] # plus de similarités
	yAG4 = [] # moins de similarités
	yAG5 = [] # moins de codes compatibles restants
	yAG6 = [] # plus de codes compatibles restants
	for n in tailles_n:
		x.append(n)
		nb_tentatives_AG0 = 0
		nb_tentatives_AG1 = 0
		nb_tentatives_AG2 = 0
		nb_tentatives_AG3 = 0
		nb_tentatives_AG4 = 0
		nb_tentatives_AG5 = 0
		nb_tentatives_AG6 = 0
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
			nb_tentativesAG0,nb_noeudsAG0 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=0,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentativesAG1,nb_noeudsAG1 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=1,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentativesAG2,nb_noeudsAG2 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=2,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentativesAG3,nb_noeudsAG3 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=3,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentativesAG4,nb_noeudsAG4 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=4,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentativesAG5,nb_noeudsAG5 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=5,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentativesAG6,nb_noeudsAG6 = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=6,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb)
			nb_tentatives_AG0 += nb_tentativesAG0
			nb_tentatives_AG1 += nb_tentativesAG1
			nb_tentatives_AG2 += nb_tentativesAG2
			nb_tentatives_AG3 += nb_tentativesAG3
			nb_tentatives_AG4 += nb_tentativesAG4
			nb_tentatives_AG5 += nb_tentativesAG5
			nb_tentatives_AG6 += nb_tentativesAG6
		yAG0.append(nb_tentatives_AG0/nbre_instances)
		yAG1.append(nb_tentatives_AG1/nbre_instances)
		yAG2.append(nb_tentatives_AG2/nbre_instances)
		yAG3.append(nb_tentatives_AG3/nbre_instances)
		yAG4.append(nb_tentatives_AG4/nbre_instances)
		yAG5.append(nb_tentatives_AG5/nbre_instances)
		yAG6.append(nb_tentatives_AG6/nbre_instances)

	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yAG0, label="AG0")
	plt.plot(x, yAG1, label="AG1")
	plt.plot(x, yAG2, label="AG2")
	plt.plot(x, yAG3, label="AG3")
	plt.plot(x, yAG4, label="AG4")
	plt.plot(x, yAG5, label="AG5")
	plt.plot(x, yAG6, label="AG6")
	plt.legend()
	plt.grid()
	plt.show()

#################################################################################################################################################################################################

def graphe2_3_evolution_temps(tailles_n,nbre_instances,meilleure_strategie_partie_1,strategie_algo_genetique,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yA = []
	yAG = []
	for n in tailles_n:
		x.append(n)
		temps_A = 0
		temps_AG = 0
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
			run(n,meilleure_strategie_partie_1,code_secret,premiere_tentative)
			temps_A += time.time() - start_time
			start_time = time.time()
			run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=strategie_algo_genetique,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
			temps_AG += time.time() - start_time
		yA.append(temps_A/nbre_instances)
		yAG.append(temps_AG/nbre_instances)
	plt.title("Evolution du temps moyen de résolution lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Temps moyen en secondes")
	plt.plot(x, yA, c="green", label="A")
	plt.plot(x, yAG, c="red", label="AG")
	plt.legend()
	plt.grid()
	plt.show()

def graphe2_3_evolution_nbre_essais(tailles_n,nbre_instances,meilleure_strategie_partie_1,strategie_algo_genetique,maxsize,maxgen,popsize,cxpb,mutpb):
	x = []
	yA = []
	yAG = []
	for n in tailles_n:
		x.append(n)
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
			nb_tentativesA,nb_noeudsA = run(n,meilleure_strategie_partie_1,code_secret,premiere_tentative)
			nb_tentativesAG,nb_noeudsAG = run(n=n,joueur=7,reponse=code_secret,premiere_tentative=premiere_tentative,strategie_algo_genetique=strategie_algo_genetique,maxsize=maxsize,maxgen=maxgen,popsize=popsize,CXPB=cxpb,MUTPB=mutpb) 
			nb_tentatives_A += nb_tentativesA
			nb_tentatives_AG += nb_tentativesAG
		yA.append(nb_tentatives_A/nbre_instances)
		yAG.append(nb_tentatives_AG/nbre_instances)
	plt.title("Evolution du nombre moyen d’essais nécessaires lorsque n et p augmentent")
	plt.xlabel("Taille n")
	plt.ylabel("Nombre moyen d’essais")
	plt.plot(x, yA, c="green", label="A")
	plt.plot(x, yAG, c="red", label="AG")
	plt.legend()
	plt.grid()
	plt.show()

#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################
#################################################################################################################################################################################################

# Tests :


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
joueur = 5
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
'''

print("n =",n)
print("code_secret sans doublon :",code_secret)
joueur = 1
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
joueur = 2
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
joueur = 3
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
joueur = 4
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
joueur = 5
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)
joueur = 6
nb_tentatives,nbre_noeuds = run(n,joueur,code_secret,premiere_tentative_dico,strategie_algo_genetique,maxsize,maxgen,popsize,CXPB,MUTPB)
print("Joueur",joueur,":","Nombre de tentatives :",nb_tentatives,"; Nombre de noeuds :",nbre_noeuds)

print("Le fichier s'est chargé sans problème. Prêt à tracer les courbes.")


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