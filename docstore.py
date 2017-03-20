from flask import Flask, jsonify
import sqlite3
import os
import hashlib
import shutil
import time
import json

app = Flask(__name__)
config = {}

@app.route('/get_all_docs')
def get_all_docs():
    cur = config['db'].cursor()
    docs = []
    for doc in cur.execute('SELECT * FROM docs').fetchall():
        d = {'id': doc[0],
             'fname': doc[1],
             # 'fhash': doc[2],
             'fdate': doc[3],
             'tags': []}

        for tag in cur.execute('SELECT * FROM xref_docs_tags WHERE doc_id = :doc_id', {'doc_id': d['id']}).fetchall():
            d['tags'].append(tag[1])

        docs.append(d)

    return jsonify(docs)

def ds_config():
    '''Set the config parameters into the config dict'''
    config['db_filename'] = 'docs.db'
    config['docs_root'] = './docs'
    # config['docs_src'] = './src'
    config['db'] = sqlite3.connect(config['db_filename'])

def ds_exit():
    print('Exiting...')
    config['db'].close()

if __name__ == '__main__':
    ds_config()
    app.run()
    ds_exit()
    
