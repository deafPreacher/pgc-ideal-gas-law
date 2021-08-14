from operator import truediv

def round_truediv(a, b):
	''' A helper function to round the result of division to 2 decimal points. '''	
	return round( truediv(a, b), 2 )

def inform_all_except(to_leave, all_connectors, message):
	for c in all_connectors:
		if c != to_leave:
			c[message]()