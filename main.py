class NormalSet():
	"""

	本プログラムで扱う集合を表現するクラス
	"""
	def __init__(self, *args) -> None:
		self._mutable_set :set = set()
		self._frozen_set :set = set()
		self._frozen :bool = False
		for obj in args:
			if (isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, frozenset)):
				for i in obj:
					self.add_element(i)
			else:
				self.add_element(obj)

	def __eq__(self, other):
		if not isinstance(other, NormalSet):
			return NotImplemented
		return (self._mutable_set) == (other.mutable_set)

	def __le__(self, other):
		if not isinstance(other, NormalSet):
			return NotImplemented
		return (self._mutable_set) <= other.mutable_set

	def __contains__(self, item):
		return item in self._mutable_set

	def __iter__(self):
		for x in self._mutable_set:
			yield x

	def __hash__(self):
		# ハッシュするタイミングで凍らせてしまう。
		self.create_frozen_set()
		return hash(self._frozen_set)

	def __and__(self, other):
		return NormalSet(self.mutable_set.__and__(other.mutable_set))

	def __or__(self, other):
		return NormalSet(self.mutable_set.__or__(other.mutable_set))

	def __sub__(self, other):
		return NormalSet(self.mutable_set.__sub__(other.mutable_set))

	def __xor__(self, other):
		return NormalSet(self.mutable_set.__xor__(other.mutable_set))

	def add_element(self, element) -> None:
		if (self._frozen == True):
			print("This set is frozen.")
		else:
			self._mutable_set.add(element)
	
	def create_frozen_set(self) -> None:
		if (self._frozen == False):
			self._frozen_set = frozenset(self._mutable_set)
			self._frozen = True
		else:
			pass

	def remove_element(self, element) -> None:
		if (self._frozen == True):
			pass
		else:
			self._mutable_set.discard(element)

	@property
	def mutable_set(self) -> set:
		return self._mutable_set

	@property
	def frozen_set(self) -> set:
		if (self._frozen == False):
			print("This set is not frozen.")
		else:
			return self._frozen_set
	
	@property
	def frozen(self) -> bool:
		return self._frozen

class OrderedPair(NormalSet):
	"""

	順序対を表現するクラス。
	"""
	def __init__(self, first_x, second_y) -> None:
		super().__init__()
		self._first_x :object = first_x
		self._second_y :object = second_y
		self._mutable_set :set = { frozenset([self._first_x]), frozenset([self._first_x, self._second_y]) }
		self.create_frozen_set()
		self._ordered_pair :frozenset = self.frozen_set

	@property
	def first_x(self):
		return self._first_x
	
	@property
	def second_y(self):
		return self._second_y

	@property
	def ordered_pair(self):
		return self._ordered_pair

	def show(self):
		print(f"<{self._first_x}, {self._second_y}>", end=" ")

class SetOfOrderedPairOrPairs(NormalSet):
	"""
	
	順序対の集合を表現するクラス。
	"""
	def __init__(self, *args):
		super().__init__()
		for obj in args:
			if isinstance(obj, OrderedPair):
				self.add_element(obj)
			elif (isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set) or isinstance(obj, frozenset)):
				for i in obj:
					self.add_element(i)
			else:
				print(f"This object {obj} is not OrderedPair")

	def add_element(self, obj) -> None:
		if (self._frozen == True):
			print("This set is frozen.")
		elif isinstance(obj, OrderedPair):
			self._mutable_set.add(obj)
		elif (isinstance(obj, list) or isinstance(obj, tuple)):
			for i in obj:
				self.add_element(i)

	def show(self):
		print("{", end="")
		length = len(self._mutable_set)
		c = 0
		for ordered_pair in self._mutable_set:
			ordered_pair.show()
			if (c < length-1):
				print(", ", end="")
			c += 1
		print("}", end="")

def calculate_direct_product(normal_set_A, normal_set_B):
	return  SetOfOrderedPairOrPairs([ OrderedPair(i, j) for i in normal_set_A for j in normal_set_B ])

def calculate_intersection(normal_set_A, normal_set_B):
	return NormalSet(normal_set_A.mutable_set & normal_set_B.mutable_set)

def is_reflective(normal_set_A, relation_R):
	if (relation_R <= calculate_direct_product(normal_set_A, normal_set_A)):
		if all([(OrderedPair(element, element) in relation_R) for element in normal_set_A]):
			return True
		else:
			return False
	else:
		return False

def is_symmetric(normal_set_A, relation_R):
	if (relation_R <= calculate_direct_product(normal_set_A, normal_set_A)):
		if all([(OrderedPair(ordered_pair.second_y, ordered_pair.first_x) in relation_R) for ordered_pair in relation_R ]):
			return True
		else:
			return False
	else:
		return False

def is_transitive(normal_set_A, relation_R):
	if (relation_R <= calculate_direct_product(normal_set_A, normal_set_A)):
		if all([(OrderedPair(ordered_pair1.first_x, ordered_pair2.second_y) in relation_R if (ordered_pair1.second_y == ordered_pair2.first_x) else True) for ordered_pair1 in relation_R for ordered_pair2 in relation_R]):
			return True
		else:
			return False
	else:
		return False

def is_poset(normal_set_A, relation_R):
	if (is_reflective(normal_set_A, relation_R) and is_transitive(normal_set_A, relation_R)):
		print("True")
		return True
	else:
		return False

def main():
	A = NormalSet(1,2,3)
	R =  SetOfOrderedPairOrPairs(OrderedPair(1,1), OrderedPair(1,2), OrderedPair(2,2), OrderedPair(3,3))
	is_poset(A, R)

if __name__ == "__main__": # 直接実行の場合
	from main import main
	main()

