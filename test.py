import json

with open("releases.json",mode="r",encoding="utf-8") as f:
  j = json.load(f)
  print(j[0][""])