from textwrap import dedent
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_player as player
#import numpy as np
#import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pathlib

import os
import gc
import json
import requests
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from elasticsearch_dsl.query import Bool, MultiMatch, Q
from elasticsearch_dsl.search import Search, MultiSearch
from elasticsearch_dsl import Mapping, Keyword, Nested, Text
from elasticsearch_dsl import Index, analyzer, tokenizer
import glob
import cv2
from matplotlib import pyplot as plt

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True

images_div = []

res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
client = Elasticsearch()

def query_images(object_list):
    hit1 = set()
    image_set = set()
    print("11. object_list =", object_list)
    
    QI = Q('match_all')
    s1 = Search(index='idxo20')
    for objectk in object_list:
        print("objectk= ",objectk)
        QI = QI & Q("match", names=objectk)

    s1 = s1.query(QI).using(client)
    s1.execute()
    for hit in s1.scan() :
        print("33 ", hit.imgfile)
        image_set.add(hit.imgfile)
    print("image_set = {0}".format(image_set))
    im = 0

    for image in image_set :
        if im > 3 : 
            break
        file, ext = os.path.splitext(image)
        image = file + '.png'
        print("66 image =", image)
        images_div.append(display_image(image))
        im = im + 1
    print("Please hit refresh...")


def no_images_msg():
    return html.div([
            html.Output(id='no_images', value="No images found")
    ])

def display_image(image):
    return html.Div(
        html.A(
            html.Img(
                src = app.get_asset_url(image)#,
				#style={'display':'block'}
           ) )
    )



def serve_layout():
    return html.Div(    
		children=[
		    dcc.Interval(id="interval-updating-images", interval=1000, n_intervals=0),
		    html.Div(
		        className="container",
		        children=[
		            html.Div(
		                id="left-side-column",
		                className="eight columns",
		                children=[
		                    html.Img(
		                        id="logo-mobile", src=app.get_asset_url("dash-logo.png")
		                    ),
		                    html.Label('Objects in Image'),
		                    html.Div([
		                        html.Div(dcc.Input(id="Objects-in-image", value="man",type='text')),                       
		                        html.Button( children="Fetch Images", id="fetch-images",  n_clicks=0),
		                        html.Div(id='output', children='Enter comma separated values and press Fetch Images'),
		                        html.Button( children="Clear Images", id="clear-images", n_clicks=0),
								html.Div(id='output-clear-button', children='placeholder-clear'),
		                        #html.Div(no_images_div, id='no-images'),
		                        html.Div(images_div, id='disp-images' ),
		                    ]),
		                ],
		            ),
		        ],
		    ),
		]
)

app.layout = serve_layout

@app.callback(Output('output', 'children'),
             [Input('fetch-images', 'n_clicks')],
              [State('Objects-in-image', 'value')])
def fetch_images(n_clicks, value):
    if n_clicks > 0:
        n_clicks = 0
        print("value=", value)
        object_list = value.split(',')
        print("22. object_list=",object_list)
        query_images(object_list)

@app.callback(Output('output-clear-button', 'children'),
             [Input('clear-images', 'n_clicks')] )
def clear_images(n_clicks):
    if n_clicks > 0:
        n_clicks = 0
        images_div = [html.Div(html.A(href='http://localhost:8053') )]
        print("In clear_images")

    

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8053)
