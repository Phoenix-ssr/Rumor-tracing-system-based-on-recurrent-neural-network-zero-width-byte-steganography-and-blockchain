import zipfile
import os
import random
from PIL import Image
from PIL import ImageEnhance
import json

# 导入必要的包
import os
from multiprocessing import cpu_count
import numpy as np
import shutil
import paddle
import paddle.fluid as fluid
from PIL import Image
import matplotlib.pyplot as plt

def lstm_net(ipt, input_dim):

    # 以数据的IDs作为输入

    emb = fluid.layers.embedding(input=ipt, size=[input_dim, 128], is_sparse=True)

    # 第一个全连接层

    fc1 = fluid.layers.fc(input=emb, size=128)

    # 进行一个长短期记忆操作

    lstm1, _ = fluid.layers.dynamic_lstm(input=fc1, #返回：隐藏状态（hidden state），LSTM的神经元状态

                                         size=128) #size=4*hidden_size

    # 第一个最大序列池操作

    fc2 = fluid.layers.sequence_pool(input=fc1, pool_type='max')

    # 第二个最大序列池操作

    lstm2 = fluid.layers.sequence_pool(input=lstm1, pool_type='max')

    # 以softmax作为全连接的输出层，大小为2,也就是正负面

    out = fluid.layers.fc(input=[fc2, lstm2], size=2, act='softmax')

    return out
paddle.enable_static()
words = fluid.data(name='words', shape=[None,1], dtype='int64', lod_level=1)
label = fluid.data(name='label', shape=[None,1], dtype='int64')
use_cuda = False 
place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()


################################################################################################################
# 用训练好的模型进行预测并输出预测结果
# 创建执行器
place = fluid.CPUPlace()
infer_exe = fluid.Executor(place)
infer_exe.run(fluid.default_startup_program())

save_path = './app/RNN/work/infer_model/'

# 从模型中获取预测程序、输入数据名称列表、分类器
[infer_program, feeded_var_names, target_var] = fluid.io.load_inference_model(dirname=save_path, executor=infer_exe)


# 获取数据
def get_data(sentence):
    # 读取数据字典
    with open('./app/RNN/data/dict.txt', 'r', encoding='utf-8') as f_data:
        dict_txt = eval(f_data.readlines()[0])
    dict_txt = dict(dict_txt)
    # 把字符串数据转换成列表数据
    keys = dict_txt.keys()
    data = []
    for s in sentence:
        # 判断是否存在未知字符
        if not s in keys:
            s = '<unk>'
        data.append(np.int64(dict_txt[s]))
    return data


data = []
# 获取图片数据
data1 = get_data('这新闻看得我彻底凌乱了，堪比大片啊！【广州伪娘coser 遭黑人强暴，路过维吾尔族商贩拔刀相助】。。。这信息量。。。。')
data2 = get_data('#开讲啦#【正在播出，黄西-不完美怎么了】我觉得如果等你把自己的房间装饰得非常漂亮后再请客的话，你可能已经没有朋友了。如果等你功成名就赚了钱以后再找女朋友的话，能够和你同甘共苦的人可能已经结婚了，我就觉得长期的目标应该定高一点，但近期的目标应该定得低一点。@黄西Joe_Wong @唯众传媒')
data3 = get_data('一代商业帝国索尼申请破产！。')
data.append(data1)
data.append(data2)
data.append(data3)
#for i in range(100):
#    data.append(data1)
# 获取每句话的单词数量
base_shape = [[len(c) for c in data]]

# 生成预测数据
tensor_words = fluid.create_lod_tensor(data, base_shape, place)

# 执行预测

result = infer_exe.run(program=infer_program,
                 feed={feeded_var_names[0]: tensor_words},
                 fetch_list=target_var)

# 分类名称
names = [ '谣言', '非谣言']

# 获取结果概率最大的label
for i in range(len(data)):
    lab = np.argsort(result)[0][i][-1]
    print('预测结果标签为：%d， 分类为：%s， 概率为：%f' % (lab, names[lab], result[0][i][lab]))


def forecast(message):
    data = []
    data.append(get_data(message))
    # 获取每句话的单词数量
    base_shape = [[len(c) for c in data]]

    # 生成预测数据
    tensor_words = fluid.create_lod_tensor(data, base_shape, place)

    # 执行预测

    result = infer_exe.run(program=infer_program,
                     feed={feeded_var_names[0]: tensor_words},
                     fetch_list=target_var)

    # 分类名称
    names = [ '谣言', '非谣言']
    i=0
    lab = np.argsort(result)[0][i][-1]
    #resultdict = '预测结果标签为：%d， 分类为：%s， 概率为：%f' % (lab, names[lab], result[0][i][lab])
    resultdict = {"预测结果标签":lab,"分类":names[lab],"概率":result[0][i][lab]}
    print(resultdict)
    return resultdict

if __name__ == '__main__':
    retun 