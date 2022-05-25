import json
import numpy as np
import os
import pandas as pd
from datetime import datetime

PATH_SUMARIZED_METRICS = "sumarized-metrics"
if not os.path.exists(PATH_SUMARIZED_METRICS):
    os.makedirs(PATH_SUMARIZED_METRICS)

def calculate_diff(last_release_date, next_release_date):
    last_release_date = last_release_date.replace("T", " ")
    last_release_date = last_release_date.replace("Z", "")
    last_release_date =  datetime.fromisoformat(last_release_date)

    next_release_date = next_release_date.replace("T", " ")
    next_release_date = next_release_date.replace("Z", "")
    next_release_date =  datetime.fromisoformat(next_release_date)
    
    delta = next_release_date - last_release_date
    return abs(delta.days)

columns = ["R1toR2", "R2toR3", "R3toR4", "R4toR5", "R5toR6", "R6toR7", "R7toR8", "R8toR9", "R9toR10"]
df = pd.DataFrame([], columns=columns) 
df.to_csv(f"{PATH_SUMARIZED_METRICS}/date_diff_metrics.csv")

df = pd.read_csv("repo_releases_created_date.csv")
for index, row in df.iterrows():
    r1r2 = calculate_diff(row['R1'], row['R2'])
    r2r3 = calculate_diff(row['R2'], row['R3'])
    r3r4 = calculate_diff(row['R3'], row['R4'])
    r4r5 = calculate_diff(row['R4'], row['R5'])
    r5r6 = calculate_diff(row['R5'], row['R6'])
    r6r7 = calculate_diff(row['R6'], row['R7'])
    r7r8 = calculate_diff(row['R7'], row['R8'])
    r8r9 = calculate_diff(row['R8'], row['R9'])
    r9r10 = calculate_diff(row['R9'], row['R10'])

    data_to_save = [r1r2, r2r3, r3r4, r4r5, r5r6, r6r7, r7r8, r8r9, r9r10]
    df_diff = pd.DataFrame([data_to_save]) 
    df_diff.to_csv(f"{PATH_SUMARIZED_METRICS}/date_diff_metrics.csv", mode='a', header=False, index=False)


df = pd.read_csv(f"{PATH_SUMARIZED_METRICS}/date_diff_metrics.csv")
r1r2 = df['R1toR2'].median()
r2r3 = df['R2toR3'].median()
r3r4 = df['R3toR4'].median()
r4r5 = df['R4toR5'].median()
r5r6 = df['R5toR6'].median()
r6r7 = df['R6toR7'].median()
r7r8 = df['R7toR8'].median()
r8r9 = df['R8toR9'].median()
r9r10 = df['R9toR10'].median()

columns = ["R1toR2", "R2toR3", "R3toR4", "R4toR5", "R5toR6", "R6toR7", "R7toR8", "R8toR9", "R9toR10"]
data_to_save = [r1r2, r2r3, r3r4, r4r5, r5r6, r6r7, r7r8, r8r9, r9r10]
df = pd.DataFrame([data_to_save], columns=columns) 
df.to_csv(f"{PATH_SUMARIZED_METRICS}/date_diff_median.csv")