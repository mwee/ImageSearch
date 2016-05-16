from app import db

class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    image_url = db.Column(db.String())

    keyword_relevances = db.relationship("KeywordRelevance", back_populates='image')

    def __init__(self, url, image_url):
        self.url = url
        self.image_url = image_url

    def __repr__(self):
        return '<id: {}, url: {}, image_url: {}>'.format(self.id, self.image_url)

class KeywordRelevance(db.Model):
    __tablename__ = 'keyword_relevance'

    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String())
    relevance = db.Column(db.Float())

    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    image = db.relationship("Image", back_populates='keyword_relevances')

    def __init__(self, keyword, relevance):
        self.keyword = keyword
        self.relevance = relevance

    def __repr__(self):
        return '<id: {}, relevance: {}>'.format(self.id, self.keyword, self.relevance)
