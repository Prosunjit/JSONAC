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
		#print node
		#child_white_nodes=[]
		(k, v) = node.items()[0]
		for (key, value) in v.items():
			if type(value) is dict:
				tmp = self.keep_label({key:value}, label, [])
				if tmp:
					for el in tmp:
						white_nodes.append(el)
		
 		if "label" in v and v["label"] == label:
			#remove objects that are not in whitelist
			delete_obj=[]
			for key, value in v.iteritems():
				if type(value) is dict:
					delete_obj.append(key)
			for item in delete_obj:
				del(v[item])
			# delete the label node from output
			del(v['label'])
			# needs more work here.
			if white_nodes:
				for wn in white_nodes:
					if wn:
						(_k,_item) =  wn.items()[0]
						v[_k] = _item
				return [{k:v}]
			else:
				return [{k:v}]
		else:
			return white_nodes;


class Query:
	def __init__(self,json,t):
		self.json = json
		self.token_pair = t
		self.cur = {}	# all the json obs are in cur before running query
		#self.cur.append(json)
		self.cur = json
		self.jobaq = {} # holds json objects after running a query
		#print json
		#print t

	def execute(self):
		
		#print "--"
		#print self.cur
		token_pair = self.token_pair
		cur = self.cur
		jobaq = self.jobaq
		
		for tp in token_pair:
			(t1,t2) = tp
			#print t1, t2
			if t1 == "child":
				for (key, j_ob) in cur.items(): # for j_ob in the current jsobob list in cur...
					#print j_ob
					#n_ob = j_ob.get(t2)
					#print "!!"
					#print j_ob
					#print t2
					n_ob = j_ob[t2]
					# need to check the policy here.
					if Policy().enforce("public","public") == True:
						#self.jobaq.append(n_ob)
						jobaq[t2] = n_ob
			elif t1 == "index":
				for (key, j_ob) in cur.item():
					n_ob = j_ob[int(t2)]
					if Policy().enforce("public","public") == True:
						#self.jobaq.append(n_ob)
						jobaq[t2] = n_ob

						
			cur = jobaq
			jobaq = {}
		return cur





def test():
	jsonpath = sys.argv[1]
	label = sys.argv[2] 
	print "jsonpath:" + jsonpath
	lj = LoadJSON("employee.json")
	j =  lj.get_json()
	#print j
	#print x["personalRecord"]["name"]
	la = LexicalAnalyzer(jsonpath)
	token_p = la.token_pair()
	q = Query({"data":j},token_p)
	print json.dumps( q.execute(), indent=4, sort_keys=True)

	print Policy().keep_label(q.execute(),label,[])

	#print x.get("name")
	#print lj.data

test()
