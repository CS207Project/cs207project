from webutils import WebClient
import matplotlib.pyplot as plt
import json

# w = WebClient('http://localhost:8080')
w = WebClient('http://www.adjch.me:8080')

# these work
# print(w.select().content)
# print(w.select({'order':1}).content)
print(w.select({'order':{'>=':1}},['pk','order']).content)


# this one doesn't.
# might just be that sorting by primary key is not being supproted
# print(w.select({'order':{'>=':1}},['pk','order'],{'sort_by':'+pk'}).content)
