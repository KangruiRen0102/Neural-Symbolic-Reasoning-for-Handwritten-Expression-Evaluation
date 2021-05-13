import os.path
import sys
sys.path.append('/Users/sebastianren/Desktop/deepproblog')
from train import train_model
from data_loader import load
from examples.NIPS.MNIST.mnist  import MNIST_Net, neural_predicate
import torch
from network import Network
from model import Model
from optimizer import Optimizer


train_queries = load('train.txt')
#print("train_queries are: ",train_queries)
test_queries = load('test.txt')

#train_queries = load('newdata_train.txt')
#test_queries = load('test.txt')[91:-1]

def test(model):
    acc = model.accuracy(test_queries, test=True)
    print('Accuracy: ', acc)
    return [('accuracy', acc)]


with open('multi_digit.pl') as f:
    problog_string = f.read()

network = MNIST_Net()
net = Network(network, 'mnist_net', neural_predicate)
net.optimizer = torch.optim.Adam(network.parameters(), lr=0.001)
model = Model(problog_string, [net], caching=False)
#print("model is: ", model.model_string)
optimizer = Optimizer(model, 2)

#test(model)
train_model(model, train_queries, 1, optimizer, test_iter=1000, test=test, snapshot_iter=10000)
