import pandas
import requests
import io
import json
import ast
import os
import shutil
from subprocess import PIPE, Popen

# pip3 install radon

# read csv
csv = pandas.read_csv("repositorios_populares_python.csv")

# create dir
PATH_RELEASES = "temp/releases-downloaded"
PATH_METRICS = "collected-metrics"
if not os.path.exists(PATH_RELEASES):
    os.makedirs(PATH_RELEASES)
    
if not os.path.exists(PATH_METRICS):
    os.makedirs(PATH_METRICS)

# Download release
def download_release(file_name, url):
    try:
        print(f"Downloading: {url} ---> {file_name}")
        data = requests.get(url, stream=True)
        with open(file_name, "wb") as file:
            file.write(data.content)
        return True
    except Exception as e:
        print(str(e))
        return False

# Uncompress file
def uncompress_release(file_name, clean_up=True):
    # support .zip, .tar, .gztar, .bztar, .xztar
    shutil.unpack_archive(file_name, PATH_RELEASES)

    # remove packed file.
    if clean_up:
        os.remove(file_name)

    # return folder name
    return os.listdir(PATH_RELEASES)[0]

# Run radon 
def exec_radon(target_folder, clean_up=True):
    print(f"Getting metrics from: [{target_folder}]")
    os.system(f"radon cc {PATH_RELEASES}/{target_folder} -j > metrics.json")

    # return metrics.json
    f = open("metrics.json", "rt", encoding="utf-8")
    data = f.read()
    f.close()

    # clean up
    if clean_up:
        shutil.rmtree(f"{PATH_RELEASES}/{target_folder}", ignore_errors=True)
        # os.remove("metrics.json")
    return json.loads(data)

# Save Metrics
def save_metric(data):
    name = data["repo_name"]
    print(f"Saving Metrics: [{name}]")
    f = open(f"{PATH_METRICS}/metrics_{name}.json", "wt", encoding="utf-8")
    f.write(json.dumps(data))
    f.close()



# main
for index, repository in csv.iterrows():
    name = repository["Name"]
    releases = ast.literal_eval(str(repository["Releases"]).strip('"'))

    data = {
        "repo_name": name.split('/')[1],
        "metrics": []
    }

    # check if metric is already collected ...
    if not os.path.exists(f"{PATH_METRICS}/metrics_{data['repo_name']}.json"):
        # download releases;
        # uncompress;
        # execute radon;
        # add to metrics lists;
        # save metrics;
        for release in releases:
            file_name = PATH_RELEASES + "/" + release.split('/')[-1]
            if download_release(file_name, release):
                target_folder = uncompress_release(file_name)
                metric_json = exec_radon(target_folder)
                data["metrics"].append(metric_json)

        save_metric(data)