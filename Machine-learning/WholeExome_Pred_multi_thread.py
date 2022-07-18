#-*- coding = utf-8 -*-
# @Time :       2021/02/24 22:38
# @Author :     Yuanyy
# @File :       WholeExome_Pred.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

import os
import pandas as pd
import pickle
from multiprocessing import Pool

input = "F:\\DigenicProg\\New20210130\\Data\\Feature_Values\\AllFV_split\\"
modelinput = "F:\\DigenicProg\\New20210130\\Data\\ML\\FeatureSelection\\"
output = "F:\\DigenicProg\\New20210130\\Data\\ML\\FeatureSelection\\Results\\WholeExome\\SplitedFiles\\"
obbfile = pd.read_table(modelinput + "ModelPara\\Test_Results.txt")

# load the model from disk
# 初步确定用10个模型
ModelNum = [21, 28, 48, 62, 64, 79, 84, 153, 162, 193]
ModelIndex = [x-1 for x in ModelNum]
ModelList = []
for m in ModelIndex:
    modelname = modelinput + "Model\\RF_finalized_model_" + str(m + 1) + ".mdl"
    model = pickle.load(open(modelname, 'rb'))
    ModelList.append(model)

# 利用obb_score给每个模型重新分配权重
Test_obb = list(obbfile.iloc[ModelIndex, 1])
weight = [(Test_obb[o] / sum(Test_obb)) for o in range(len(Test_obb))]

def get_predprob(input, file_num, ModelList):
    print("File " + str(file_num+1) + " starting...")
    Dataset = pd.read_table(input + "File_" + str(file_num+1) + ".txt")
    features = [x for x in Dataset.columns if x not in ["GeneA", "GeneB", "Class", "From", "NumOfCommonInteraction_CP", "commonInteractionJacSim_CP", "EssgCom", "RVIS_EVS.add", "FuncChangeInt.add"]]
    Xt, yt = Dataset[features], Dataset["Class"]
    for count in list(range(len(ModelList))):
        predprob = ModelList[count].predict_proba(Xt)[:, 1]
        predprob_c = [predprob[i] * weight[count] for i in range(len(Xt))]
        if count == 0:
            prob_add = predprob_c
        else:
            prob_add = [predprob_c[i] + prob_add[i] for i in range(len(prob_add))]
    final_prob = pd.concat([pd.DataFrame(Dataset.iloc[:, 0:2]), pd.DataFrame(prob_add, columns=["Predprob"])], axis=1)
    final_prob.to_csv(output + "File_" + str(file_num+1) + "_predprob.txt", sep="\t", index=False)

# Predict

# 开始多进程处理
print('Parent process %s.' % os.getpid())
p = Pool(6)
# 遍历每一个case
for j in range(0, 97):
    p.apply_async(get_predprob, args=(input, j, ModelList))
print('Waiting for all subprocesses done...')
p.close()
p.join()
print('All subprocesses done.')

# Predict
# for j in range(0, 97):
#     print("File " + str(j+1) + " starting...")
#     Dataset = pd.read_table(input + "File_" + str(j+1) + ".txt")
#     features = [x for x in Dataset.columns if x not in ["GeneA", "GeneB", "Class", "From", "NumOfCommonInteraction_CP", "commonInteractionJacSim_CP", "EssgCom", "RVIS_EVS.add", "FuncChangeInt.add"]]
#     Xt, yt = Dataset[features], Dataset["Class"]
#     for count in list(range(len(ModelList))):
#         predprob = ModelList[count].predict_proba(Xt)[:, 1]
#         predprob_c = [predprob[i] * weight[count] for i in range(len(Xt))]
#         if count == 0:
#             prob_add = predprob_c
#         else:
#             prob_add = [predprob_c[i] + prob_add[i] for i in range(len(prob_add))]
#     final_prob = pd.concat([pd.DataFrame(Dataset.iloc[:, 0:2]), pd.DataFrame(prob_add, columns=["Predprob"])], axis=1)
#     final_prob.to_csv(output + "File_" + str(j+1) + "_predprob.txt", sep="\t", index=False)


