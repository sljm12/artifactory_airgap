import requests
from requests.auth import HTTPBasicAuth
import json
from pathlib import Path
import os
import datetime


output_dir = "./export"

auth = HTTPBasicAuth('admin', 'P@ssw0rd')
query = 'items.find({"type":"file","created" : {"$gt" : "2021-05-22T13:45:00+08:00"},"repo" : "maven-challenge"})'
root_url = "http://192.168.1.96:8082/artifactory"
r = requests.post(root_url+"/api/search/aql", auth=auth, data=query)
print(r.text)

j = json.loads(r.text)

latest_time = datetime.datetime.fromisoformat("2021-05-22T13:45:00+08:00")

for r in j["results"]:

    print(r["path"]+"\t"+r["created"])
    dir_path = os.path.join(output_dir, r["path"])

    full_url = root_url +"/"+r["repo"]+"/"+r["path"]+"/"+r["name"]

    response = requests.get(full_url)
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    file_path = os.path.join(dir_path, r["name"])
    Path(file_path).write_bytes(response.content)
