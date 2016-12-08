JSONAC
======
Access control for data represented in JSON format.

Summary:

In this project, I assume there is a JSON data file (eg. employee records including addr, phone no, SSN and so on) which contains some sensitive information and  might be stored somewhere (I do not actually consider where it is stored). The data owner wants to project sharing of the data from the JSON file. So, he comes up with a policy file (also represented in JSON) which states who can access which part of the file. This project is all about this enforcement.

The policy file:
The policy file has two parts: (1) in the first part, it specify labels for  JSONPaths. (2) in the second part, it  says which users (represented by roles) can access contents assigned to which labels. 

How it works:
The starting script (ObQuery.py) loads the JSON file and corresponding policy file into memory. Based on the labeling policy (specified in the policy) it assigns labes on every JSON paths of the file. The labels are actually juxtaposed into the content of the file. 

When there is an access request, the program checks which JSONpath the requester is accessing. It also consult the role of the user. Finally, if the specified role of the user can access the requested JSONPath (which is specified in the policy file) the request is granted.

How to run the script:
<script-name> <JSONfile> <requested_JSONPath> <Role_of_the_user>
Eg. 
python ObQuery.py employee.json /personalRecord public



Args:
	employee.json : json data file
	/personalRecord: a path in the JSON file
	public: Clearance label of the Requester

