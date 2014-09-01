import ystockquote as stock
import inspect as inspect 
import types as types

"""Welcome to the test suite"""


"""This is for inspections"""

def poke(obj):
	
	expr={[t for t in dir(types) if callable(getattr(obj, t))]:1}
	for t in expr.keys():
		if t==type(obj):
			print t

	#expr={'module':poke_module,'class':poke_class,'instancemethod':2,'str':3,'int':4,'dict':5,'function':6,frame:7,traceback:8]		
	try: 
		print t
		# need to rewrite expr[str(type(obj)).split("'")[1]](obj)
		#need to handle errors better
	except:
		print "type not yet defined"
		expr['class'](obj)


	"""Lists the functions and documentation"""
def poke_class(obj):
	method=[method for method in dir(obj) if callable(getattr(obj,method))]
		#FILTER for __""__ named methods vs. user defined.
	process_method=ls((lambda s: " ".join(s.split(),(lambda s:s))))
	print "\n".join(["%s \n %s \n\t%s\n" % ((method.ljust(spacing)),"("+str(input(getattr(obj,method)))+")", process_method(str(getattr(obj, method).__doc__))) for method in methods_list])
	a=raw_input("Y or N (case sensitive): Keep Looking?")
	if a=="Y":
		print [method for method in dir(obj) if callable(getattr(obj,method))],[process_method(str(getattr(obj,method).__doc__)) for method in dir(obj) if callable(getattr(obj,method))]

def poke_module(obj):
	method=[method for method in dir(obj) if callable(getattr(obj,method))]
	print method

def poke_data(obj):
	pass
	#inspect.isdatadescriptor()

def poke_frame(obj):
	pass
	#inspect.isframe()
	#inspect.istraceback()


def ls(boolean, option1, option2):
	"""Change boolean to an option that may have a value. If boolean exists at any value besides: None, False, "" (empty string),0,(maybe more empty kinds of 'variables') then it returns 'True'. This means most objects, dictionaries, etc: will act as True and advancing the current 'option' as it's 'return value'. Basically, the option returned is the last non-false option provided. The exception being that if all values are False, "", etc., then the last option is the return value (i.e. (None or False) would return False, rather than None when a str() function is applied to the result, where None advanced the interactive terminal as if the user hit enter. However, if this is an actual instance of something (due to modifying __value to return False, None,etc.)"""
	return boolean and option1 or option2

def modules():
	"""Lists all available modules"""
	help("modules")

def poke_function(obj):
	"""Returns with required arguments of a function"""
	a= str(str(inspect.getargspec(func)).split("]")[0]).split("[")[1]
	return a
"""This sections is just notes:
inspect: getabsfile(),isfunction(), isclass(),isbuiltin(), ismodule(),ismethod(), classify_classy_attrs(cls)
pydoc: isdata(),ispath(),locate()
sys:stderr,last_type, last_value,
"""

"""This is for debugging:
inspect: getcallargs(), getfile(), getframeinfo(),getoutterframes(),getsource(),getsourcefile(), istraceback(),trace(),stack()"""
if __name__=="__main__":
	a=raw_input("Name a module: ")
	help(a)
