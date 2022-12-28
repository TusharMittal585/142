from flask import Flask, jsonify, request
from content_filtering import get_recommendations
from storage import all_articles,liked_articles,did_not_read,not_liked_articles
from demographic_filtering import output

app = Flask(__name__)

@app.route("/get-movie")
def get_articles():
    article_data = {
        "title": all_articles[0][19],
        "poster_link": all_articles[0][27],
        "rating": all_articles[0][20],
        "overview": all_articles[0][9]
    }
    return jsonify({
        "data": article_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-article", methods=["POST"])
def unliked_article():
    article = all_articles[0]
    not_liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/did-not-read", methods=["POST"])
def did_not_read():
    article = all_articles[0]
    did_not_read.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-articles")
def popular_articles():
    article_data = []
    for article in output:
        _d = {
            "title": article[0],
            "rating": article[4],
            "overview": article[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200

@app.route("/recommended-articles")
def recommended_articles():
    all_recommended = []
    for liked_article in liked_article:
        output = get_recommendations(liked_article[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    article_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        article_data.append(_d)
    return jsonify({
        "data": article_data,
        "status": "success"
    }), 200 

if __name__ == "__main__":
  app.run()