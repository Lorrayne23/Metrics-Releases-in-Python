import csv
import pandas as pd
import requests
import time
from datetime import datetime
from datetime import date
import tarfile

token = 'place_token_here'

headers = {"Authorization": f"Bearer {token}"}

query = """{
  repository(owner: "repo_owner", name: "repo_name") {
    releases(first: 40, after:null) {
      pageInfo {
        endCursor
        hasNextPage
      }
      totalCount
      nodes {
        url
        releaseAssets(first: 30) {
          totalCount
          nodes {
            name
            downloadUrl
            downloadCount
          }
        }
      }
    }
  }
}
"""

def run_query(query):
  downloaded = False
  while not downloaded:
    try:
      request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
      if request.status_code == 200:
          return request.json()
      else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    except:
      time.sleep(2)
      continue

def check_releases_extension(results):
  releases = []
  for r in results:
    assets = r["releaseAssets"]["nodes"]
    for asset in assets:
      url = asset["downloadUrl"]
      if not ".sig" in url and not ".asc" in url and not ".sha512" in url:    # exclude extensions
        if "tar.gz" in url or ".zip" in url:                                # filter by tar.gz or .zip
            releases.append(url)
            break
  return releases

def save_releases(repo_owner, repo_name, releases):
  data = []
  name = repo_owner + '/' + repo_name
  data.append([name, releases[0], releases[1], releases[2], releases[3], releases[4], releases[5], releases[6], releases[7], releases[8], releases[9]])
  df = pd.DataFrame(data) 
  df.to_csv("repo_releases.csv", mode='a', header=False, index=False)

# Create file to save the data
columns = ["Name", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
df = pd.DataFrame([], columns=columns) 
df.to_csv("repo_releases.csv")
with open('repositorios_populares_python.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, quotechar='|')
  next(spamreader)
  next_page = 'null'
  has_next_page = False
  for idx, row in enumerate(spamreader):
    repository = row[1]
    repo_owner = repository.split('/')[0]
    repo_name = repository.split('/')[1]
    if idx == 0:
      query = query.replace('repo_owner', repo_owner)
      query = query.replace('repo_name', repo_name)
    else:
      query = query.replace('name: "' + old_repo_name + '"', 'name: "' + repo_name + '"')
      query = query.replace('owner: "' + old_repo_owner + '"', 'owner: "' + repo_owner + '"')
      query = query.replace('"' + next_page + '"', 'null')
    old_repo_name = repo_name
    old_repo_owner = repo_owner
    query_result = run_query(query)
    results = query_result['data']['repository']['releases']['nodes']
    
    releases = []
    releases = check_releases_extension(results)

    if len(releases) >= 10:
      save_releases(repo_owner, repo_name, releases[0:10])
      continue

    has_next_page = query_result['data']['repository']['releases']['pageInfo']['hasNextPage']
    if has_next_page:
      next_page = query_result['data']['repository']['releases']['pageInfo']['endCursor']
      query = query.replace('null', '"' + next_page + '"')

    while has_next_page and len(releases) < 10:
      old_pagination = query_result['data']['repository']['releases']['pageInfo']['endCursor']
      query_result = run_query(query)

      valid_releases = check_releases_extension(results)
      releases = releases + valid_releases
      next_page = query_result['data']['repository']['releases']['pageInfo']['endCursor']
      query = query.replace(old_pagination, next_page)
      has_next_page = query_result['data']['repository']['releases']['pageInfo']['hasNextPage']

      if len(releases) >= 10:
        save_releases(repo_owner, repo_name, releases[0:10])


