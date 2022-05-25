import csv
import pandas as pd
import requests
import time
from datetime import datetime
from datetime import date
import tarfile

token = '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'

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
        tagName
        createdAt
      }
    }
    url
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
      print("Failed to query!")
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

def save_releases(repo_owner, repo_name, url, releases):
  data = []
  name = repo_owner + '/' + repo_name
  data.append([name, url, releases[0], releases[1], releases[2], releases[3], releases[4], releases[5], releases[6], releases[7], releases[8], releases[9]])
  df = pd.DataFrame(data) 
  df.to_csv("repo_releases.csv", mode='a', header=False, index=False)

def save_releases_date(repo_owner, repo_name, url, createdAt):
  data = []
  name = repo_owner + '/' + repo_name
  data.append([name, url, createdAt[0], createdAt[1], createdAt[2], createdAt[3], createdAt[4], createdAt[5], createdAt[6], createdAt[7], createdAt[8], createdAt[9]])
  df = pd.DataFrame(data) 
  df.to_csv("repo_releases_created_date.csv", mode='a', header=False, index=False)

# Create file to save the data
columns = ["Name", "URL", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]
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
    print(f'Repository: {repo_name}')
    query_result = run_query(query)
    results = query_result['data']['repository']['releases']['nodes']
    url = query_result['data']['repository']['url']
    
    releases = []
    createdAt = []
    for r in results:
      releases.append(r["tagName"])
      createdAt.append(r["createdAt"])

    # releases = check_releases_extension(results)

    if len(releases) >= 10:
      save_releases(repo_owner, repo_name, url, releases[0:10])
      save_releases_date(repo_owner, repo_name, url, createdAt[0:10])
      continue

    # has_next_page = query_result['data']['repository']['releases']['pageInfo']['hasNextPage']
    # if has_next_page:
    #   next_page = query_result['data']['repository']['releases']['pageInfo']['endCursor']
    #   query = query.replace('null', '"' + next_page + '"')

    # while has_next_page and len(releases) < 10:
    #   old_pagination = query_result['data']['repository']['releases']['pageInfo']['endCursor']
    #   query_result = run_query(query)

    #   valid_releases = check_releases_extension(results)
    #   releases = releases + valid_releases
    #   next_page = query_result['data']['repository']['releases']['pageInfo']['endCursor']
    #   query = query.replace(old_pagination, next_page)
    #   has_next_page = query_result['data']['repository']['releases']['pageInfo']['hasNextPage']

    #   if len(releases) >= 10:
    #     save_releases(repo_owner, repo_name, releases[0:10])


