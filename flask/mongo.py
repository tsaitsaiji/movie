from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# 連接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DBS']
ratings_collection = db['ratings']

class MovieRating:
    def __init__(self, title, director, actors, release_date, rating):
        self.title = title
        self.director = director
        self.actors = actors
        self.release_date = release_date
        self.rating = rating

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/rate', methods=['POST'])
def rate_movie():
    title = request.form.get('title')
    director = request.form.get('director')
    actors = request.form.get('actors')
    release_date = request.form.get('release_date')
    rating = int(request.form.get('rating'))

    # 將評分存儲到 MongoDB
    ratings_collection.insert_one({
        'title': title,
        'director': director,
        'actors': actors,
        'release_date': release_date,
        'rating': rating
    })

    # 取得所有評分
    ratings = list(ratings_collection.find())
    return render_template('index.html', ratings=ratings, new_rating=MovieRating(title, director, actors, release_date, rating))

@app.route('/movies')
def index():
    # 獲取所有評分
    ratings = list(ratings_collection.find())
    return render_template('index.html', ratings=ratings)

if __name__ == '__main__':
    app.run(debug=True)