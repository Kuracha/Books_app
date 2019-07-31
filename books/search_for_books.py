import os
import requests
import json


def search(value):
        googleapikey = "AIzaSyBjejFtcCA45MzR6MefoA7XbH6bGx9gBAc"
        params = {"q":value, 'key':googleapikey}
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=params)
        rj = r.json()
        rr =rj['items']
        return rr





print(search("Harry Potter"))