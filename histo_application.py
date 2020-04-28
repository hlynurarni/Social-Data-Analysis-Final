# CSV 2 flare.json
# convert a csv file to flare.json for use with many D3.js viz's
# This script creates outputs a flare.json file with 2 levels of nesting.
# For additional nested layers, add them in lines 32 - 47
# sample: http://bl.ocks.org/mbostock/1283663

# author: Andrew Heekin
# MIT License

import pandas as pd
import json


df = pd.read_csv('fire_incidents1year.csv')


# choose columns to keep, in the desired nested json hierarchical order
df = df[["IncGeo_BoroughName", "WardName", "IncidentNumber"]]


# order in the groupby here matters, it determines the json nesting
# the groupby call makes a pandas series by grouping 'the_parent' and 'the_child', while summing the numerical column 'child_size'
df1 = df.groupby(['IncGeo_BoroughName', 'WardName'])['IncidentNumber'].sum()
df1 = df1.reset_index()


# start a new flare.json document
flare = dict()
flare = {"name":"flare", "children": []}


for line in df1.values:
    the_parent = line[0]
    the_child = line[1]
    child_size = line[2]

    # make a list of keys
    keys_list = []
    for item in d['children']:
        keys_list.append(item['name'])

    # if 'the_parent' is NOT a key in the flare.json yet, append it
    if not the_parent in keys_list:
        d['children'].append({"name":the_parent, "children":[{"name":the_child, "size":child_size}]})

    # if 'the_parent' IS a key in the flare.json, add a new child to it
    else:
        d['children'][keys_list.index(the_parent)]['children'].append({"name":the_child, "size":child_size})

flare = d


# export the final result to a json file
with open('flare.json', 'w') as outfile:
    json.dump(flare, outfile)