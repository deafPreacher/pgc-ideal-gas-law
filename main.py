from propagating_constraints import connector, converter

def main():
	# setting up the propagating constraints
	temprature = connector('Temprature in kelvins')
	pressure = connector('Pressure in atmosphere')
	volume = connector('Volume in litres')
	moles = connector('Number of moles')
	converter(pressure, volume, moles, temprature)

	quantities = {
		'temprature': temprature,
		'pressure': pressure,
		'volume': volume,
		'moles': moles
	}

	print('[INFO] All connectors ready.')
	print('[INFO] Available quantities are - ')

	[ print(key) for key in quantities.keys() ]

	unknown = input('[QUESTION] select the quantity you want to compute : ').lower()

	if (unknown not in quantities.keys()):
		raise 'the selected quantity is not present.'

	for quantity in quantities.keys():
		if quantity != unknown :
			value = float( input( 'enter the value of {0} : '.format(quantity) ) )
			quantities[quantity]['set']('User', value)

	print('[INFO] value of', unknown, 'is', quantities[unknown]['value'])


if __name__ == '__main__':
	main()