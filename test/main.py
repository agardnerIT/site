from pyscript import document
import requests


import pyodide_http

pyodide_http.patch_all()

def send_post(event):

    payload = { "foo": "bar" }
    url = "https://jsonplaceholder.typicode.com/posts/2"
    url = "https://webhook.site/b603beb6-d105-469c-91df-1c5f6e75fec0"
    url = "https://httpdump.app/dumps/179b653b-8119-4401-aa8a-2659ce265d5d"
    #response = requests.post(url, data=payload)
    response = requests.get(url)
    output_div = document.querySelector("#output")
    output_div.innerText += str(response.status_code)
    output_div.innerText += str(response.json())