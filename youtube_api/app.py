import sqlite3  # Standardbibliothek, sollte immer zuerst importiert werden
import pandas as pd
from flask import Flask, request, render_template, jsonify
import os

app = Flask(__name__)

dirname = os.path.dirname(__file__)
DB_PATH = os.path.join(dirname, 'data/euro_2024_videos.db')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/')
def data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query('SELECT * FROM videos', conn)
    conn.close()
    html_table = df.to_html(classes='data', escape=False, index=False)
    return render_template('data.html', tables=html_table, titles=df.columns.values)

@app.route('/channels/')
def channels():
    conn = sqlite3.connect(DB_PATH)
    df_channels = pd.read_sql_query('SELECT DISTINCT channel_title FROM videos', conn)
    conn.close()
    channels = df_channels['channel_title'].tolist()
    return render_template('channels.html', channels=channels)


@app.route('/channel_videos/', methods=['POST'])
def channel_videos():
    channel_title = request.form.get('channel_title')
    conn = sqlite3.connect(DB_PATH)
    df_videos = pd.read_sql_query('SELECT * FROM videos WHERE channel_title = ?', conn, params=(channel_title,))
    conn.close()
    html_table = df_videos.to_html(classes='data', escape=False, index=False)
    return render_template('channel_videos.html', tables=html_table, titles=df_videos.columns.values, channel_title=channel_title)


@app.route('/diagrams/')
def diagrams():
    return render_template('diagrams.html')

if __name__ == '__main__':
    app.run(debug=True)