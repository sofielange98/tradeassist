import pandas as pd
import numpy.random as rand

def get_random_currency():
	phys = pd.read_csv('app/static/physical_currency_list.csv')
	dig = pd.read_csv('app/static/digital_currency_list.csv')
	c1 = rand.randint(0,len(phys))
	c2 = rand.randint(0,len(phys))
	c1 = phys.iloc[c1]['currency code']
	c2 = phys.iloc[c2]['currency code']
	return (c1,c2)