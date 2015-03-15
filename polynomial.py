class Polynomial:
	def __init__(self):
		self.components = {}

	def addMonomial(self, m):
		if self.components.get(m.exponent, False):
			self.components[m.exponent] += m.factor
		else:
			self.components[m.exponent] = m.factor

	def setStrategy(self):
		if (self.getDegree() == 1):
			self.strategy = FirstOrderSolveStrategy()
		else:
			self.strategy = StupidSolveStrategy()


	def build(self, dictionary):
		self.components = dictionary
		self.setStrategy()

	def prettyPrint(self):
		result = ""
		for key, value in self.components.items():
			if value == 1:
				if key == 0:
					result += str(value) + '+'
				else:
					result += self.printExponent(key) + '+'
			elif value:
				result += str(value) + self.printExponent(key) + '+'
		
		return result

	def printExponent(self, key):
		if key == 0:
			return ''
		elif key == 1:
			return 'x'
		else:
			return 'x^' + str(key)

	def getDegree(self):
		l = sorted(self.components.keys(), reverse=True)
		return l[0]

	def solve(self):
		return self.strategy.solve(self)

	def add(self, p):
		result = Polynomial()
		components = {}

		for key, value in self.components.items():
			if key in p.components.keys():
				components[key] = value + p.components[key]
			else:
				components[key] = value

		for key2, value2 in p.components.items():
			if not key2 in self.components.keys():
				components[key2] = value2

		result.build(components)
		return result


class Monomial(Polynomial):
	def __init__(self):
		self.components = {}

	def build(self, dictionary):
		if len(dictionary) != 1:
			raise Exception("This is not a monomial, sry :(")

		self.exponent, self.factor = dictionary.popitem()
		self.components[self.exponent] = self.factor


class SolveStrategy:
	def solve(self, p):
		pass


class FirstOrderSolveStrategy(SolveStrategy):
	def solve(self, p):
		a = p.components[1]
		b = p.components.get(0, 0)
		return -b/a


class StupidSolveStrategy(SolveStrategy):
	def solve(self, p):
		return "I'm too stupid to solve higher order polynomials :("
