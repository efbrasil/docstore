import sqlite3
import os
import hashlib
import shutil
import time
import sys

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

def ds_create_db(db_filename, docs_root, docs_src):
    '''Create initial database with the files in docs_src. If file db_filename alreary exists, raise an exception. Also, move files from docs_src to docs_root, renaming them to their sha256 hashes
    '''

    if os.path.exists(db_filename):
        raise(Exception('Database file already exists'))

    if not os.path.exists(docs_root):
        os.makedirs(docs_root)
        
    if not os.path.isdir(docs_root):
        raise(Exception('docs_root already exists and it\'s not a directory'))
    
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    # cur.execute('DROP TABLE IF EXISTS docs')
    # cur.execute('DROP TABLE IF EXISTS tags')
    # cur.execute('DROP TABLE IF EXISTS xref_docs_tags')

    cur.execute('CREATE TABLE docs (id integer PRIMARY KEY, name text, hash text, date_added integer)')
    cur.execute('CREATE TABLE tags (id integer PRIMARY KEY, desc text)')
    cur.execute('CREATE TABLE xref_docs_tags (doc_id integer, tag_id integer)')

    if os.path.isdir(docs_src):
        for fname, fpath in read_files(docs_src):
            fhash = hashlib.sha256(open(fpath, 'rb').read()).hexdigest()
            hashpath = '{}/{}'.format(docs_root, fhash)
            # print('{} --> {}'.format(fpath, hashpath))
            shutil.copyfile(fpath, '{}/{}'.format(docs_root, fhash))
            cur.execute('INSERT INTO docs (name, hash, date_added) VALUES (?,?,?)', (fname, fhash, int(time.time())))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    db_filename = './docs.db'
    docs_root = './docs'
    docs_src = './src'
    
    ds_create_db(db_filename, docs_root, docs_src)
    
    
