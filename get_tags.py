from clarifai.client import ClarifaiApi
import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import Image, KeywordRelevance

import traceback


# http://stackoverflow.com/questions/6710834/iterating-over-list-or-single-element-in-python
def get_list(x):
    if isinstance(x, list):
        return x
    else:
        return [x]


def populate_database():
    clarifai_api = ClarifaiApi()

    with open('imagespider/items.json') as data_file:
        data = json.load(data_file)

    engine = create_engine('postgresql://localhost/image_search_engine', echo=True)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    for url_dict in data[:100]:
        url = url_dict['url']
        image_url = url_dict['image_url']
        if image_url[0] == '/':
            image_url = 'http:' + image_url

        image = Image(url=url, image_url=image_url)

        try:
            result = clarifai_api.tag_image_urls(image_url)
            classes_list = get_list(result['results'][0]['result']['tag']['classes'][0])
            probs_list = get_list(result['results'][0]['result']['tag']['probs'][0])
            print(classes_list, type(classes_list))
            for tag, relevance in list(zip(classes_list, probs_list)):
                print(tag, type(tag))
                keyword_relevance = KeywordRelevance(keyword=tag, relevance=relevance)
                image.keyword_relevances.append(keyword_relevance)

                session.add(keyword_relevance)
        except:
            print image_url
            print url
            traceback.print_exc()
            continue

    session.commit()

if __name__ == '__main__':
    populate_database()
