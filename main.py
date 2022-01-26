from flask import Flask, render_template,request, redirect, request
import pandas as pd
import datetime

df2 = pd.read_csv("C:\\Users\\Josh\\Desktop\\cs437p1\\project_1_AOL_query_log\\Clean-Data-01.txt",sep='\t')
df2 = df2.append(pd.read_csv("C:\\Users\\Josh\\Desktop\\cs437p1\\project_1_AOL_query_log\\Clean-Data-02.txt",sep='\t'))
df2 = df2.append(pd.read_csv("C:\\Users\\Josh\\Desktop\\cs437p1\\project_1_AOL_query_log\\Clean-Data-03.txt",sep='\t'))
df2 = df2.append(pd.read_csv("C:\\Users\\Josh\\Desktop\\cs437p1\\project_1_AOL_query_log\\Clean-Data-04.txt",sep='\t'))
df2 = df2.append(pd.read_csv("C:\\Users\\Josh\\Desktop\\cs437p1\\project_1_AOL_query_log\\Clean-Data-05.txt",sep='\t'))
df2["Query"] = df2["Query"].astype(str)
df2["QueryTime"]= pd.to_datetime(df2["QueryTime"])
print("Initialization Complete!")

app = Flask(__name__)
from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/ajax', methods = ['POST'])
def returnHome():
    print("homeeee")
    return redirect("index.html")

@app.route('/suggest', methods = ['POST'])
def suggest():
    """Returns new df with queries that start with the query parameter. Sorted by frequency, excludes exact match."""
    query = request.form['myQuery']
    sg = df2.loc[df2['Query'].str.startswith(query)]
    sg = sg[sg['Query'] != query]
    sg = sg.groupby(['Query']).size().reset_index(name='freq')
    sg = sg.sort_values(by=['freq'],ascending=False)
    data_dict = sg.head(5).to_dict()
    return data_dict['Query']

def build_results(data):
    sorted_dict = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
    results = {}
    for key in sorted_dict:
        results[key] = {"content":df['content'][key-1], "title":df['title'][key-1]}
    return results

@app.route('/results')
def results(query):
    print("resultsss", query)
    list_of_cannidates, clean_query = getResults(query,inverted_index)
    unsorted_dictionary_of_doc_probs = ranking(clean_query, list_of_cannidates, inverted_index)
    results = build_results(unsorted_dictionary_of_doc_probs)
    return render_template("results.html", query=clean_query, results = results, number_of_results = len(results))

@app.route('/', methods=['POST'])
def getQuery():
    query = request.form['myQuery']
    return results(query)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5505)