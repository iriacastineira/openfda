import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.github.com")
conn.request("GET", "/orgs/elastic/repos", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
for i in range(len(repos)):
    repo = repos[i]
    print("The name of the repositories is", repo['name'])                   