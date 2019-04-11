# coding: utf-8
import numpy as np

def softmax(arr):
    e_arr = np.exp(arr-np.max(arr))
    return e_arr/np.sum(e_arr)


# 初始值随意设定
start_score=np.zeros([16],dtype='float32')+1000


# mmr - 之前的玩家分数<br>
# result - 本次比赛结果<br>
# k - 整体分数量级<br>
# mmr_zoom - 用于调整softmax结果分布的参数 默认0.1<br>
# result_zoom - 用于调整softmax结果分布的参数 默认1<br>
# beta - 滑动平均参数 默认0.9<br>
def update(mmr,result,k=1000,mmr_zoom=0.01,result_zoom=0.01,beta=0.85):
    predict = softmax(mmr*mmr_zoom)
    actual = softmax(result*result_zoom)
    this_mmr = mmr + k*(actual-predict)
    return mmr * beta + (1-beta) * this_mmr


result = np.array([400,500,250,200,150,100,90,80,70,60,50,40,30,20,10,5],dtype='float32')


score = update(start_score,result,1000,0.01,0.01,0.85)


score = update(score,result,1000,0.01,0.01,0.85)

