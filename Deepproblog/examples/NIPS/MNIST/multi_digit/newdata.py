import torchvision
import random
import os

trainset = torchvision.datasets.MNIST(root='../../../data/MNIST', train=True, download=True)
testset = torchvision.datasets.MNIST(root='../../../data/MNIST', train=False, download=True)
#dictionary 前面的是key 后面的是value
datasets = {'train': trainset, 'test': testset}
#i 应该是dataset中的一个indices

def get_img_file(file_name):
    imagelist = []
    for parent, dirnames, filenames in os.walk(file_name):
        for filename in filenames:
            if filename.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                imagelist.append(os.path.join(parent, filename))
        return imagelist

        
#得到一个数字 multidigit
def next_number(i, j, dataset, shapeset, nr_digits):
    #得到随机图形出现位置
    variable_digit = random.randint(0, nr_digits)
    n = 0
    #图片
    nr = list()  
    output_var = 0  
   
    for index in range(nr_digits):
        print("variable_digit is:",variable_digit)
        if(index == variable_digit):
            x = next(j)
            description = shapeset[x].replace('shapes/','')
            description = description.replace('.png','')
            c = random.randint(0, 9)
            output_var = c
        else:
            x = next(i)
            _, c = dataset[x]
        #item读进来直接写入空list
        n = n * 10 + c
        nr.append(str(x))
    print("nr is",nr,"n is",n,"output_var is",output_var)
    return nr, n, output_var


def next_example(i, j, dataset, shapeset, op, length):
    #return的是两个symbol和他们加起来的结果
    nr1, n1, output_var1 = next_number(i, j, dataset, shapeset, length)
    nr2, n2, output_var2 = next_number(i, j, dataset, shapeset, length)
    return nr1, nr2, op(n1, n2), output_var1, output_var2

#op取传统加法
def generate_examples(dataset_name, op, length, out, shapeset):
    dataset = datasets[dataset_name]
    #提取dataset中元素将其转换为list并打乱
    indices = list(range(len(dataset)))
    shapexample = list(range(len(shapeset)))

    random.shuffle(indices)
    random.shuffle(shapexample)
    #随即提取element
    i = iter(indices)
    j = iter(shapexample)

    examples = list()
    while (True):
        try:
            #调用前期function
            examples.append(next_example(i, j, dataset, shapeset, op, length))
        except StopIteration:
            break

    with open(out, 'w') as f:
        
        for example in examples:
            #args1 = {}
            #args2 = {}
            #分别把两个symbol和结果输入写进去
            #for index in range(len(example[0])):
                #if index == example[7]:
                 #   args = tuple('{}({})'.format(example[5], e)
                  #  argss1 = list(args1)
                   # argss1.append(args)
                    #args1 = tuple(argss1)
                #else:
                 #   args = tuple('{}({})'.format(dataset_name, e)
                  #  argss1 = list(args1)
                   # argss1.append(args)
                    #args1 = tuple(argss1)
            #for index in range(len(example[1])):
             #   if index == example[8]:
              #      args = tuple('{}({})'.format(example[6], e)
               #     argss2 = list(args2)
                #    argss2.append(args)
                 #   args2 = tuple(argss2)
                #else:
                 #   args = tuple('{}({})'.format(dataset_name, e)
                  #  argss2 = list(args2)
                   # argss2.append(args)
                    #args2 = tuple(argss2)
            args1 = tuple('{}({})'.format(dataset_name, e) for e in example[0])
            args2 = tuple('{}({})'.format(dataset_name, e) for e in example[1])
            args3 = example[2]
            f.write('addition([{}], [{}], {}, {}, {}).\n'.format(args1,args2,args3,example[3],example[4]))
shapeset = get_img_file("shapes")
generate_examples('train',lambda x, y: x + y, 1, 'newdata_train.txt', shapeset)
generate_examples('train',lambda x, y: x + y, 3, 'newdata.txt', shapeset)