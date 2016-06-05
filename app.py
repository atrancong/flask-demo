from flask import Flask, render_template, request, redirect

app = Flask(__name__)

import requests
import simplejson as json
import pandas as pd
from bokeh.plotting import figure, output_notebook, save, output_file

def stock_plot(stock_code):
    r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/{}/data.json?column_index=4&api_key=DVNk9TzytJe4BP47knTW'.format(stock_code))
    parsed_json = json.loads(r.text)
    data = parsed_json['dataset_data']['data']
    df = pd.DataFrame(data, columns=['date','closing_price'])
    df['date']=pd.to_datetime(df['date'])
    p = figure(width=800, height=250, x_axis_type="datetime")
    p.line(df['date'], df['closing_price'], color='navy', alpha=0.5)
    output_file('templates/bokeh_graph.html')
    return save(p)

app.vars={}

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars['stock_code'] = request.form['stock_code']
        stock_plot(app.vars['stock_code'])
        return render_template('bokeh_graph.html') #, stock_code=app.vars['stock_code']

if __name__ == '__main__':
      app.run()
