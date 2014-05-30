import  utility as utl
import sys


def debug(str):
	#print str
	pass

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

	def add_prim_mem(self,key=None, value=None):
		if key:
			self.prim_mem.append({key:value})
		else:
			self.prim_mem.append(value)

	def add_obj_mem(self,key = None, value=None):
		
		debug("---")
		debug(key)
		debug(value)
		if key:
			#value.set_key(key)
			self.obj_mem.append( {key:value} )
		else:
			self.obj_mem.append(obj)

	def add_array_mem(self,key=None, value=[]):
		self.set_type("ARRAY")
		if key:
			self.array_mem.append(value)
		else:
			self.array_mem.append(value)

	def set_label (self,label):
		self.label = label
	
	def get_prim_mem(self):
		return self.prim_mem

	
	def _print_array(self, arr):
		json = ""

		#if arr.key:
		#	json =  json + "\"" + arr.key + "\"" + " : "

		if arr.type == "ARRAY":
			json = json + " [ "
		commaFlg = False

		# print primitive members first.
		for a in arr.prim_mem:
			if commaFlg :
				json = json + " , "
			if type(a) is str:
				json = json + "\"" +  str(a) + "\""
			elif type(a) is int or type(a) is float:
				json = json + str(a)
			else:
				#print a, type(a)
				json = json + "\"" + str(a) + "\""
			commaFlg = True

		'''# print object members
		for o  in arr.obj_mem:			
			if commaFlg:
				json = json + " , "
			json = json + self._print_obj(o)

			commaFlg = True
		'''
		# print array members
		
		for a in arr.array_mem:
			#print a
			if commaFlg:
				json = json + " , "
			if a.type == "ARRAY":
				json = json + self._print_array(a)
			elif a.type == "OBJECT":
				json = json + self._print_obj(a)
			else:
				pass
			commaFlg = True
		

		if arr.type == "ARRAY":
			json = json + "]"
		

		return json
	

	def _print_obj(self,obj):
		json = ""
		commaFlg=False
		#if  obj.key :
		#	json =  "\"" + obj.key + "\"" + " : "
			

		json = json + " { "

		# get primitive member first.

		for kv in obj.prim_mem:
			for (k,v) in kv.items():
				if commaFlg: 
					json = json + " , "  				
				json = json + "\""+str(k) + "\"" + " : " + "\"" + str(v) + "\""
				commaFlg = True

		# get obj member...
		for o in obj.obj_mem:
			for (k,v) in o.items():
				if commaFlg :
					json = json + " , "
				if v.type == "OBJECT": #!!!!!
					#json = json +  self._print_obj(o)
					json = "{} \"{}\":{}".format(json,k,self._print_obj(v))
				elif v.type == "ARRAY":
					#json = json + self._print_array(o)
					json = "{} \"{}\" : {}".format(json,k,self._print_array(v))
				else:
					pass
			commaFlg = True
			#json = json + " , " ## some fix

		# get array member
		'''
		for a in obj.array_mem:
			if commaFlg :
				json = json + " , "
			json = json + self._print_array(a)

			commaFlg = True
		'''

		json = json + " } "

		return json

	def print_json (self):
		if self.type == "OBJECT":
			return self._print_obj(self)
		elif self.type == "ARRAY":
			return self._print_array(self)
		else:
			return {"error":"Neting obj nor Array"}

	def pretty_print(self):
		return 	utl.pretty_print( self.print_json())
			
'''
	this class represent the whole object tree of the json data
'''
class PyObjTree:

	def __init__(self, jsonObj):
		self.root = self.buildTree(jsonObj)
		#return self.root
	def get_root(self):
		return self.root
	
	def buildTree(self,jsonObj):

		#py_obj = PyJSOb(type="OBJECT")
		#print jsonObj
		if type(jsonObj) is dict:
			py_obj = PyJSOb(type="OBJECT")

			for (k,v) in jsonObj.items():
				#print k, v
				if type(v) is dict:
					py_obj.add_obj_mem( key=k, value = self.buildTree(v) )

				elif type(v) is list:
					py_obj.add_obj_mem(key=k, value = self.buildTree(v))

				elif type(v) is str or type(v) is int or type(v) is float:
					#print v
					py_obj.add_prim_mem(key=k, value = v)
				else:					
					py_obj.add_prim_mem(key=k, value = v)
					#print type(v)
					pass
			return py_obj
		
		elif type (jsonObj) is list:
			py_obj = PyJSOb(type="ARRAY")
			for arr in jsonObj:
				if type(arr) is list:
					py_obj.add_array_mem( value=self.buildTree(arr))
				elif type(arr) is dict:
					py_obj.add_array_mem(value=self.buildTree(arr))

				elif type(arr) is str or type(arr) is int or type(arr) is float:
					py_obj.add_prim_mem(value = arr)
				else:
					py_obj.add_prim_mem(value = arr)
			return py_obj
		else:
			pass

def test():
	if len(sys.argv) < 2:
		print "give all arguments"
		exit()
	job = utl.LoadJSON(path=sys.argv[1]).get_json()
	tree = PyObjTree(job)
	pyjsob = PyJSOb()
	to = tree.root
	to.get_prim_mem()
	print to.print_json()

	print to.pretty_print()

if __name__ == "__main__":
	test()
