import torchvision
import random
import os

trainset = torchvision.datasets.MNIST(root='../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../data/MNIST', train=False, download=True)

datasets = {'train': trainset, 'test': testset}

def get_img_file(file_name):
    imagelist = []
    for parent, dirnames, filenames in os.walk(file_name):
        for filename in filenames:
            if filename.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                imagelist.append(os.path.join(parent, filename))
        return imagelist



def next_example(dataset, i, j, shapeset):
    x, y = next(i), next(i)
    z = next(j)
    (_, c1), (_, c2) = dataset[x], dataset[y]
    description = shapeset[z].replace('shapes/','')
    description = description.replace('.png','')
    #print("description is:",description)
    #print("trainset[x] is: ",trainset[x])
    #print("x is ",x,"y is ",y,"c1 is ",c1,"c2 is ",c2)
    return x, y, c1 + c2, description


def gather_examples(dataset_name, filename, shapeset):
    dataset = datasets[dataset_name]
    examples = list()

    indices = list(range(len(dataset)))
    #print("indices are:",indices)
    
    shapexample = list(range(len(shapeset)))
    #print("shapeset is:",shapexample)
    
    random.shuffle(indices)
    random.shuffle(shapexample)

    i = iter(indices)
    j = iter(shapexample)
    while True:
        try:
            examples.append(next_example(dataset, i,j,shapeset))
        except StopIteration:
            break
    #print(examples)
    with open(filename, 'w') as f:
        for example in examples:
            args = tuple('{}({})'.format(dataset_name, e) for e in example[:-2])
            print(args)
            f.write('addition({},{},{},{}).\n'.format(*args, example[-2],example[-1]))


#gather_examples('train', 'train_data.txt')
#gather_examples('test', 'test_data.txt')
shapeset = get_img_file("shapes")
gather_examples('train', 'newdata.txt',shapeset)
