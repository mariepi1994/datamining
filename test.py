import numpy
# x is your dataset
x = numpy.random.rand(100, 5)
print(x)
indices = numpy.random.permutation(x.shape[0])
training_idx, test_idx = indices[:80], indices[80:]
training, test = x[training_idx,:], x[test_idx,:]
print(training_idx, test_idx)
