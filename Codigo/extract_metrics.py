import json
import statistics

# This code is not ready

f = open('collected-metrics\metrics_youtube-dl.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
count = 0
for files in data["metrics"]:
    complexity = []
    for file in files:
        for structure_metrics in files[file]:
            if structure_metrics['rank'] == 'A':
                complexity.append(0)
            elif structure_metrics['rank'] == 'B':
                complexity.append(1)
            elif structure_metrics['rank'] == 'C':
                complexity.append(2)
            elif structure_metrics['rank'] == 'D':
                complexity.append(3)
            elif structure_metrics['rank'] == 'E':
                complexity.append(4)
            else:
                complexity.append(5)
    mediana = statistics.median(complexity)
    print("Mediana da cc da release " + str(count) +": " + str(mediana))
    count = count + 1
    

  



