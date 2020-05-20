import random
#from constraint import *
import copy
import time
from copy import deepcopy

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
		data = dict([(n,0) for n in set(self.code_secret)])
		for i in range(len(self.code_tentative)):
			if self.code_tentative[i] == self.code_secret[i]:	
				temp_bp += 1
				data[self.code_tentative[i]] += 1
			else:
				if self.code_tentative[i] in self.code_secret:
					if data[self.code_tentative[i]] == self.code_secret.count(self.code_tentative[i]):
						continue
					elif data[self.code_tentative[i]] < self.code_secret.count(self.code_tentative[i]):
						data[self.code_tentative[i]] += 1
						if self.code_secret[self.code_secret.index(self.code_tentative[i])] != self.code_tentative[self.code_secret.index(self.code_tentative[i])]:
							temp_mp += 1
						elif self.code_secret.count(self.code_tentative[i]) == 2:
							temp_mp += 1
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
	compatible = True # renvoie True si code compatible
	mm_temp = Mastermind(n)
	for t,s in states.items(): # on boucle sur les anciennes tentatives, à chaque itération on compare le nombre de pièces bien et mal placées
		code_temp = []
		for i in s[0].values(): # conversion en liste
			code_temp.append(i)
		mm_temp.create_code_secret(code_temp) # liste (tentative)
		mm_temp.create_code_tentative(essai) # dico (code qu'on essaye déterminer sa compatiblité)
		mm_temp.comparaison() # on compare les deux codes
		# si le nombre de pièces bien (ou mal) placées de la tentative courante de la boucle
		# n'est pas égal au nombre de pièces bien (ou mal) placées du code qu'on essaye de déterminer sa compatibilité
		# alors on met le booleen compatible à False
		if mm_temp.get_states()[len(mm_temp.get_states())][1] != s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] != s[2]:
			compatible = False # renvoie false si code non compatible
			break
	return compatible

def compatibilite_doublons(n,states,essai):
	compatible = True
	mm_temp = Mastermind(n)
	for t,s in states.items():
		code_temp = []
		for i in s[0].values():
			code_temp.append(i)
		mm_temp.create_code_secret(code_temp) # liste
		mm_temp.create_code_tentative(essai) # dico
		mm_temp.comparaison_doublons()
		if mm_temp.get_states()[len(mm_temp.get_states())][1] != s[1] or mm_temp.get_states()[len(mm_temp.get_states())][2] != s[2]:
			compatible = False
			break
	return compatible

def engendrer_et_tester(D,n,states):
	'''
	D : domaine des variables
	n : contrainte
	'''
	while True:
		res = {}
		D_temp = D.copy()
		for i in range(n):
			temp = random.choice(D_temp)
			res[i] = temp
			#D_temp.remove(temp) # améliore l'algo en évitant les doublons
		if compatibilite(n,states,res):
			break
	return res

