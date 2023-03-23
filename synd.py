from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    with open("feed/rss.xml",'r') as g:
        feed = g.read()
    return feed

if __name__ == '__main__':
    app.run()