import pandas as pd
import numpy as np
import os
import json
from sklearn.metrics import r2_score

directory = rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\outputs_computed\computed"
directory_GT = rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\outputs\GT"

r2_score_list = []

# Computing the the r2_score of the computed monthly averages against the extracted monthly averages
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    file_path_GT = os.path.join(directory_GT, filename)

    df_pred = pd.read_csv(file_path)
    df_true = pd.read_csv(file_path_GT)

    for column in df_true.columns:
        pred_list = df_pred[column]
        true_list = []
        for i in range(len(list(df_true[column]))):
            if list(df_true[column])[i] !=0 :
                true_list.append(list(df_true[column])[i])
            else :
                true_list.append(list(df_pred[column])[i])

        r2 = r2_score(true_list, pred_list)
        r2_score_list.append(r2)

# Writing it to a json file which will be tracked as a metric(-M) by DVC
with open(rf"C:\Users\91979\Desktop\Jup_NoteBks\BDL\Asgt_3\example\DVC_repo\metrics\r2_score.json", 'w') as f:
        f.write(json.dumps(
            dict(avg_r2_score=np.mean(np.array(r2_score_list))),
            indent=4
        ))