from flask import Flask
import sqlite3
import os
import hashlib
import shutil
import time

app = Flask(__name__)

@app.route('/get_all_docs')
def get_all_docs():
    
    return 'Hello World!'

config = {}
docs = {}

def df_create_db(db_filename, docs_root, docs_src):
    '''Create initial database with the files in docs_src. If file db_filename alreary exists, raise an exception. Also, move files from docs_src to docs_root, renaming them to their sha256 hashes
    '''

    if os.path.exists(db_filename):
        raise(Exception('Database file already exists'))
    
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # cur.execute('DROP TABLE IF EXISTS docs')
    # cur.execute('DROP TABLE IF EXISTS tags')
    # cur.execute('DROP TABLE IF EXISTS xref_docs_tags')

    cur.execute('CREATE TABLE docs (id integer PRIMARY KEY, name text, hash text, date_added integer)')
    cur.execute('CREATE TABLE tags (id integer PRIMARY KEY, desc text)')
    cur.execute('CREATE TABLE xref_docs_tags (doc_id integer, tag_id integer)')

    for fname, fpath in read_files(docs_src):
        fhash = hashlib.sha256(open(fpath, 'rb').read()).hexdigest()
        hashpath = '{}/{}'.format(config['docs_root'], fhash)
        # print('{} --> {}'.format(fpath, hashpath))
        shutil.copyfile(fpath, '{}/{}'.format(docs_root, fhash))
        cur.execute('INSERT INTO docs (name, hash, date_added) VALUES (?,?,?)', (fname, fhash, int(time.time())))

    conn.commit()
    conn.close()

def read_files(d):
    '''Read all files from directory d and return a list with the filenames'''
    files = []
    for f in os.scandir(d):
        fname = f.name
        fpath = '{}/{}'.format(d, fname)
        if f.is_file():
            files.append((fname, fpath))
        elif f.is_dir():
            files.extend(read_files('{}'.format(fpath)))
    return (files)

def ds_read_db(db_filename):
    '''Read the database into the main dicts'''

    if not os.path.exists(db_filename):
        raise(Exception('Database file not found.'))
    
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    docs = {}
    for f in cur.execute('SELECT * FROM docs'):
        docs[f[0]] = {'name': f[1],
                      'hash': f[2],
                      'added': f[3]}

    conn.close()
    
    print(docs)

    

def ds_config():
    '''Set the config parameters into the config dict'''
    config['db_filename'] = 'docs.db'
    config['docs_root'] = './docs'
    config['docs_src'] = './src'
    config['db'] = sqlite3.connect[config['db_filename']]

def ds_exit():
    config['db'].close()

if __name__ == '__main__':
    ds_config()
    # df_create_db(config['db_filename'],
    #              config['docs_root'],
    #              config['docs_src'])
    
    # ds_read_db(config['db_filename'])
    
    app.run()
    ds_exit()
    
