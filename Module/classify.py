# -*- coding: utf-8 -*-
"""
Created on Sun May  1 19:27:18 2022
@Sun: Sarthak Mishra

"""

import glob
import os
import pickle
import time

import pandas as pd

from Module.utility.len_time_module import time_convert
from Module.utility.wait_display import print_dot


def ensemble_proba(prb, prd, predict):
    cls_prob = prb[prd == predict]
    return cls_prob


def e_ne_prediction(tsX):
    """
    This function takes the generated kmer features as input and predicts whether it
    belongs to ESKAPEE or NON ESKAPEE Category.
    type data: dataframe
    :rtype: [cls, prob] a list consisting of the class label and confidence score.
    """
    # print(os.getcwd())
    model_dir = os.path.join("./Module/Models", "*.sav")
    # print(model_dir)

    models = glob.glob(model_dir)
    # print(models)

    # cls_lb = ['Enterococcus faecium', 'Staphylococcus aureus', 'Klebsiella pneumoniae', 'Acinetobacter baumannii',
    #           'Pseudomonas aeruginosa', 'Enterobacter', 'Escherichia coli', 'Non ESKAPE']

    pred_df = pd.DataFrame()
    prob_df = pd.DataFrame()

    counter = 0
    for mod in models:
        counter += 1
        model = pickle.load(open(mod, "rb"))
        if model[-1].verbose != 0:
            model[-1].verbose = 0
        predY_temp = model.predict(tsX)
        #print(predY_temp)
        probY_temp = model.predict_proba(tsX)
        name = os.path.splitext(os.path.basename(mod))[0]
        pred_df[name] = predY_temp
        prob_df[name] = [probY_temp[i, predY_temp[i] - 1] for i in range(len(predY_temp))]
        print_dot(1)

    #print(pred_df)
    pred = pred_df.mode(axis=1).iloc[:, 0].values.tolist()
    
    # pred_prob = np.mean(prob_df, axis=1)
    # pred_cls = [cls_lb[i - 1] for i in pred]
    if len(pred) == 1:
        return pred
    else:
        return None


def eskapee_classification(data):
    SampX = data.values.reshape(-1, 4003)[:, 3:]
    eskape_cls = ['Enterococcus faecium', 'Staphylococcus aureus', 'Klebsiella pneumoniae', 'Acinetobacter baumannii',
                  'Pseudomonas aeruginosa', 'Enterobacter','Escherichia coli']
    print("Classifying into ESKAPEE / Non ESKAPEE")
    time1 = time.perf_counter()
    pred = e_ne_prediction(SampX)[0]
    timetaken = round(time.perf_counter() - time1)
    print(f'Time Taken in prediction: {time_convert(timetaken)}')
    print()
    if pred < 8:
        mncls = 'ESKAPEE'
        sbcls = eskape_cls[pred - 1]
    else:
        mncls = 'Non-ESKAPEE'
        sbcls = 'N.A.'

    return {'mncl': mncls, 'sbcl': sbcls}
