import sys
from  lexical_analyzer import LexicalAnalyzer
import simplejson as json


jsonpath="/personalRecord/identification[1]/eid"

class LoadJSON:
	def __init__(self,path):
		self.data = json.load(self.read_file(path))


	def read_file(self,filename):
		return  open(filename,'r')

	def get_json(self):
		return self.data



class Filter:
	def __init__(self):
		pass
	def keep(label, job):
		#keep object with given label only. all the other objects are deleted.
		# if job is dict

		if type (job) is dict:
			#check all descendant ob
			pass
		elif type(job) is list:
			pass


class Policy:

	def __init__(self):
		pass

	def enforce(self,req_label, cur_label):
		# assume no label hierarchy. Security policy need to be inforced here.
		if req_label != cur_label:
			return False
		return True

	def keep_label(self,node,label,white_nodes):
		# node is a dictionary, label is the access label, white_nodes are the nodes that have been cleared for access.
		#on every run of these function, we traverse child dict, and find which nodes can be shown (in white_nodes). then from the current node, delete all teh object and insert only the white_objects.
		if type(node) is not  dict:
			return white_nodes
		elif type(node) is dict:
			for key, value in node.iteritems():
				if type(value) is dict:
					white_nodes = self.keep_label(value, label, white_nodes)

		
		if "label" in node and node["label"] == label:
			#remove objects that are not in whitelist
			delete_obj=[]
			for key, value in node.iteritems():
				if type(value) is dict:
					#del(node[key])
					delete_obj.append(key)
			for item in delete_obj:
				del(node[item])
			i=0
			#print "after deleting ob"
			#print node
			#print "white_node"
			#print white_nodes
				# needs more work here.
			if white_nodes:
				for item in white_nodes:
					node["new"+str(i)] = item
					i = i + 1
				#print "adding white node with node"
				#print node
				return [node]
			else:
				white_nodes.append(node)
				return white_nodes
		else:
			return white_nodes


class Query:
	def __init__(self,json,t):
		self.json = json
		self.token_pair = t
		self.cur = []	# all the json obs are in cur before running query
		self.cur.append(json)
		self.jobaq = [] # holds json objects after running a query
		#print json
		#print t

	def execute(self):
		
		#print "--"
		#print self.cur
		
		for tp in self.token_pair:
			(t1,t2) = tp
			#print t1, t2
			if t1 == "child":
				for j_ob in self.cur: # for j_ob in the current jsobob list in cur...
					#print j_ob
					n_ob = j_ob.get(t2)
					# need to check the policy here.
					if Policy().enforce("public","public") == True:
						self.jobaq.append(n_ob)
			elif t1 == "index":
				for j_ob in self.cur:
					n_ob = j_ob[int(t2)]
					if Policy().enforce("public","public") == True:
						self.jobaq.append(n_ob)

						
			self.cur = self.jobaq
			self.jobaq = []
		return self.cur





def test():
	jsonpath = sys.argv[1]
	print "jsonpath:" + jsonpath
	lj = LoadJSON("employee.json")
	j =  lj.get_json()
	#print x["personalRecord"]["name"]
	la = LexicalAnalyzer(jsonpath)
	token_p = la.token_pair()
	q = Query(j,token_p)
	#print q.execute()[0]

	print Policy().keep_label(q.execute()[0],"public",[])

	#print x.get("name")
	#print lj.data

test()
