import requests
import json
import os


class tsbAPI:
  def __init__(self):
    self.repo_url = "https://api.github.com/repos/ProjectTSB/TheSkyBlessing"
    self.releases = {}
    
  def fetch_release(self):
    """実行時点のリリース一覧を取得します

    Returns: dict
    """
    resp = requests.get(self.repo_url)
    r = resp.json()
    
    resp = requests.get(r["releases_url"][:-5])
    #r = resp.json()
    for r in resp.json():
      self.releases[r["tag_name"]] = {
        "name": r["name"],
        "body": r["body"],
        "download_url": r["assets"][0]["browser_download_url"]
        }
    return self.releases
    
  def get_release(self):
    """最後に取得した辞書を返します

    Returns: dict
    """
    return self.releases if self.releases else self.fetch_release()

api = tsbAPI()
api.get_release()
for k,v in api.releases.items():
  print(k)
  print(v)






