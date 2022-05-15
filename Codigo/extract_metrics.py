import json
import numpy as np
import os
import pandas as pd
import math

PATH_SUMARIZED_METRICS = "sumarized-metrics"
if not os.path.exists(PATH_SUMARIZED_METRICS):
    os.makedirs(PATH_SUMARIZED_METRICS)

def calculate_diff(data):
    diffs = []
    for idx, value in enumerate(data):
        if idx == 9:
            continue
        if value == 0:
            value = 1
        diff = (data[idx + 1] * 100) / value
        diff = diff- 100
        diffs.append(round(diff, 2))
    return diffs

columns = ["Name", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
df = pd.DataFrame([], columns=columns) 
df.to_csv(f"{PATH_SUMARIZED_METRICS}/cc_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/locs_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/llocs_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/comments_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/mi_metrics.csv")

columns = ["Name", "R1toR2", "R2toR3", "R3toR4", "R4toR5", "R5toR6", "R6toR7", "R7toR8", "R8toR9", "R9toR10"]
df = pd.DataFrame([], columns=columns) 
df.to_csv(f"{PATH_SUMARIZED_METRICS}/cc_diff_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/locs_diff_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/llocs_diff_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/comments_diff_metrics.csv")
df.to_csv(f"{PATH_SUMARIZED_METRICS}/mi_diff_metrics.csv")

PATH_METRICS = "collected-metrics"
# iterate over files in
# that directory
file_names = []
for filename in os.listdir(PATH_METRICS):
    f = os.path.join(PATH_METRICS, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file_names.append(f)

for file_name in file_names:
    f = open(file_name)
    data = json.load(f)
    count = 0
    repo_name = data['repo_name']
    
    # RQ 1
    complexitys = []
    for files in data["cc_metrics"]:
        if not files:
            complexitys.append(0)
            continue
        complexity_rank = []
        complexity = 0
        for file in files:
            file_complexity = 0
            for structure_metrics in files[file]:
                if structure_metrics == 'error':
                    continue
                file_complexity = file_complexity + structure_metrics['complexity']
            complexity = complexity + file_complexity
        complexitys.append(complexity)    
    
    data_to_save = [data['repo_name'], complexitys[0], complexitys[1], complexitys[2], complexitys[3], complexitys[4], complexitys[5], complexitys[6], complexitys[7], complexitys[8], complexitys[9]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/cc_metrics.csv", mode='a', header=False, index=False)

    data_diff_to_save = calculate_diff(complexitys)
    data_to_save = [data['repo_name'], data_diff_to_save[0], data_diff_to_save[1], data_diff_to_save[2], data_diff_to_save[3], data_diff_to_save[4], data_diff_to_save[5], data_diff_to_save[6], data_diff_to_save[7], data_diff_to_save[8]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/cc_diff_metrics.csv", mode='a', header=False, index=False)


    # RQ 2
    locs = []
    llocs = []
    comments = []
    for files in data["raw_metrics"]:
        if not files:
            locs.append(0)
            llocs.append(0)
            comments.append(0)
            continue
        loc = 0 
        lloc = 0
        comment = 0
        for file in files:
            file_loc = 0 
            file_lloc = 0
            file_comment = 0
            if 'error' in files[file]:
                continue
            loc = loc + files[file]['loc']
            lloc = lloc + files[file]['lloc']
            comment = comment + files[file]['comments']
        locs.append(loc)    
        llocs.append(lloc)    
        comments.append(comment)    
    
    data_to_save = [data['repo_name'], locs[0], locs[1], locs[2], locs[3], locs[4], locs[5], locs[6], locs[7], locs[8], locs[9]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/locs_metrics.csv", mode='a', header=False, index=False)

    data_diff_to_save = calculate_diff(locs)
    data_to_save = [data['repo_name'], data_diff_to_save[0], data_diff_to_save[1], data_diff_to_save[2], data_diff_to_save[3], data_diff_to_save[4], data_diff_to_save[5], data_diff_to_save[6], data_diff_to_save[7], data_diff_to_save[8]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/locs_diff_metrics.csv", mode='a', header=False, index=False)

    data_to_save = [data['repo_name'], llocs[0], llocs[1], llocs[2], llocs[3], llocs[4], llocs[5], llocs[6], llocs[7], llocs[8], llocs[9]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/llocs_metrics.csv", mode='a', header=False, index=False)

    data_diff_to_save = calculate_diff(llocs)
    data_to_save = [data['repo_name'], data_diff_to_save[0], data_diff_to_save[1], data_diff_to_save[2], data_diff_to_save[3], data_diff_to_save[4], data_diff_to_save[5], data_diff_to_save[6], data_diff_to_save[7], data_diff_to_save[8]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/llocs_diff_metrics.csv", mode='a', header=False, index=False)

    data_to_save = [data['repo_name'], comments[0], comments[1], comments[2], comments[3], comments[4], comments[5], comments[6], comments[7], comments[8], comments[9]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/comments_metrics.csv", mode='a', header=False, index=False)

    data_diff_to_save = calculate_diff(comments)
    data_to_save = [data['repo_name'], data_diff_to_save[0], data_diff_to_save[1], data_diff_to_save[2], data_diff_to_save[3], data_diff_to_save[4], data_diff_to_save[5], data_diff_to_save[6], data_diff_to_save[7], data_diff_to_save[8]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/comments_diff_metrics.csv", mode='a', header=False, index=False)


    # RQ 3
    mis = []
    for files in data["mi_metrics"]:
        if not files:
            mis.append(0)
            continue
        release_mi = []
        for file in files:
            file_mi = 0
            if 'error' in files[file]:
                continue
            release_mi.append(files[file]['mi'])
        median = np.median(release_mi)
        if math.isnan(median):
            median = 0
        mis.append(median)  

    data_to_save = [data['repo_name'], mis[0], mis[1], mis[2], mis[3], mis[4], mis[5], mis[6], mis[7], mis[8], mis[9]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/mi_metrics.csv", mode='a', header=False, index=False)

    data_diff_to_save = calculate_diff(mis)
    data_to_save = [data['repo_name'], data_diff_to_save[0], data_diff_to_save[1], data_diff_to_save[2], data_diff_to_save[3], data_diff_to_save[4], data_diff_to_save[5], data_diff_to_save[6], data_diff_to_save[7], data_diff_to_save[8]]
    df = pd.DataFrame([data_to_save]) 
    df.to_csv(f"{PATH_SUMARIZED_METRICS}/mi_diff_metrics.csv", mode='a', header=False, index=False)
    



  



