import requests
from threading import Thread
import json
import os

class Dict(dict):
  def __init__(self,*args,**kwargs):
    super().__init__(*args,**kwargs)
    self.__dict__ = self

class tsbAPI:
  def __init__(self):
    self.repo_url = "https://api.github.com/repos/ProjectTSB/TheSkyBlessing"
    self.releases = {}
    
  def fetch_release(self):
    """実行時点のリリース一覧を取得します

    Returns: Dict
    """
    resp = requests.get(self.repo_url)
    r = resp.json()
    
    resp = requests.get(r["releases_url"][:-5])
    #r = resp.json()
    for r in resp.json():
      for i in r["assets"]:
        if i["browser_download_url"].split("/")[-1] == "TheSkyBlessing.zip":
          download_url = i["browser_download_url"]
      self.releases[r["tag_name"]] = {
        "name": r["name"],
        "body": r["body"],
        "size": r["assets"][0]["size"],
        "download_url": download_url
        }
    return self.releases
    
  def get_release(self):
    """最後に取得したリリース一覧を返します

    Returns: dict
    """
    return self.releases if self.releases else self.fetch_release()


class mojangAPI:
  def __init__(self):
    self.manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
    self.releases = {}

  
  def _get_server(self,version,version_url):
    resp = requests.get(version_url)
    server = resp.json()["downloads"]["server"]["url"]
    self.releases[version] = server


  def fetch_release(self):
    """実行時点のリリース一覧を取得します

    Returns: dict
    """
    resp = requests.get(self.manifest_url)
    r = resp.json()

    for i in r["versions"]:
      if i["type"] == "release":
        if i["id"] == "1.7.9":
          break
        self.releases[i["id"]] = None
        th = Thread(target=(self._get_server),args=(i["id"],i["url"]))
        th.start()
    th.join()
    return self.releases

  def get_release(self):
    """最後に取得したリリース一覧を返します

    Returns: dict
    """
    return self.releases if self.releases else self.fetch_release()
  



"""
api = tsbAPI()
api.get_release()
for k,v in api.releases.items():
  print(k)
  print(v)
"""

"""
mj = mojangAPI()
print("\n".join(k+" "+v for k,v in mj.fetch_release().items()))
"""