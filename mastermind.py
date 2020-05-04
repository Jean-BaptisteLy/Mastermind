import random
from constraint import *
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


def RAC(i,V,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n et states : les contraintes
	'''
	if len(V) == 0:
		return i
	else:
		xk = V[0]
		V_temp = V.copy()
		V_temp.remove(xk)
		for v in D[xk]:
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre		
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				if n == len(noeud):
					i_dico = {}
					for j in range(len(noeud)):
						i_dico[j] = noeud[j]
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico
				res = RAC(i+list(v),V_temp,D,n,states)
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i

def RAC_forward_checking(i,V,D,n,states):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n et states : les contraintes
	'''
	if len(V) == 0:
		return i
	else:
		xk = V[0]
		V_temp = V.copy()
		V_temp.remove(xk)
		for v in D[xk]:
			#print("v :",v)
			D_bis = deepcopy(D)
			for d in D_bis:
				if v in d:
					d.remove(v)
			#print("D_bis :",D_bis)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			if len(noeud) == len(set(noeud)): # si c'est localement consistant : caractères uniques
				if n == len(noeud):
					i_dico = {}
					for j in range(len(noeud)):
						i_dico[j] = noeud[j]
					if compatibilite(n,states,i_dico): # si le code est compatible, on le prend
						return i_dico
				res = RAC_forward_checking(i+list(v),V_temp,D_bis,n,states)
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i

def RAC_forward_checking_doublons(i,V,D,n,states,nbre_occurences):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n, states, nbre_occurences : les contraintes
	'''
	if len(V) == 0:
		return i
	else:
		xk = V[0]
		V_temp = V.copy()
		V_temp.remove(xk)
		for j in range(len(D[xk])):
			nbre_occurences_bis = nbre_occurences.copy()
			v = D[xk][j]
			nbre_occurences_bis[j] += 1
			D_bis = deepcopy(D)
			if nbre_occurences_bis[j] == 2:
				for d in D_bis:
					if v in d:
						d.remove(v)
			noeud = i + list(v)
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			if n == len(noeud):
				i_dico = {}
				for j in range(len(noeud)):
					i_dico[j] = noeud[j]
				cd = compatibilite_doublons(n,states,i_dico)
				if cd: # si le code est compatible, on le prend
					return i_dico
			res = RAC_forward_checking_doublons(i+list(v),V_temp,D_bis,n,states,nbre_occurences_bis)
			if len(res) == n and compatibilite_doublons(n,states,res):
				i = res
				break
	return i

def RAC_forward_checking_ameliore(i,V,D,n,states,nbre_places):
	'''
	i : instanciation courante
	V : liste de variables non-instanciées dans i
	D : domaines des variables
	n et states : les contraintes
	'''
	if len(V) == 0:
		return i
	else:
		xk = V[0]
		V_temp = V.copy()
		V_temp.remove(xk)
		for v in D[xk]:
			#print("v :",v)
			D_bis = deepcopy(D)
			for d in D_bis:
				if v in d:
					d.remove(v)
			#print("D_bis :",D_bis)
			noeud = i + list(v)
			#print("i :",i)
			#print("v :",list(v))
			#print("noeud :",noeud) # permet de voir tous les noeuds de l'arbre
			#input()
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
				#print("i :",i)
				#print("v :",list(v))
				res = RAC_forward_checking_ameliore(i+list(v),V_temp,D_bis,n,states,nbre_places)
				if len(res) == n and compatibilite(n,states,res):
					i = res
					break
	return i

def run():
	'''
	print("Veuillez choisir le type de joueur :")
	print("0: je ne veux plus jouer")
	print("1: engendrer et tester")
	print("2: retour arrière chronologique sans forward checking")
	print("3: retour arrière chronologique AVEC forward checking SANS doublons")
	print("4: retour arrière chronologique AVEC forward checking AVEC doublons")
	print("5: retour arrière chronologique AVEC forward checking SANS doublon, AMELIORE")
	print("6: Bonus : ")
	print("7: algorithme génétique")
	print("8: bonus")
	print("9: je veux jouer moi-même")
	joueur = int(input())
	'''

	joueur = 5

	if joueur == 7:
		'''
		print("Veuillez choisir la stratégie de l'algorithme génétique :")
		print("0: random")
		print("1: Choix du code présentant le PLUS de similarité avec les autres codes compatibles")
		print("2: Choix du code présentant le MOINS de similarité avec les autres codes compatibles")
		print("3: Estimation du nombre de codes compatibles restants (MOINS) si un code était tenté ")
		print("4: Estimation du nombre de codes compatibles restants (PLUS) si un code était tenté")
		print("5: Bonus : Meilleure fitness")
		print("6: Bonus : Pire fitness")
		print("7: Bonus : ")
		strategie_algo_genetique = int(input())
		'''
		strategie_algo_genetique = 1

	if (joueur == 0):
		print("Ok.")
	else:
		'''	
		print("Veuillez choisir le nombre de variables.")
		n = int(input())
		'''
		n = 4
		mastermind = Mastermind(n)

		if joueur == 4: # doublons
			mastermind.create_code_secret_random_v2()
		elif joueur == 9:
			print("Premier joueur : Veuillez votre code secret à l'abri des regards :")

		else: # sans doublon
			mastermind.create_code_secret_random()

		#mastermind.create_code_secret(['7', '7', '2', '6'])
		#mastermind.create_code_secret(['0', '1', '0', '2'])
		#mastermind.create_code_secret(['3', '5', '3', '1'])
		#mastermind.create_code_secret(['1', '1', '3', '3'])
		#mastermind.create_code_secret(['6', '1', '5', '7'])

		reponse = mastermind.get_code_secret()
		print("La réponse est :",reponse)

		maxsize = 10 # taille maximale de E
		maxgen = 105 # nombre de générations
		popsize = 50 # taille de la population
		CXPB = 0.6
		MUTPB = 0.4	

		D_engendrer_et_tester = mastermind.get_Dp().copy()

		D_RAC = []
		for i in range(n):
			temp = mastermind.get_Dp().copy()
			D_RAC.append(temp)
		V_RAC = []
		for i in range(0,n):
			V_RAC.append(i)

		D_algoGen = mastermind.get_Dp().copy()

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
					D_engendrer_et_tester_temp = D_engendrer_et_tester.copy()
					for i in range(n):
						temp = random.choice(D_engendrer_et_tester_temp)
						res[i] = temp
						D_engendrer_et_tester_temp.remove(temp)
				else:
					while True:
						res = {}
						D_engendrer_et_tester_temp = D_engendrer_et_tester.copy()
						for i in range(n):
							temp = random.choice(D_engendrer_et_tester_temp)
							res[i] = temp
							D_engendrer_et_tester_temp.remove(temp) # améliore l'algo en évitant les doublons
						if compatibilite(mastermind.get_n(),mastermind.get_states(),res):
							break

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
					V = V_RAC.copy()
					D = deepcopy(D_RAC)
					states = mastermind.get_states()
					res = RAC(i,V,D,n,states)

			#################################################################################################################################################################################################

			elif (joueur == 3): # retour arrière chronologique AVEC forward checking SANS doublons
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_RAC_temp = D_RAC[0].copy()
					for i in range(n):
						temp = random.choice(D_RAC_temp)
						res[i] = temp
						D_RAC_temp.remove(temp) # évite les doublons
				else:
					i = []
					V = V_RAC.copy()
					D = deepcopy(D_RAC)
					states = mastermind.get_states()
					res = RAC_forward_checking(i,V,D,n,states)

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
					V = V_RAC.copy()
					D = deepcopy(D_RAC)
					states = mastermind.get_states()
					nbre_occurences = [0] * mastermind.get_p()
					res = RAC_forward_checking_doublons(i,V,D,n,states,nbre_occurences)

			#################################################################################################################################################################################################

			elif (joueur == 5): # retour arrière chronologique AVEC forward checking SANS doublon, AMELIORE
				res = {}
				if mastermind.get_nb_tentatives() == 0:
					D_RAC_temp = D_RAC[0].copy()
					for i in range(n):
						temp = random.choice(D_RAC_temp)
						res[i] = temp
						D_RAC_temp.remove(temp) # évite les doublons
					res = {0: '1', 1: '0', 2: '6', 3: '3'}
				else:
					i = []
					V = V_RAC.copy()
					D = deepcopy(D_RAC)
					states = mastermind.get_states()
					#print("states :",states)
					liste_bp = [bp[1] for bp in mastermind.get_states().values()]
					liste_mp = [mp[2] for mp in mastermind.get_states().values()]
					max_bien_placees = max(liste_bp)
					max_mal_placees = max(liste_mp)
					somme_placees = [sp[1]+sp[2] for sp in mastermind.get_states().values()]
					somme_max_placees = max(somme_placees)
					nbre_places = [max_bien_placees,max_mal_placees,somme_max_placees]
					#print("nbre_places :",nbre_places)
					res = RAC_forward_checking_ameliore(i,V,D,n,states,nbre_places)

			#################################################################################################################################################################################################

			elif (joueur == 6): # bonus
				pass

			#################################################################################################################################################################################################

			elif (joueur == 7): # algorithme génétique

				E = [] # ensemble de codes compatibles
				res = {}
				
				if mastermind.get_nb_tentatives() == 0:
					D_algoGen_temp = D_algoGen.copy()
					for i in range(n):
						temp = random.choice(D_algoGen_temp)
						res[i] = temp
						D_algoGen_temp.remove(temp)
					historique = {}

				else:
					# Evaluation ou "fitness" des individus
					# Activation de la génération
					''' Sélection "naturelle"
						les moins bons sont éliminés
						les meilleurs se reproduisent
					'''
					# Fin lorsque "fitness" suffisamment bonne

					# Evaluation de l'historique en fonction du secret
					fitness = (mastermind.get_n()*2) * mastermind.get_states()[mastermind.get_nb_tentatives()][1] + mastermind.get_states()[mastermind.get_nb_tentatives()][2]
					historique[mastermind.get_nb_tentatives()] = fitness
					population = []
					nouvelle_population = []

					start_time = time.time()

					#timeout = 1
					continuer = True
					#for continuer in range(timeout):
					while(continuer):
						for gen in range(maxgen):
							#print("Génération",gen,":")
							if gen > 0:
								parents = []
								#population_temp = population.copy()
								population_temp = deepcopy(population)
								'''
								for i in population:
									if i[1] < 5:
										parents.append(i)
								'''
								for i in range( int(len(population)/2) ):
									temp = min(population_temp, key = lambda t: t[1])
									#print("temp =",temp)
									parents.append(temp)
									population_temp.remove(temp)
								
							
							nouvelle_population[:] = []
							#print("NOUVELLE POPULATION VIDE :",nouvelle_population)
							for p in range(popsize):
								#print("La population grandit, de taille",p+1)
								individu = {}
								if gen == 0:
									D_algoGen_temp = D_algoGen.copy()
									for i in range(n):
										temp = random.choice(D_algoGen_temp)
										individu[i] = temp
										D_algoGen_temp.remove(temp)
								else:
									#parents_temp = parents.copy()
									parents_temp = deepcopy(parents)
									#print("parents_temp :",parents_temp)
									children = []
									if random.random() < 0.5:
										#if random.random() < CXPB:
										if random.random() < CXPB and len(parents_temp) >= 2:
											#print("CROSSOVER FAIT")
											separation = random.randint(1, n-1) # point du crossover
											for i in range(2):
												temp = random.choice(parents_temp)
												#print("temp :",temp)
												temp2 = []
												for k,v in temp[0].items():
													temp2.append(v)
												#print("temp 2 :",temp2)
												if i == 0:
													child = temp2[:separation]
												else:
													child = temp2[separation:]	
												
												#print("child :",child)
												children.append(child)
												parents_temp.remove(temp)
											#print("children :",children)
											fusion = children[0] + children[1]
											for i in range(n):
												individu[i] = fusion[i]
											#print(individu)
										else:
											#print("CROSSOVER NON FAIT")
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]
									else:
										if random.random() < MUTPB:
											#print("MUTATION FAITE")
											child = random.choice(parents_temp)
											alea = random.randint(0,len(child)-1)
											#print("parents :",parents)
											#print("child avant :",child)
											child[0][alea] = random.choice(D_algoGen)
											#print("child après :",child)
											#print("parents :",parents)
											for i in range(n):
												individu[i] = child[0][i]
										else:
											#print("MUTATION NON FAITE")
											individu_random = random.choice(parents_temp)[0]
											for i in range(n):
												individu[i] = individu_random[i]


								#print("individu",p,":",individu)
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
									#print("fitness :",fitness)
									#print("fitnessN :",fitnessN)

								#nouvelle_population.append((individu,fitness))
								nouvelle_population.append((individu,fitnessN))
								#population.append((individu,fitness))

							# Nouvelle population
							population[:] = nouvelle_population
							#print("population :",population)

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
							if strategie_algo_genetique == 1:													
								res,res_individu_fitness = random.choice(E) # random
							elif strategie_algo_genetique == 2:
								res,res_individu_fitness = min(E, key = lambda t: t[1]) # sélectionne la meilleure fitness
							elif strategie_algo_genetique == 3:
								res,res_individu_fitness = max(E, key = lambda t: t[1]) # sélectionne la pire fitness
							elif strategie_algo_genetique == 4:
								# Choix du code présentant le plus de similarité avec les autres codes compatibles.
								similaires = []
								for c in E:
									#print("c :",c)
									E_copy = deepcopy(E)
									#print("E_copy :",E_copy)
									while c in E_copy:
										E_copy.remove(c)
									#print("E_copy :",E_copy)
									temp_similarite = 0
									for c_etoile in E_copy:
										#print("c_etoile :",c_etoile)
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										temp_similarite += mm_temp.get_states()[len(mm_temp.get_states())][1] + mm_temp.get_states()[len(mm_temp.get_states())][2]
										#print(mm_temp.get_states()[len(mm_temp.get_states())][1],mm_temp.get_states()[len(mm_temp.get_states())][2])
									similaires.append(temp_similarite)
								#print(similaires)
								res,res_individu_fitness = E[similaires.index(max(similaires))] # le plus de similarités
							elif strategie_algo_genetique == 5:
								# Choix du code présentant le moins de similarité avec les autres codes compatibles.
								similaires = []
								for c in E:
									#print("c :",c)
									E_copy = deepcopy(E)
									#print("E_copy :",E_copy)
									while c in E_copy:
										E_copy.remove(c)
									#print("E_copy :",E_copy)
									temp_similarite = 0
									for c_etoile in E_copy:
										#print("c_etoile :",c_etoile)
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										temp_similarite += mm_temp.get_states()[len(mm_temp.get_states())][1] + mm_temp.get_states()[len(mm_temp.get_states())][2]
										#print(mm_temp.get_states()[len(mm_temp.get_states())][1],mm_temp.get_states()[len(mm_temp.get_states())][2])
									similaires.append(temp_similarite)
								#print(similaires)
								res,res_individu_fitness = E[similaires.index(min(similaires))] # le moins de similarités

							elif strategie_algo_genetique == 6:
								# Estimation du nombre de codes compatibles restants si un code était tenté
								#longueur_S = 4
								longueur_S = len(E)
								estimations = []
								S = []
								E_copy = deepcopy(E)
								for i in range(longueur_S):
									if len(E_copy) == 0:
										break
									temp = random.choice(E_copy)
									S.append(temp)
									#while temp in E_copy:
										#E_copy.remove(temp)
								#print("S :",S)
								for c in E:
									remain = 0
									#print("c :",c)
									S_copy = deepcopy(S)
									while c in S_copy:
										S_copy.remove(c)
									#print("S_copy :",S_copy)
									for c_etoile in S_copy:
										mm_temp = Mastermind(n)
										code_temp = []
										for i in c_etoile[0].values():
											code_temp.append(i)
										#print("c_etoile :",code_temp)
										mm_temp.create_code_secret(code_temp) #liste
										mm_temp.create_code_tentative(c[0]) #dico
										mm_temp.comparaison()
										S_copy_bis = deepcopy(S_copy)
										while c_etoile in S_copy_bis:
											S_copy_bis.remove(c_etoile)
										#remain = 0
										#print("S_copy_bis :",S_copy_bis)
										for other_code in S_copy_bis:
											#print("other_code :",other_code)
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
											#print(mm_temp.get_states()[len(mm_temp.get_states())][1],mm_temp0.get_states()[len(mm_temp.get_states())][1])
											#print(mm_temp.get_states()[len(mm_temp.get_states())][2],mm_temp0.get_states()[len(mm_temp.get_states())][2])
									#print("remain :",remain)
									estimations.append(remain)
								#print("estimations :",estimations)
								res,res_individu_fitness = E[estimations.index(min(estimations))]
							
							#print("E :",E)
							#print("res :",res)
							#print("res_individu_fitness :",res_individu_fitness)
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
			if joueur != 4:
				mastermind.comparaison()
			else:
				mastermind.comparaison_doublons()

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



for i in range(1000):
	print(i)
	run()


# possibilité d'éviter les doublons dans E