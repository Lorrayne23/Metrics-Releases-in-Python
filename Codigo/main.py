import pandas as pd
import requests

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
        releases(first: 10) {
          nodes {
            url
          }
        }
      }
    }
  }
}
"""
  request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
  if request.status_code == 200:
      return request.json()
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

data = []

def save_file(result):
  results = result["data"]["search"]["nodes"]
  for r in results:
    releases = []
    name = r["nameWithOwner"]
    if len(r["releases"]["nodes"]) == 10:
        for i in r["releases"]["nodes"]:
            url = i["url"]
            releases.append(url)
    if len(releases) == 10:
        data.append([name, releases])

  columns = ["Name", "Releases"]
  df = pd.DataFrame(data, columns=columns) 
  df.to_csv("repositorios_populares_python.csv")

pages = 50
endCursor = None

for page in range(pages):
  result = run_query(endCursor)
  save_file(result)
  has_next = result["data"]["search"]["pageInfo"]["hasNextPage"]
  if not has_next:
      break
  endCursor = result["data"]["search"]["pageInfo"]["endCursor"]

