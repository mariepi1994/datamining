import pandas as pd
import numpy as np
import math

class Models():
    def __init__():
        self.y_train = None
        self.y_test = None
        self.x_train = None
        self.y_train = None
        pass



#split the data into train(70%) and test(30%)
def splitData(fx, fy, train_percentage):
    file_x = pd.read_csv(fx)
    file_y = pd.read_csv(fy)
    X = file_x.values
    Y = file_y.values

    print(X.shape[0])
    indices = np.random.permutation(X.shape[0])
    print(indices)
    split = math.floor(len(indices) * train_percentage)
    train_i, test_i = indices[:split], indices[split:]

    train_x, test_x = X[train_i,:], X[test_i,:]
    train_y, test_y = Y[train_i,:], Y[test_i,:]
    print(train_x, test_x, train_y, test_y  )


def main():
    splitData("unbalanced_x.csv", "unbalanced_y.csv", 0.70)

if __name__ == '__main__':
    main()
