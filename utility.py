'''
	given a list [10,20] return an dict {'0':10, '1':20}

'''
def list2Dict(list):
	r = {}
	for l in range(len(list)):
		r[str(l)] = list[l]
	return r


def test():
	print list2Dict([10,20])

if __name__ == '__main__':
	test()
