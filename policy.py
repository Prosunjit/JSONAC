import utility as utl
import PythonJsonObj as PyObjTree
import ObQuery as Query
import constant as constant


class Enforcement:
	def __init__():
		pass

class NodeLabeling:
	def __init__(self,obj_tree , label_file = file):
		self.obj_tree = obj_tree
		self.label_file = label_file		
		self.query_ob = Query.ObQuery(self.obj_tree)

	def appy_labels(self):
		self._labelling()

		return self.obj_tree

	# labels object tree for each (path, label)
	def _labelling(self):
		lbls = self._labels()
		for l in lbls:
			(path, label) = l
			self._ob_tree_labelling(path,label)
		pass
	
	#read (path, label) from input file, and returns [(path,label),..]
	def _labels(self):
		j = utl.LoadJSON(path=self.label_file)
		js = j.get_json()
		r = []
		for ob in js:
			if  ob['target'] != "NODE":
				r.append((ob['target'],ob['label']))
		return r

	def _ob_tree_labelling(self, path, label):
		# here path can be absolute or relative path
		res = self.query_ob.query(path)

		for r in res:
			#print "labeling----------------"
			#print r
			if isinstance(r,PyObjTree.PyJSOb):
				# r.path is eqv to path, because path matched r and r.abs_path is absolute 
				#print "labeling object with id{}---------".format(id(r))
				#self._labeling_on_condition(r,label,r.abs_path) 
				self.recursive_labeling(r,label, r.abs_path)
				pass
		
		pass

	def _labeling_on_condition(self, job, object_label, object_path):
		#print job
		if job.label == constant.DEFAULT_LABEL:
			job.set_label(object_label)
			job.set_label_path(object_path)
		elif utl.json_subpath(object_path, job.label_path):
			job.set_label(object_label)
			job.set_label_path(object_path)
			#print "############"

			#utl.pretty_print (job.print_json())
			pass
		else:
			pass
	def recursive_labeling(self,job, label, path):
		#job.set_label(label)

		#print "labeling object with id {} with label {} with path{}---------".format(id(job),label,path)
		self._labeling_on_condition(job,label,path)
		if job.type == "OBJECT":
			# all members in obj_mem is either ob, or array
			for ob in job.obj_mem:
				(k,v) = ob.items()[0]
				self.recursive_labeling(v,label,path)

		elif job.type == "ARRAY":
			for ob in job.array_mem:
				self.recursive_labeling(ob,label,path)

		else:
			pass

	

def test():
	print NodeLabeling(None,label_file="path_label_policy.json")._labels()
	pass

if __name__ == "__main__":
	test()
