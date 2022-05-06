import pandas as pd
import requests
import time
from datetime import datetime
from datetime import date

token = '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'

headers = {"Authorization": f"Bearer {token}"}

def calculate_repo_age(create_date):
  today = date.today()
  create_date = create_date.split("T", 1)
  create_date = datetime.strptime(create_date[0], '%Y-%m-%d').date()
  delta = today - create_date
  age = delta.days/360
  i, d = divmod(age, 1)
  return i

def run_query(cursor):
    f_cursor = "null" if cursor is None else "\"" + cursor + "\""
    query = """{
  search(
    query: "language:python, stars:>1"
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
        createdAt
        stargazers {
          totalCount
        }
        releases {
          totalCount
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
    name = r["nameWithOwner"]
    if r['releases']['totalCount'] >= 10:
      stargazers = r['stargazers']['totalCount']
      age = calculate_repo_age(r['createdAt'])
      num_of_releases = r['releases']['totalCount']

      data.append([name, stargazers, age, num_of_releases])

    columns = ["Name", "Stargazers", "Age", "Num_of_Releases"]
    df = pd.DataFrame(data, columns=columns) 
    df.to_csv("repositorios_populares_python.csv")

pages = 1500
endCursor = None
for page in range(pages):
    result = run_query(endCursor)
    save_file(result)
    has_next = result["data"]["search"]["pageInfo"]["hasNextPage"]
    if not has_next:
        break
    endCursor = result["data"]["search"]["pageInfo"]["endCursor"]

