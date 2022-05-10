import json
import statistics
import os
import pandas as pd

PATH_SUMARIZED_METRICS = "sumarized-metrics"
if not os.path.exists(PATH_SUMARIZED_METRICS):
    os.makedirs(PATH_SUMARIZED_METRICS)

columns = ["Name", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
df = pd.DataFrame([], columns=columns) 
df.to_csv(f"{PATH_SUMARIZED_METRICS}/cc_metrics.csv")

# This code is not ready
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
    if not data['cc_metrics'][0]:
        continue
    count = 0
    repo_name = data['repo_name']
    complexitys = []
    for files in data["cc_metrics"]:
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
    
    # mediana = statistics.median(complexity_rank)
    # print("Mediana da cc da release " + str(count) +": " + str(mediana))
    # count = count + 1



  



