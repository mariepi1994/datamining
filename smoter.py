from imblearn.over_sampling import SMOTE
from collections import Counter
import numpy as np
import csv
def loadXcsv():
	ret_list = []
	with open('unbalanced_clean_x.csv') as csvfile:
		csvReader = csv.reader(csvfile)
		for row in csvReader:
			ret_list.append(row)
	return ret_list

def loadYcsv():
	ret_list = []
	with open('unbalanced_clean_y.csv') as csvfile:
		csvReader = csv.reader(csvfile)
		for row in csvReader:
			ret_list.append(row)
	return ret_list

def smoteData(x,y):
	value, count = np.unique(y, return_counts=True)
	counts = dict(zip(value, count))
	print("Before SMOTE")
	print(counts)
	
	my_smoter = SMOTE()
	x,y = my_smoter.fit_sample(x,y)

	value, count = np.unique(y, return_counts=True)
	counts = dict(zip(value, count))
	print("After SMOTE")
	print(counts)

def main():
	x = np.array(loadXcsv()).astype(np.float64)
	y = np.array(loadYcsv()).astype(np.float64)
	y = np.ravel(y)
	
	smoteData(x,y)

if __name__ == '__main__':
	main()