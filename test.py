import ystockquote as stock
import inspect as inspect 

"""Welcome to the test suite"""

def lu(obj,spacing=5, collapse=1):
	"""Lists the functions and documentation"""
	methods_list=[method for method in dir(obj) if inspect.isfunction(getattr(obj, method))]
	process_method=collapse and (lambda s: " ".join(s.split())) or (lambda s:s)
	print "\n".join(["%s \n %s \n\t%s\n" % ((method.ljust(spacing)),"("+str(input(getattr(obj,method)))+")", process_method(str(getattr(obj, method).__doc__))) for method in methods_list])
	a=raw_input("Y or N (case sensitive): Keep Looking?")
	if a=="Y":
		print [method for method in dir(obj) if callable(getattr(obj,method))],[process_method(str(getattr(obj,method).__doc__)) for method in dir(obj) if callable(getattr(obj,method))]

def modules():
	"""Lists all available modules"""
	help("modules")

def input(func):
	"""Returns with required arguments of a function"""
	a= str(str(inspect.getargspec(func)).split("]")[0]).split("[")[1]
	return a
"""This sections is just notes:
getabsfile(),isfunction(), isclass(),isbuiltin(), ismodule(),ismethod()
"""

if __name__=="__main__":
	a=raw_input("Name a module: ")
	help(a)
