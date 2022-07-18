#-*- coding = utf-8 -*-
# @Time :       2021/02/22 22:22
# @Author :     Yuanyy
# @File :       FeatureSelection.py
# @Package :    
# @IDE :        PyCharm
# @JDK :        Python 3.7.1
# @Description :利用调参的数据集同时进行特征选择

import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from sklearn.metrics import accuracy_score, average_precision_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

# 导入文件
input = "F:\\DigenicProg\\New20210130\\Data\\Feature_Values\\"
output = "F:\\DigenicProg\\New20210130\\Data\\ML\\"
# positive
DIDA = pd.read_table(input + "Original\\DIDAcom_FV.txt")
features = [x for x in DIDA.columns if x not in ["GeneA", "GeneB", "Class", "From"]]
# negative
MD = pd.read_table(input + "Delt\\Training_MD_FV.txt")
LOF = pd.read_table(input + "Delt\\Training_LOF_FV.txt")
MDLOF = pd.read_table(input + "Delt\\Training_MDLOF_FV.txt")
Random = pd.read_table(input + "Delt\\Training_Random_FV.txt")
DIDA_NDI = pd.read_table(input + "Delt\\Training_DIDA_NDI_FV.txt")
#Training = pd.read_table("F:\\DigenicProg\\New20210130\\Data\\ML\\TrainingSet\\Trainingset_AdjustPara.txt")
Training = pd.concat([DIDA, MD, LOF, MDLOF, Random, DIDA_NDI], axis=0, ignore_index=True)
features = [x for x in Training.columns if x not in ["GeneA", "GeneB", "Class", "From"]]
X, y = Training[features], Training["Class"]

oob_score = []
Accuracy = []
Recall = []
Precision = []
F1score = []
AUC = []
PR = []
for i in list(range(36, 0, -1)):
    RF = RandomForestClassifier(n_estimators=200, random_state=10, oob_score=True)
    RF.fit(X, y)
    y_predprob = (RF.predict_proba(X))[:, 1]
    y_pred = RF.predict(X)
    R = recall_score(y, y_pred)
    P = precision_score(y, y_pred)
    F1 = 2 * P * R / (P + R)
    oob_score.append(RF.oob_score_)
    Accuracy.append(accuracy_score(y, y_pred))
    Recall.append(R)
    Precision.append(P)
    F1score.append(F1)
    AUC.append(metrics.roc_auc_score(y, y_predprob))
    PR.append(average_precision_score(y, y_predprob))

    rf_RFE = RFE(estimator=RF, n_features_to_select=i)
    rf_RFE.fit_transform(X, y)
    # bool数组不能直接进行取反操作
    print(str(i) + "-" + X.columns[rf_RFE.support_ == False])
    X = X.iloc[:, rf_RFE.support_]

#跑完上面后还要跑一边for的上半部分循环，因为i=1的时候模型没有跑

# 将Acc和AUC等计算的参数写入txt
Results = open("F:\\DigenicProg\\New20210130\\Data\\ML\\FeatureSelection\\FeatureSelectionparas_alltraining3.txt", "a")
Results.write("Count" + "\t" + "oob_score" + "\t" + "Accuracy" + "\t" + "Recall" + "\t"  + "Precision" + "\t" + "F1score" + "\t" + "AUC" + "\t" + "PR" + "\n")
for m in list(range(37)):
    Results.write(str(m+1) + "\t" + str(oob_score[m]) + "\t" + str(Accuracy[m]) + "\t" + str(Recall[m]) + "\t" + str(Precision[m]) + "\t" + str(F1score[m]) + "\t" + str(AUC[m]) + "\t" + str(PR[m]) + "\n")
Results.close()

#由obb score发现，当删除13个特征之后obb score值最大