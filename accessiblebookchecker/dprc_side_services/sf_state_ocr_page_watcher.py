import requests, bs4


new_request = requests.get("https://www2.ed.gov/about/offices/list/ocr/docs/investigations/open-investigations/dis1.html?queries%5Bstate%5D=CA&queries%5Bsearch%5D=san+francisco+state&perPage=50&sorts%5Bdate%5D=1")
print(new_request.content)