#-*- coding = utf-8 -*-
# @Time :       2021/03/02 21:56
# @Author :     Yuanyy
# @File :       4_FeatureContribution.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :

import pandas as pd
import numpy as np
import pickle
import shap

# 利用treeinterpreter包计算每个特征对于每个样本分类结果的贡献度
# instances_Xt = Xt.values
# prediction_Xt, bias_Xt, contributions_Xt = ti.predict(RF, Xt)
# for q in range(len(contributions_Xt)):
#     if q == 0:
#         tmp2 = pd.concat([features, pd.DataFrame(contributions_Xt[q], columns=["model" + str(i + 1) + "_" + str(j + 1) + "_" + str(q + 1) + "_" + str(0),"model" + str(i + 1) + "_" + str(j + 1) + "_" + str(q + 1) + "_" + str(1)])], axis=1)
#     else:
#         tmp2 = pd.concat([tmp2, pd.DataFrame(contributions_Xt[q], columns=["model" + str(i + 1) + "_" + str(j + 1) + "_" + str(q + 1) + "_" + str(0), "model" + str(i + 1) + "_" + str(j + 1) + "_" + str(q + 1) + "_" + str(1)])], axis=1)
# tmp2.to_csv(output + "ti_Eva_Contributions_" + str(i + 1) + "_" + str(j + 1) + ".txt", sep="\t", index=False)

# file path
input = "F:\\DigenicProg\\New20210130\\Data\\Feature_Values\\"
modelinput = "F:\\DigenicProg\\New20210130\\Data\\ML\\FeatureSelection\\"
TestDatainput = "F:\\DigenicProg\\New20210130\\Data\\Feature_Values\\"
output = "F:\\DigenicProg\\New20210130\\Data\\ML\\FeatureSelection\\shap_after\\"

# import Data
DIDA = pd.read_table(input + "Original\\DIDAcom_FV.txt")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From", "NumOfCommonInteraction_CP", "commonInteractionJacSim_CP", "EssgCom", "RVIS_EVS.add", "FuncChangeInt.add"]]
obbfile = pd.read_table(modelinput + "ModelPara\\Test_Results.txt")
AllPositive = DIDA
# negative
MD = pd.read_table(input + "Delt\\Training_MD_FV.txt")
LOF = pd.read_table(input + "Delt\\Training_LOF_FV.txt")
MDLOF = pd.read_table(input + "Delt\\Training_MDLOF_FV.txt")
Random = pd.read_table(input + "Delt\\Training_Random_FV.txt")
DIDA_NDI = pd.read_table(input + "Delt\\Training_DIDA_NDI_FV.txt")
AllNegative = pd.concat([MD, LOF, MDLOF, Random, DIDA_NDI], axis=0, ignore_index=True)
# evaluate
MDe = pd.read_table(input + "Delt\\Evaluate_MD_FV.txt")
LOFe = pd.read_table(input + "Delt\\Evaluate_LOF_FV.txt")
MDLOFe = pd.read_table(input + "Delt\\Evaluate_MDLOF_FV.txt")
Randome = pd.read_table(input + "Delt\\Evaluate_Random_FV.txt")
DIDA_NDIe = pd.read_table(input + "Delt\\Evaluate_DIDA_NDI_FV.txt")
AllEvaluative = pd.concat([MDe, LOFe, MDLOFe, Randome, DIDA_NDIe], axis=0, ignore_index=True)


# load the model from disk
ModelNum = [21, 28, 48, 62, 64, 79, 84, 153, 162, 193]
ModelIndex = [x-1 for x in ModelNum]
ModelList = []
for i in ModelIndex:
    modelname = modelinput + "Model\\RF_finalized_model_" + str(i + 1) + ".mdl"
    model = pickle.load(open(modelname, 'rb'))
    ModelList.append(model)

# 利用obb_score给每个模型重新分配权重
Test_obb = list(obbfile.iloc[ModelIndex, 1])
weight = [(Test_obb[i] / sum(Test_obb)) for i in range(len(Test_obb))]

# 利用shap计算每个特征在每个样本分类上的贡献度
dataset = AllEvaluative
dataset = pd.read_table(TestDatainput + "Original\\Manualcom_FV.txt")
X, y = dataset[features], dataset["Class"]
for i in range(len(ModelList)):
    explainer = shap.TreeExplainer(ModelList[i])
    shap_values_X = explainer.shap_values(X)
    for p in range(X.iloc[:, 0].size):
        if p == 0:
            tmp = pd.concat([pd.DataFrame(features, columns=["Feature"]), pd.DataFrame(shap_values_X[0][p], columns=["model" + str(ModelNum[i]) + "_" + str(p + 1) + "_" + str(0)]), pd.DataFrame(shap_values_X[1][p], columns=["model" + str(ModelNum[i]) + "_" + str(p + 1) + "_" + str(1)])], axis=1)
        else:
            tmp = pd.concat([tmp, pd.DataFrame(shap_values_X[0][p], columns=["model" + str(ModelNum[i]) + "_" + str(p + 1) + "_" + str(0)]), pd.DataFrame(shap_values_X[1][p], columns=["model" + str(ModelNum[i]) + "_" + str(p + 1) + "_" + str(1)])], axis=1)
    tmp.to_csv(output + "Manual/shap_Contributions_" + str(ModelNum[i]) + ".txt", sep="\t", index=False)

