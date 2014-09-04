import ystockquote as stock
import inspect as inspect 

"""Welcome to the test suite"""

def poke(obj,spacing=5, ls=1):
	#**DEV** >>>a=isfunction()

	"""Lists the functions and documentation"""
	methods_list=[method for method in dir(obj) if inspect.isfunction(getattr(obj, method))]
	process_method=ls(collapse,(lambda s: " ".join(s.split())),(lambda s:s))
	print "\n".join(["%s \n %s \n\t%s\n" % ((method.ljust(spacing)),"("+str(input(getattr(obj,method)))+")", process_method(str(getattr(obj, method).__doc__))) for method in methods_list])
	a=raw_input("Y or N (case sensitive): Keep Looking?")
	if a=="Y":
		print [method for method in dir(obj) if callable(getattr(obj,method))],[process_method(str(getattr(obj,method).__doc__)) for method in dir(obj) if callable(getattr(obj,method))]

def ls(boolean, option1, option2):
	"""Change boolean to an option that may have a value. If boolean exists at any value besides: None, False, "" (empty string),0,(maybe more empty kinds of 'variables') then it returns 'True'. This means most objects, dictionaries, etc: will act as True and advancing the current 'option' as it's 'return value'. Basically, the option returned is the last non-false option provided. The exception being that if all values are False, "", etc., then the last option is the return value (i.e. (None or False) would return False, rather than None when a str() function is applied to the result, where None advanced the interactive terminal as if the user hit enter. However, if this is an actual instance of something (due to modifying __value to return False, None,etc.)"""
	return boolean and option1 or option2

def modules():
	"""Lists all available modules"""
	help("modules")

def input(func):
	"""Returns with required arguments of a function"""
	a= str(str(inspect.getargspec(func)).split("]")[0]).split("[")[1]
	return a
"""This sections is just notes:
inspect: getabsfile(),isfunction(), isclass(),isbuiltin(), ismodule(),ismethod(), 
pydoc: isdata(),ispath(),locate()
"""

if __name__=="__main__":
	a=raw_input("Name a module: ")
	help(a)
