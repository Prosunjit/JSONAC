from lexical_analyzer import LexicalAnalyzer
from PythonJsonObj import PyObjTree, PyJSOb
import utility as utl
import sys
import policy as Policy

class ObQuery:
	def __init__(self, root_ob):
		self.tree_root = root_ob
		 

	def _gapvalue(self,gap_key, obj):
		r = []

		'''only object type has primitve member of {k:v} format. In Array object, primitive members are only string, or number. 
		so, need not to check prim_mem of array object '''

		if obj.type == "OBJECT":
			for o in obj.prim_mem:
				(k,v) =  o.items()[0]
				if k == gap_key:
					r.append(v)
		for o in obj.obj_mem:
			for (k,v) in o.items():
				if k == gap_key:
					r.append(v)
				else:
					r = r + self._gapvalue(gap_key,v)

		for o in obj.array_mem:
			if isinstance(o,PyJSOb):
				r = r + self._gapvalue(gap_key,o)
		return r
		pass	 
	def query(self,path):

		path_token = LexicalAnalyzer(path).token_pair()
		ini_nodes = [self.tree_root]
		final_nodes=[]		
		token_pair = path_token
		 
		for tp in token_pair:

			(t1,t2) = tp
			final_nodes = []
			 
			if t1 == "child":
				for root in ini_nodes:
					# looking into the object
					for n in root.obj_mem:
						for (k,v) in n.items():
							if k == t2:
								final_nodes.append(v)
					for n in root.prim_mem:
						(k,v) = n.items()[0]
						if k == t2:
							final_nodes.append(v)
				pass
				 
			elif t1 == "index":
				for root in ini_nodes:
					t2 = int(t2)
					try:
						n = root.array_mem[t2]
					except:
						pass
				final_nodes.append(n)
				pass
				 
			elif t1 == "gap":
				for root in ini_nodes:
					final_nodes = final_nodes + self._gapvalue(t2,root)
				pass
			ini_nodes = final_nodes
		return final_nodes


	def _authorized_only(self, job, label_hierarchy, user_clearance):
		# check descendant nodes for clearance
		array_mem = []
		obj_mem = []
		prim_mem = []
		if job.type == "OBJECT":
			# check for obj_members
			for ob in job.obj_mem:
				(key,value) = ob.items()[0]
				value = self._authorized_only(value,label_hierarchy, user_clearance)

			pass
		elif job.type == "ARRAY":
			pass
		else:
			pass

		
		


	# this method do query without ac, then apply access control on the result
	# not considering clearance lattice.

	def ac_query(self, path, label_hierarchy, user_clearance):
		q_res = self.query(path)

		for ob in q_res:
			pass
		pass

def test():
	
	#run with this command :  python ObQuery.py employee.json /personalRecord

	#build the Json Obj tree here
	obj_tree = PyObjTree(utl.LoadJSON(path=sys.argv[1]).get_json()).get_root()
	print id(obj_tree)
	#apply labels to obj tree

	Policy.NodeLabeling(obj_tree,label_file="path_label_policy.json").appy_labels()
	print id(obj_tree)
	#querying against give path
	path = sys.argv[2]

	oq = ObQuery(obj_tree)
	
	res = oq.query(path)
	# we need to iterate through the res. there can be more than one result.
	for r in res:
		if isinstance(r,PyJSOb):
			print r.print_json()
			print utl.pretty_print ( r.print_json() )
		else:
			print r


if __name__ == "__main__":
	test()
