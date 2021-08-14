from operator import mul, add, sub
from utils import round_truediv as div, inform_all_except

def make_ternary_constraint(a, b, c, ab, bc, ac):
	''' A generic function that constructs a ternary constraint. 
	A constraint is system that can respond to changes. '''

	def update_value():
		''' This function check values of two variables, and sets the third one accordingly. '''
		av, bv, cv = [ con['has_value']() for con in (a, b, c) ]

		if av and bv :
			c_value = ab( a['value'], b['value'] )
			c['set']( constraint, c_value )

		elif bv and cv :
			a_value = bc( c['value'], b['value'] )
			a['set']( constraint, a_value )

		elif av and cv :
			b_value = ac( c['value'], a['value'] )
			b['set']( constraint, b_value )

	def forget_value():
		''' This function makes all of its connectors forget the value they're holding. '''
		for con in (a, b, c):
			con['forget']( constraint )

	constraint = {
		"update": update_value,
		"forget": forget_value
	}

	for con in (a, b, c):
		con['connect']( constraint )

	return constraint

def multiplier(a, b, c):
	''' 
	The constaint is C = A * B.
	A, B, C are all connectors.
	MUL is for computing the value of C i.e. C = MUL(A, B).
	first DIV is for computing the value of A i.e. A = DIV(C, B).
	second DIV is for computing the value of B i.e. B = DIV(C, A)
	'''

	return make_ternary_constraint(a, b, c, mul, div, div)

def adder(a, b, c):
	return make_ternary_constraint(a, b, c, add, sub, sub)

def connector(name=None):
	''' 
	Connector is system that can hold a value and its source, but also a set of constaints.
	If the value of a connector is changed, then all the constraints connected to it will also respond to this change.
	'''

	informant = None
	constraints = []

	def set_value(source, value):
		nonlocal informant

		val = connector['value']
		if val is None :
			informant, connector['value'] = source, value
			if name is not None :
				# print('Setting', name, 'to', value)
				pass
			inform_all_except(source, constraints, 'update')
		else :
			print('Contradiction detected', name, val, 'vs', value)

	def forget_value(source) :
		nonlocal informant

		if informant == source :
			informant, connector['value'] = None, None
			if name is not None :
				print('Forgetting', name)
			inform_all_except(source, constraints, 'forget')
		# else :
		# 	print('Source is not correct')

	connector = {
		"set": set_value,
		"forget": forget_value,
		"value": None,
		"has_value": lambda : connector['value'] != None,
		"connect": lambda x: constraints.append(x)
	}

	return connector

def constant(connector, value):
	constraint = {}
	connector['value'] = value
	return constraint

def converter(p, v, n, t):
	''' 

	This function makes up a complex message passing system using the above functions.
	The following system is for the ideal gas law.
	Each input variable is a user defined connector.
	P*V = N*T*R

	The breakdown is as follow:
		1. A multiplier constraint for P*V. A = MUL(P, V)
		2. A multiplier constraint for N*T. B = MUL(N, T)
		3. A multiplier constraint for B*R. A = MUL(B, R)
		4. A constant constraint for R. R = 0.08314

	The overall constraint looks like:
		A = B * R
		|   |   |- R = 0.08314
		|   |   
		|   |- B = N * R
		|   
		|- A = P * V		
	
	If you understand the pattern, you can make this system for any formula you know.

	'''

	a, b, r = [ connector() for _ in range(3) ]
	multiplier(p, v, a)
	multiplier(n, t, b)
	multiplier(b, r, a)	
	constant(r, 0.08314) # ideal gas constant