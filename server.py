from flask import Flask
from bm25 import BM25
from flask import jsonify, request
app = Flask(__name__)

@app.route('/help')
def help():
    return 'This is Help! :D'

@app.route('/idf', methods=['GET'])
def idf():
    word = request.args.get('word')
    bm25 = BM25()
    result = dict()
    result['word'] = word
    result['idf'] = bm25.idf(word)
    return jsonify(result)

@app.route('/search', methods=['GET'])
def search():
    word = request.args.get('q')
    bm25 = BM25()
    results = bm25.search(word)[:100]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
