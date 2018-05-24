import urllib.request
from html.parser import HTMLParser

site = "https://ieeexplore.ieee.org/document/4018419/"

with urllib.request.urlopen(site) as response:
   html = response.read()

texto = html.decode("utf-8")
abs = '"abstract":'
inicio = texto.find(abs)

subtexto = texto[inicio:]

ss = subtexto.split('"')

print( ss[3] )
print( inicio)

