import  utility as utl
import sys


class PyJSOb:

	def __init__(self,tag=None,path=None, type="OBJECT"):
		self.key = tag
		self.path = path
		self.label = None
		self.children = []
		self.prim_mem = []
		self.obj_mem = []
		self.array_mem = []
		self.type = type

	def set_type(self, type="OBJECT"):
		self.type = type

	def set_path(self,path):
		self.path = path

	def set_key (self,tag):
		self.key = tag

	def add_child (self,child):
		self.children.append(child)

	def add_prim_mem(self,key, value):
		self.prim_mem.append({key:value})

	def add_obj_mem(self,key = None, obj=None):
		if key:
			obj.set_key(key)
			self.obj_mem.append( obj )
		#else:
		#	self.obj_mem.append(obj)

	def add_array_mem(self,key=None, arr=[]):
		self.set_type("ARRAY")
		if key:
			self.array_mem.append(arr)
		#else:
		#	self.array_mem.append(arr)

	def set_label (self,label):
		self.label = label
	
	def get_prim_mem(self):
		return self.prim_mem
	def print_obj_mem(self):
		commaFlg = False
		json = " { "
		for o in self.obj_mem:
			if commaFlg:
				json = json + " , "
			json = json + self._print_obj(o)
			commaFlg = True
		json = json + " } "
		return json
	

	def _print_obj(self,obj):
		json = ""
		commaFlg=False
		if  obj.key :
			json =  "\"" + obj.key + "\"" + " : "
			

		json = json + " { "

		for kv in obj.prim_mem:
			for (k,v) in kv.items():
				if commaFlg: 
					json = json + " , "  				
				json = json + "\""+str(k) + "\"" + " : " + "\"" + str(v) + "\""
				commaFlg = True


		for o in obj.obj_mem:
			if commaFlg :
				json = json + " , "
			json = json +  self._print_obj(o)
			commaFlg = True
			#json = json + " , " ## some fix

		json = json + " } "

		return json

	def pretty_print(self):
		if self.type == "OBJECT":
			utl.pretty_print( self.print_obj_mem())
				
'''
	this class represent the whole object tree of the json data
'''
class PyObjTree:

	def __init__(self, jsonObj):
		self.root = self.buildTree(jsonObj)
	
	def buildTree(self,jsonObj):

		#py_obj = PyJSOb(type="OBJECT")
		#print jsonObj
		if type(jsonObj) is dict:
			py_obj = PyJSOb(type="OBJECT")

			for (k,v) in jsonObj.items():
				#print k, v
				if type(v) is dict:
					py_obj.add_obj_mem( k, self.buildTree(v) )

				elif type(v) is list:
					py_obj.add_obj_mem(k, self.buildTree(v))

				elif type(v) is str or type(v) is int or type(v) is float:
					#print v
					py_obj.add_prim_mem(k, v)
				else:					
					py_obj.add_prim_mem(k, v)
					#print type(v)
					pass
			return py_obj
		
		elif type (jsonObj) is list:
			py_obj = PyJSOb(type="ARRAY")
			#print py_obj
			for arr in jsonObj:
				if type(arr) is list:
					py_obj.add_array_mem( self.buildTree(arr))
				elif type(arr) is dict:
					py_obj.add_array_mem(self.buildTree(arr))

				elif type(arr) is str or type(arr) is int or type(arr) is float:
					py_obj.add_array_mem(arr)
				else:
					py_obj.add_array_mem(arr)
			return py_obj
		else:
			pass

def test():
	#if len(sys.argv) < 2:
	#	print "give all arguments"
	#	exit()
	job = utl.LoadJSON(path="employee.json").get_json()
	tree = PyObjTree(job)
	pyjsob = PyJSOb()
	to = tree.root
	to.get_prim_mem()
	to.pretty_print()

if __name__ == "__main__":
	test()
