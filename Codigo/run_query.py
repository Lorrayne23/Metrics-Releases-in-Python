import pandas as pd
import requests
import time

token = input("Entre com seu token: ")

headers = {"Authorization": f"Bearer {token}"}

def run_query(cursor):
    f_cursor = "null" if cursor is None else "\"" + cursor + "\""
    query = """{
  search(
    query: "language:python, stars:>100"
    type: REPOSITORY
    first: 20
    after: """ + f_cursor + """
  ) {
    pageInfo {
      endCursor
      hasNextPage
    }
    nodes {
      ... on Repository {
        nameWithOwner
        releases(first: 50) {
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
  }
}
"""
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

data = []
def save_file(result):
  results = result["data"]["search"]["nodes"]
  for r in results:
    releases = []
    name = r["nameWithOwner"]
    for i in r["releases"]["nodes"]:
        assets = i["releaseAssets"]["nodes"]
        for asset in assets:
            url = asset["downloadUrl"]
            if not ".sig" in url and not ".asc" in url and not ".sha512" in url:    # exclude extensions
                if "tar.gz" in url or ".zip" in url:                                # filter by tar.gz or .zip
                    releases.append(url)
                    break

    if len(releases) >= 10:
        data.append([name, releases[0:10]])

    columns = ["Name", "Releases"]
    df = pd.DataFrame(data, columns=columns) 
    df.to_csv("repositorios_populares_python.csv")

pages = 1000
endCursor = None
for page in range(pages):
    result = run_query(endCursor)
    save_file(result)
    has_next = result["data"]["search"]["pageInfo"]["hasNextPage"]
    if not has_next:
        break
    endCursor = result["data"]["search"]["pageInfo"]["endCursor"]

