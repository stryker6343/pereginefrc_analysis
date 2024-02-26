Notes:

12/10/2023

The Peregrine API can be found at https://api.peregrinefrc.com/.


```python
import requests

r = requests.get("https://api.peregrinefrc.com/")
print(r.json()["uptime"])
```