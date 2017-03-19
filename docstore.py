from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

def ds_startup():
    pass

if __name__ == '__main__':
    print('dentro')
    # app.run()
