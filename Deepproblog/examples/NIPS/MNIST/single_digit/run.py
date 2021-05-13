import os.path
import sys
sys.path.append('/Users/sebastianren/Desktop/deepproblog')
from train import train_model
from data_loader import load
from examples.NIPS.MNIST.mnist import test_MNIST, MNIST_Net, neural_predicate
from model import Model
from optimizer import Optimizer
from network import Network
import torch


queries = load('train_data.txt')
test_queries = load('test_data.txt')

with open('addition.pl') as f:
    problog_string = f.read()

#print(problog_string)
#本身pytorch net，自带forward
network = MNIST_Net()
#Network包裹原net，加neural——predicate
net = Network(network, 'mnist_net', neural_predicate)
net.optimizer = torch.optim.Adam(network.parameters(), lr=0.001)

model = Model(problog_string, [net], caching=False)
#print("model is: ", model.model_string)
optimizer = Optimizer(model, 2)

train_model(model, queries, 1, optimizer, test_iter=1000, test=lambda x: x.accuracy(test_queries, test=True), snapshot_iter=10000)
