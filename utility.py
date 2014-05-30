try:
	import simplejson as json
except ImportError:
	import json

class LoadJSON:
        def __init__(self,path=None, str=None):
		if path:
			#print self.read_file(path)
               		self.data = json.load(self.read_file(path))
		elif str:
			#print str
			self.data = json.loads( str )
		else:
			self.data = json.load( "{ }")


        def read_file(self,filename):
                return  open(filename,'r')

        def get_json(self):
                return self.data



''' given a json string... do pretty printing'''
def pretty_print(str):
	str =  str.encode("utf-8")
	str = str.replace(": u", ": ").replace("'", '"')
	print "--->"
	print str
	print "<---"
	lj = LoadJSON(str = str)
	return  json.dumps( lj.get_json(),indent=4, sort_keys=True )
	#print "...."

'''
	given a list [10,20] return an dict {'0':10, '1':20}

'''

def list2Dict(list):
	r = {}
	for l in range(len(list)):
		r[str(l)] = list[l]
	return r

def remove_key_from_dict_array(dict_array):
	r = []
	for d in dict_array:
		for (k,v) in d.items():
			r.append(v)

	return r

def test():
	print list2Dict([10,20])
	print remove_key_from_dict_array([{'a':10},{'b':"AC"}])

if __name__ == '__main__':
	test()