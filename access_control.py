

class TreeNode:
	def __init__(self,name):
		self.children = []
		self.value = name
	
	def add_child(self, tn):
		self.children.append(tn)


class NodeHierarchy:
	def __init__(self):
		self.root_list = []
		self.nodes=[]
	def insert(self,x_v,y_v): # insert a hierarchy of two node such that x dominates y. x_v, y_v are values of x & y
		if self._find_node(x_v) == None:
			self._add_2_nodes(x_v)
		if self._find_node(y_v) == None:
			self._add_2_nodes(y_v)

		x = self._find_node(x_v)
		y = self._find_node(y_v)
		x.add_child(y)

		pass

	def check(self,x_v,y_v): # check there x dominates y
		
		x = self._find_node(x_v)
		y = self._find_node(y_v)
		status = False

		if x_v == y_v:
			return True

		for n in x.children:
			status= self.check(n.value,y_v)
			if status ==  True:
				return status
		return False

	def _add_2_nodes(self,x_v):
		tn = TreeNode(x_v)
		self.nodes.append(tn)
		
	
	def _find_node(self,x_v):
		
		for n in self.nodes:
			if n.value == x_v:
				return n
		return None

	
		
def test():
	nh = NodeHierarchy()
	#nh._add_2_nodes("public")
	#nh._add_2_nodes("private")
	#print nh._find_node("public")
	nh.insert("private","public")
	nh.insert("protected","private")
	print nh.check("protected","public")

if __name__ == "__main__":
	test()
