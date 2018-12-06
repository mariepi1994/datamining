import pandas as pd
import numpy as np
import math
import scipy.io
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from smoter import smoteData, printXTocsv, printYTocsv


class Models():
    def __init__(self,train_x, test_x, train_y, test_y):
        self.y_train = train_y
        self.y_test = test_y
        self.x_train = train_x
        self.x_test = test_x

    def SVM(self):
        print("Running SVM...")
        clf = SVC(decision_function_shape='ovo',kernel='poly', gamma='auto',degree=2)
        clf.fit(self.x_train, self.y_train)
        return clf.score(self.x_test,self.y_test)*100

    def NeuralNet(self):
        print("Running Neural Net....")
        clf = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(25,))
        clf.fit(self.x_train, self.y_train)
        y_pred = clf.predict(self.x_test)
        return clf.score(self.x_test,self.y_test)*100


#split the data into train(70%) and test(30%)
def splitData(fx, fy, train_percentage):
    max_num = 50
    file_x = pd.read_csv(fx)
    file_y = pd.read_csv(fy)
    X = file_x.values
    Y = file_y.values

    indices = np.random.permutation(X.shape[0])
    split = math.floor(len(indices) * train_percentage)
    train_i, test_i = indices[:split], indices[split:]

    train_x, test_x = X[train_i,:], X[test_i,:]
    train_y, test_y = Y[train_i,:], Y[test_i,:]
    return train_x[0:max_num], test_x[0:max_num], train_y[0:max_num], test_y[0:max_num]


def main():
    x_file = "unbalanced_all_x.csv"
    y_file = "unbalanced_all_y.csv"
    train_x, test_x, train_y, test_y = splitData(x_file, y_file, 0.70)

    train_y = [item for sublist in train_y for item in sublist]
    test_y  = [item for sublist in test_y for item in sublist]

    train_x, train_y = smoteData(train_x, train_y)
    model = Models(train_x, test_x, train_y, test_y)

    print("----------Results - Before Smote--------------")
    print("SVM: ", model.SVM())
    print("Neural Net: ", model.NeuralNet())

    train_x, train_y = smoteData(train_x, train_y)
    model = Models(train_x, test_x, train_y, test_y)

    print("----------Results - After Smote--------------")
    print("SVM: ", model.SVM())
    print("Neural Net: ", model.NeuralNet())

if __name__ == '__main__':
    main()
