import pandas
import requests
import json
import ast
import os
import shutil
import random
import threading
import queue
from subprocess import PIPE, Popen

# pip3 install radon

# create dir
PATH_RELEASES = "temp/releases-downloaded"
PATH_METRICS = "collected-metrics"
if not os.path.exists(PATH_RELEASES):
    os.makedirs(PATH_RELEASES)
    
if not os.path.exists(PATH_METRICS):
    os.makedirs(PATH_METRICS)

# Download release
def download_release(file_name, url, tag):
    try:
        print(f"Downloading: {url} | {tag} ---> {file_name}")
        os.system(f"git clone -b {tag} --depth 1 {url} {file_name}")
        return True
    except Exception as e:
        print(str(e))
        return False

# Run radon 
def handle_exec_thread(cmd):
    os.system(cmd)

def exec_radon(target_folder, repo_name, clean_up=True):
    print(f"Getting metrics from: [{target_folder}]")

    # files
    file_cc = f"cc_metrics_{repo_name}.json"
    file_raw = f"raw_metrics_{repo_name}.json"
    file_hal = f"hal_metrics_{repo_name}.json"
    file_mi = f"mi_metrics_{repo_name}.json"

    # cmds
    cmd_cc = f"radon cc {target_folder} --average --total-average -j > {file_cc}"
    cmd_raw = f"radon raw {target_folder} -s -j > {file_raw}"
    cmd_hal = f"radon hal  {target_folder} -j > {file_hal}"
    cmd_mi = f"radon mi  {target_folder} -j > {file_mi}"

    # threads
    thread_cc = threading.Thread(target=handle_exec_thread, args=(cmd_cc,))
    thread_raw = threading.Thread(target=handle_exec_thread, args=(cmd_raw,))
    thread_hal = threading.Thread(target=handle_exec_thread, args=(cmd_hal,))
    thread_mi = threading.Thread(target=handle_exec_thread, args=(cmd_mi,))

    # star threads
    thread_cc.start()
    thread_raw.start()
    thread_hal.start()
    thread_mi.start()

    # wait threads
    thread_cc.join()
    thread_raw.join()
    thread_hal.join()
    thread_mi.join()

    # return cc_metrics.json
    f = open(file_cc, "rt", encoding="utf-8")
    cc_data = f.read()
    f.close()

    # return raw_metrics.json
    f = open(file_raw, "rt", encoding="utf-8")
    raw_data = f.read()
    f.close()

    # return hal_metrics.json
    f = open(file_hal, "rt", encoding="utf-8")
    hal_data = f.read()
    f.close()

    # return mi_metrics.json
    f = open(file_mi, "rt", encoding="utf-8")
    mi_data = f.read()
    f.close()


    # clean up
    if clean_up:
        shutil.rmtree(target_folder, ignore_errors=True)

        try:
            os.remove(file_cc)
            os.remove(file_hal)
            os.remove(file_raw)
            os.remove(file_mi)
        except:
            print("Failed to delete random metrics!")

    return [cc_data, raw_data, hal_data, mi_data]

# Save Metrics
def save_metric(data):
    name = data["repo_name"]
    print(f"Saving Metrics: [{name}]")
    f = open(f"{PATH_METRICS}/metrics_{name}.json", "wt", encoding="utf-8")
    f.write(json.dumps(data))
    f.close()

def proc_analyseThread(queue):
    while True:
        repository = queue.get()
        
        # repository vars
        name = repository["Name"]
        url = repository["URL"]

        releases = []
        releases.append(repository["R1"])
        releases.append(repository["R2"])
        releases.append(repository["R3"])
        releases.append(repository["R4"])
        releases.append(repository["R5"])
        releases.append(repository["R6"])
        releases.append(repository["R7"])
        releases.append(repository["R8"])
        releases.append(repository["R9"])
        releases.append(repository["R10"])

        data = {
            "repo_name": name.split('/')[1],
            "cc_metrics": [],
            "raw_metrics": [],
            "hal_metrics": [],
            "mi_metrics": []
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
                
                # check if path already exists
                if os.path.exists(file_name):
                    rand1 = str(random.randint(0,999999))
                    rand2 = str(random.randint(100000,999999))
                    file_name += '_' + rand1 + "_" + rand2

                if download_release(file_name, url, release):
                    # target_folder = uncompress_release(file_name)
                    metric_json = []
                    metric_json = exec_radon(file_name, data["repo_name"])
                    data["cc_metrics"].append(json.loads(metric_json[0]))
                    data["raw_metrics"].append(json.loads(metric_json[1]))
                    data["hal_metrics"].append(json.loads(metric_json[2]))
                    data["mi_metrics"].append(json.loads(metric_json[3]))

            save_metric(data)
        queue.task_done()

# SETUP QUEUE
THREAD_COUNT = 20
poll_queue = queue.Queue()
print("[*] Thread Count:", THREAD_COUNT)
for i in range(THREAD_COUNT):
    try:
        worker = threading.Thread(target=proc_analyseThread, args=(poll_queue,))
        worker.start()
    except Exception as e:
        print(str(e))

# PUT IN QUEUE
csv = pandas.read_csv("repo_releases.csv")
for index, repository in csv.iterrows():
    poll_queue.put(repository)

# Wait Poll Threads Done!
poll_queue.join()