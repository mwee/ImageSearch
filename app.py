from collections import defaultdict, OrderedDict

from flask import Flask, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import select, create_engine, desc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route('/')
def hello_world():
    return render_template('search.html')

@app.route('/search')
def search():
    arg_keywords = request.args.get('keywords')
    keywords = arg_keywords.split(' ')

    engine = create_engine('postgresql://localhost/image_search_engine', echo=True)
    conn = engine.connect()

    image_results_relevance = defaultdict(float)
    for keyword in keywords:
        s = select([KeywordRelevance]).where(KeywordRelevance.keyword.contains(keyword)). \
            order_by(desc(KeywordRelevance.relevance)).limit(100)
        result = conn.execute(s)

        for row in result:
            relevance = row[2]
            image_id = row[3]
            s = select([Image]).where(Image.id == image_id)
            result = conn.execute(s)
            image = result.fetchone()
            hash_tuple = (image[1], image[2])
            image_results_relevance[hash_tuple] += relevance

    od = OrderedDict(sorted(image_results_relevance.items(), reverse=True, key=lambda t: t[1]))

    return render_template('results.html', results=od.keys())

if __name__ == '__main__':
    app.run(debug=True)
