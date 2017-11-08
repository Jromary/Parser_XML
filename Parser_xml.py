# -- coding: utf-8 --


class Item(object):
	"""docstring for Item"""
	def __init__(self, name = None, atribut = {}, types = 'Node'):
		super(Item, self).__init__()
		self.Name = name
		self.Type = types
		if atribut == [] or atribut == None:
			self.Atribut = {}
		else:
			self.Atribut = atribut

	def __repr__(self):
		res = ''
		if self.Name != None:
			'''if self.Type == 'b':
				res += 'Balise Name: '+ str(self.Name)
			else:
				res += 'Text: '+ str(self.Name)'''

			res += str(self.Type) + ': ' + str(self.Name)
		else:
			res += 'No Name referenced'
		if len(self.Atribut) > 0:
			res += ' , Atributs:'
			for cle in self.Atribut:
				res += ' | '+ str(cle) + ' = ' + str(self.Atribut[cle])

		return res


class Tree(object):
	"""docstring for Tree"""
	def __init__(self, val = None, parent = None):
		super(Tree, self).__init__()
		self.Val = val
		self.Child = []
		if parent == None:
			self.Read(val)
		else:
			self.Parent = parent

	def __repr__(self):
		return 'Tree()'

	def __str__(self):
		"""Show All the current tree, with a unfold
		like systeme"""
		return self.__str__aux()

	def __str__aux(self, dist = 0, indent = ''):
		res = ""
		distance = 3+dist
		"""for i in range(len(indent), distance-4):
			indent += ''
		"""
		indents = indent
		res += str(self.Val) + '\n'
		for i in range(len(self.Child)):
			if i == len(self.Child)-1:
				res += indent + '└─'
			else:
				if len(self.Child[i].Child) > 0:
					res += indent + '├┬'
				else:
					res += indent + '├─'
			indents += '│'
			res += self.Child[i].__str__aux(distance, indents)
			indents = indent
		return res

	def havechild(self):
		return len(self.Child) != 0

	def haveparent(self):
		return self.Parent != None

	def Children(self, number = 0):
		if number < len(self.Child):
			return self.Child[number]

	def Ancestor(self):
		return self.Parent

	def Push(self, val = None):
		"""Add a child at the current node"""
		New_Tree = Tree(val, self)
		New_Tree.Parent = self
		self.Child.append(New_Tree)

	def Pop(self):
		"""Remove the current node and all child of it"""
		self.Parent.Child.remove(self)
		while len(self.Child) > 0:
			self.Child[-1].Parent = None
			self.Child.pop()

	def Read(self, name = None):
		if name != None:
			pass
			file = open(name, 'r')
			data = file.read()
			file.close()
			print (data)
			tab = []
			i = 0
			tempo = ''
			while i < len(data):#parcourt toutes les lignes
				if data[i] == '<':#si balise ouvrante
					if len(tempo[1::]) > 0 and tempo[1::] != '\n':
						for j in range(len(tempo[1::])):
							if not(tempo[j+1] == ' ' or tempo[j+1] == '\n'):
								tab.append([str(tempo[1::]),{}, 'Text'])
								break
					tempo = ''
					temp = ''
					j = i+1
					while j < len(data):#on recopi tt jsqu'a la fermante
						temp += data[j]
						j += 1
						if data[j] == '>':
							break
					i = j
					if len(temp) > 4 and temp[0]=='!' and temp[1]=='-' and temp[2]=='-' and temp[-1]=='-' and temp[-2]=='-':
						tab.append([str(temp[3:-2:]),{}, 'Commentaire'])
					else:
						tab.append(temp.split(' ', 1))
				tempo += data[i]
				i += 1

			for i in range(len(tab)):#pour tt les balise trouve
				temp = tab[i][1::]
				if len(temp) == 1:#si elle on des atributs
					temp = str(temp[0])
					dic = {}
					j = 0
					key = ''
					val = ''
					while j < len(temp):#on cherche l'atribut
						if temp[j] != ' ':
							k = j
							while k < len(temp):
								key += temp[k]
								k += 1
								if temp[k] == '=' or temp[k] == ' ':
									break
							end = False
							while k < len(temp) and not(end): #on cherche sa valeur
								if temp[k] == "'":
									m = k+1
									while m < len(temp):
										val += temp[m]
										m += 1
										if temp[m] == "'":
											end = True
											break
									k = m
								elif temp[k] == '"':
									m = k+1
									while m < len(temp):
										val += temp[m]
										m += 1
										if temp[m] == '"':
											end = True
											break
									k = m
								k += 1
							j = k
							dic[key] = val#on a trouver la valeur, on lie atribut+val
						key = ''
						val = ''
						j += 1
					tab[i][1] = dic#on remplace pour avoir une liste d'atribut ss forme de dict
					tab[i].append('Element')
				else:
					tab[i].append({})#sinon on presise qu'il n'y a pas d'attribut
					tab[i].append('Element')

			for i in range(len(tab)):#on remplie l'arbre avec les balise
				if tab[i][2] == 'Text' or tab[i][2] == 'Commentaire':
					self.Push(Item(tab[i][0], tab[i][1], tab[i][2]))
				elif tab[i][0][0] == '/':#si balise fermante on remonte dans l'arbre
					self = self.Ancestor()
					self.Push(Item(tab[i][0], tab[i][1], tab[i][2]))
				elif tab[i][0][0] != '?' and tab[i][0][-1] != '/':#si ouvrante on decend
					self.Push(Item(tab[i][0], tab[i][1], tab[i][2]))
					self = self.Children(-1)
				else:#sinon on reste a la profondeur courante
					self.Push(Item(tab[i][0], tab[i][1], tab[i][2]))
		else:
			return




def main():
	pipop = Tree('Test.xml')
	print()
	print (pipop)


if __name__ == '__main__':
	main()