def RAC(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaine des variables
	n et states : les contraintes
	'''
	if nbreVar == 0:
		return i
	else:
		nbreVar -= 1
		for v in D:
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre		
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				if n == len(noeud):
					i_dico = {}
					for j in range(len(noeud)):
						i_dico[j] = noeud[j]
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico
				res = RAC(i+list(v),nbreVar,D,n,states)
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i

def RAC_forward_checking(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaine des variables
	n et states : les contraintes
	'''
	if nbreVar == 0:
		return i
	else:
		nbreVar -= 1
		for v in D:
			D_bis = D.copy()
			D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				if n == len(noeud):
					i_dico = {}
					for j in range(len(noeud)):
						i_dico[j] = noeud[j]
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico
				res = RAC_forward_checking(i+list(v),nbreVar,D_bis,n,states)
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i

def RAC_forward_checking_doublons(i,nbreVar,D,n,states,nbre_occurences):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaine des variables
	n, states, nbre_occurences : les contraintes
	'''
	if nbreVar == 0:
		return i
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
			if n == len(noeud):
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				cd = compatibilite_doublons(n,states,i_dico)
				if cd: # si le code est compatible, on le prend
					return i_dico
			res = RAC_forward_checking_doublons(i+list(v),nbreVar,D_bis,n,states,nbre_occurences_bis)
			if len(res) == n and compatibilite_doublons(n,states,res):
				i = res
				break
	return i

def RAC_forward_checking_ameliore(i,nbreVar,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaine des variables
	n, states : les contraintes
	'''
	if nbreVar == 0:
		return i
	else:
		nbreVar -= 1
		for v in D:
			D_bis = D.copy()
			D_bis.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				if n == len(noeud): # code complet			
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico
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
				res = RAC_forward_checking_ameliore(i+list(v),nbreVar,D_bis,n,states)
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i

def engendrer_et_tester_bonus(D,n,states):
	'''
	D : domaine des variables
	n : contrainte
	'''
	while True:
		res = {}
		D_temp = D.copy()
		for i in range(n):
			temp = random.choice(D_temp)
			res[i] = temp
			D_temp.remove(temp) # améliore l'algo en évitant les doublons
		if compatibilite(n,states,res):
			break
	return res

def run():
	
	print("Veuillez choisir le type de joueur :")
	print("0: je ne veux plus jouer")
	print("1: engendrer et tester")
	print("2: retour arrière chronologique sans forward checking")
	print("3: retour arrière chronologique AVEC forward checking SANS doublons")
	print("4: retour arrière chronologique AVEC forward checking AVEC doublons")
	print("5: retour arrière chronologique AVEC forward checking SANS doublon, AMELIORE")
	print("6: Bonus : engendrer et tester AMELIORE")
	print("7: algorithme génétique")
	print("8: Bonus : ")
	print("9: je veux jouer moi-même")
	joueur = int(input())

	if joueur == 7:		
		print("Veuillez choisir la stratégie de l'algorithme génétique :")
		print("0: random")
		print("1: Bonus : Meilleure fitness")
		print("2: Bonus : Pire fitness")
		print("3: Choix du code présentant le PLUS de similarité avec les autres codes compatibles")
		print("4: Choix du code présentant le MOINS de similarité avec les autres codes compatibles")
		print("5: Estimation du nombre de codes compatibles restants (MOINS) si un code était tenté ")
		print("6: Estimation du nombre de codes compatibles restants (PLUS) si un code était tenté")
		print("7: Bonus : ")
		strategie_algo_genetique = int(input())

	difficulte = 0 # 0 quand l'ordinateur joue
	if joueur == 9:
		print("Veuillez choisir le nombre de joueurs :")
		print("1: 1 joueur")
		print("2: 2 joueurs")
		nbre_joueurs = int(input())

		print("Veuillez choisir la difficulté :")
		print("0: facile : sans doublon")
		print("1: moyen : avec doublon")
		difficulte = int(input())
		
	if (joueur == 0):
		print("Ok.")
	else:
		print("Veuillez choisir le nombre de variables.")
		n = int(input())
		mastermind = Mastermind(n)

		if joueur == 4: # doublons
			mastermind.create_code_secret_random_v2()
		elif joueur == 9:
			if nbre_joueurs == 1:
				if difficulte == 0:
					mastermind.create_code_secret_random()
				elif difficulte == 1:
					mastermind.create_code_secret_random_v2()
			elif nbre_joueurs == 2:
				if difficulte == 0:
					print("Premier joueur : Veuillez votre code secret contenant",mastermind.get_n(),"caractères distincts à l'abri des regards :")
				elif difficulte == 1:
					print("Premier joueur : Veuillez votre code secret contenant",mastermind.get_n(),"caractères à l'abri des regards :")
				code_secret_liste = []
				while(True):
					temp_str = str(input())
					if len(temp_str) == n:
						break
					else:
						if difficulte == 0:
							print("Veuillez ressaisir votre code secret contenant",mastermind.get_n(),"caractères distincts :")
						elif difficulte == 1:
							print("Veuillez ressaisir votre code secret contenant",mastermind.get_n(),"caractères :")
				for i in range(len(temp_str)):
					code_secret_liste.append(temp_str[i])
				mastermind.create_code_secret(code_secret_liste)
		else: # sans doublon
			mastermind.create_code_secret_random()

		reponse = mastermind.get_code_secret()
		#print("La réponse est :",reponse)

		maxsize = 10 # taille maximale de E
		maxgen = 50 # nombre de générations
		popsize = 50 # taille de la population
		CXPB = 0.6 # probabilité de crossover
		MUTPB = 0.4	# probabilité de mutation

		D = mastermind.get_Dp().copy()

		while(True):
			'''
			if(mastermind.get_nb_tentatives() > 0):
				for i in mastermind.get_states():
					print("Tentative",i,":",mastermind.get_states()[i][0],"bien placés :",mastermind.get_states()[i][1],"mal placés :",mastermind.get_states()[i][2])
			
			print("Tentative courante",mastermind.get_nb_tentatives()+1,":")
			'''
			
			if(mastermind.get_nb_tentatives() > 0):
				print("Tentative",len(mastermind.get_states()),":",mastermind.get_states()[len(mastermind.get_states())][0],"bien placés :",mastermind.get_states()[len(mastermind.get_states())][1],"mal placés :",mastermind.get_states()[len(mastermind.get_states())][2])	
			
			#################################################################################################################################################################################################
			
			if (joueur == 9):
				res = []
				if difficulte == 0:
					print("Deuxième joueur : Veuillez saisir votre code contenant",mastermind.get_n(),"caractères distincts :")
				elif difficulte == 1:
					print("Deuxième joueur : Veuillez saisir votre code contenant",mastermind.get_n(),"caractères :")
				while(True):
					temp_str = str(input())
					if len(temp_str) == n:
						break
					else:
						if difficulte == 0:
							print("Deuxième joueur : Veuillez ressaisir votre code contenant",mastermind.get_n(),"caractères distincts :")
						elif difficulte == 1:
							print("Deuxième joueur : Veuillez ressaisir votre code contenant",mastermind.get_n(),"caractères :")
				for i in temp_str:
					res.append(i)

			#################################################################################################################################################################################################

			elif (joueur == 1): # engendrer et tester
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_temp = D.copy()
					for i in range(n):
						temp = random.choice(D_temp)
						res[i] = temp
						D_temp.remove(temp)
				else:
					states = mastermind.get_states()
					res = engendrer_et_tester(D,n,states)

			#################################################################################################################################################################################################

			elif (joueur == 2): # retour arrière chronologique sans forward checking
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_RAC_temp = D_RAC[0].copy()
					for i in range(n):
						temp = random.choice(D_RAC_temp)
						res[i] = temp
						D_RAC_temp.remove(temp)
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res = RAC(i,nbreVar,D,n,states)

			#################################################################################################################################################################################################

			elif (joueur == 3): # retour arrière chronologique AVEC forward checking SANS doublons
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_temp = D.copy()
					for i in range(n):
						temp = random.choice(D_temp)
						res[i] = temp
						D_temp.remove(temp)
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res = RAC_forward_checking(i,nbreVar,D,n,states)

			#################################################################################################################################################################################################

			elif (joueur == 4): # retour arrière chronologique AVEC forward checking AVEC doublons
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					temp_doublons = {}
					D_RAC_temp = D_RAC[0].copy()
					for i in range(n):
						temp = random.choice(D_RAC_temp)
						res[i] = temp
						if temp in temp_doublons:
							temp_doublons[temp] += 1
							D_RAC_temp.remove(temp) # évite les doublons
						else:
							temp_doublons[temp] = 1
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					nbre_occurences = [0] * mastermind.get_p()
					res = RAC_forward_checking_doublons(i,nbreVar,D,n,states,nbre_occurences)

			#################################################################################################################################################################################################

			elif (joueur == 5): # retour arrière chronologique AVEC forward checking SANS doublon, AMELIORE
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_RAC_temp = D_RAC[0].copy()
					for i in range(n):
						temp = random.choice(D_RAC_temp)
						res[i] = temp
						D_RAC_temp.remove(temp) # évite les doublons
				else:
					i = []
					nbreVar = n
					states = mastermind.get_states()
					res = RAC_forward_checking_ameliore(i,nbreVar,D,n,states)

			#################################################################################################################################################################################################

			elif (joueur == 6): # bonus
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_temp = D.copy()
					for i in range(n):
						temp = random.choice(D_temp)
						res[i] = temp
						D_temp.remove(temp)
				else:
					states = mastermind.get_states()
					res = engendrer_et_tester_bonus(D,n,states)

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
			if joueur == 4 or difficulte == 1:
				mastermind.comparaison_doublons()
			else:
				mastermind.comparaison()

			mastermind.check_victoire()

			if mastermind.get_victoire():				
				if(mastermind.get_nb_tentatives() > 0):
					print("##############################################################################")
					print("Résumé de toutes les tentatives :")
					for i in mastermind.get_states():
						print("Tentative",i,":",mastermind.get_states()[i][0],"bien placés :",mastermind.get_states()[i][1],"mal placés :",mastermind.get_states()[i][2])
					print("##############################################################################")
					#input()

				#print("states :",mastermind.get_states())
				print("################################## VICTOIRE ##################################")
				print("La réponse était bien :",reponse)
				print("Victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				break
			'''
			if mastermind.get_nb_tentatives() == 10:
				print("Arrêt sans victoire au bout de",mastermind.get_nb_tentatives(),"tentative(s).")
				break
			'''
						
run()

'''
for i in range(1000):
	print(i)
	run()
'''

# possibilité d'éviter les doublons dans E