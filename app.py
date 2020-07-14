import os
from datetime import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env 

app = Flask(__name__)

app.config["MONGODB_NAME"] = "odd_dog"
app.config["MONGO_URI"] = os.environ.get('MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/discussions')
def discussions():
    all_categories = mongo.db.categories.find()
    comments = mongo.db.comments.find()
    return render_template('discussions.html', comments=comments, 
                           now=datetime.now().strftime("%D, %H:%M"),
                           categories=all_categories)


@app.route('/health')
def health():
    image = url_for('static', filename='images/yorkshire-terrier.jpg')
    comments = mongo.db.comments.find({'category_name': 'Health'})
    return render_template('filtering.html', comments=comments, image=image)


@app.route('/lifestyle')
def lifestyle():
    image = url_for('static', filename='images/man-with-dog.jpg')
    comments = mongo.db.comments.find({'category_name': 'Lifestyle'})
    return render_template('filtering.html', comments=comments, image=image)


@app.route('/story')
def story():
    image = url_for('static', filename='images/dog-gang.jpg')
    comments = mongo.db.comments.find({'category_name': 'Story'})
    return render_template('filtering.html', comments=comments, image=image)


@app.route('/food')
def food():
    image = url_for('static', filename='images/black-and-white-dalmatian.jpg')
    comments = mongo.db.comments.find({'category_name': 'Food'})
    return render_template('filtering.html', comments=comments, image=image)


@app.route('/goodboy')
def goodboy():
    image = url_for('static', filename='images/man-training-a-rottweiler.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     'How to turn a bad pooch into a good boy.'})
    return render_template('blogpost.html', 
                           blog_articles=blog_articles, image=image)


@app.route('/badbreath')
def badbreath():
    image = url_for('static', filename='images/english-bulldog.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     "Is your dogs bad breath doggin' you?"})
    return render_template('blogpost.html', 
                           blog_articles=blog_articles, image=image)


@app.route('/chewed_couch')
def chewed_couch():
    image = url_for('static', filename='images/shih-tzu.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     'Put a stop to the chewed up couch.'})
    return render_template('blogpost.html', blog_articles=
                           blog_articles, image=image)


@app.route('/newpuppy')
def newpuppy():
    image = url_for('static', filename='images/puppy-sleeping.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     'Are you ready for a new puppy?'})
    return render_template('articles.html', 
                           blog_articles=blog_articles, image=image)


@app.route('/better_life')
def better_life():
    image = url_for('static', filename='images/siberian-husky.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     'Four tips for a better life.'})
    return render_template('articles.html', 
                           blog_articles=blog_articles, image=image)


@app.route('/dog_bathing')
def dog_bathing():
    image = url_for('static', filename='images/chihuahua.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     'Tips for easier dog bathing.'})
    return render_template('articles.html', 
                           blog_articles=blog_articles, image=image)


@app.route('/pet_allergies')
def pet_allergies():
    image = url_for('static', filename='images/portuguese-water-dog.jpg')
    blog_articles = mongo.db.blog_articles.find_one({'blog_title': 
                                                     '6 Myths About Pet Allergies.'})
    return render_template('articles.html', blog_articles=blog_articles, 
                           image=image)


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/start_discussion')
def start_discussion():
    return render_template('start_discussion.html', 
                           now=datetime.now().strftime("%D, %H:%M"), 
                           categories=mongo.db.categories.find())


@app.route('/insert_discussion', methods=['POST'])
def insert_discussion():
    comments = mongo.db.comments
    comments.insert_one(request.form.to_dict())
    return redirect(url_for('discussions'))


@app.route('/edit_discussion/<comment_id>')
def edit_discussion(comment_id):
    the_comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edit_discussion.html', 
                           now=datetime.now().strftime("%D, %H:%M"), 
                           comment=the_comment, categories=all_categories)


@app.route('/update_discussion/<comment_id>', methods=["POST"])
def update_discussion(comment_id):
    comments = mongo.db.comments
    comments.update({'_id': ObjectId(comment_id)},
                    {
                     'category_name': request.form.get('category_name'),
                     'date_time': request.form.get('date_time'),
                     'username': request.form.get('username'),
                     'title': request.form.get('title'),
                     'comment': request.form.get('comment'),
                     'likes': request.form.get('likes'),
                    })
    return redirect(url_for('discussions'))


@app.route('/update_likes/<comment_id>', methods=["POST"])
def update_likes(comment_id):
    comments = mongo.db.comments
    comments.find_one_and_update({'_id': ObjectId(comment_id)},
                                 {
                                  '$inc': {'likes': 1},
                                 })
    return redirect(url_for('discussions'))


@app.route('/delete_discussion/<comment_id>')
def delete_discussion(comment_id):
    mongo.db.comments.remove({'_id': ObjectId(comment_id)})
    return redirect(url_for('discussions'))


@app.route('/discussions_thread/<comment_id>')
def discussions_thread(comment_id):
    the_comment = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    reply_comment = mongo.db.comment_replies.find({'comment_id': comment_id})
    return render_template('discussions_thread.html',
                           now=datetime.now().strftime("%D, %H:%M"),
                           comment=the_comment,
                           reply_comment=reply_comment)


@app.route('/reply/<comment_id>', methods=['POST'])
def reply(comment_id):
    comments = mongo.db.comment_replies
    comments.insert_one({ 
                         'comment_id': comment_id,
                         'date_time': request.form.get('date_time'),
                         'username': request.form.get('username'),
                         'comment': request.form.get('comment'),
                         })
    return redirect(request.referrer)


@app.route('/edit_reply/<comment_id>')
def edit_reply(comment_id):
    the_reply = mongo.db.comment_replies.find_one({'_id': ObjectId(comment_id)})
    return render_template('edit_reply.html',
                           now=datetime.now().strftime("%D, %H:%M"),
                           reply=the_reply)


@app.route('/update_reply/<reply_id>', methods=["POST"])
def update_reply(reply_id):
    reply = mongo.db.comment_replies
    reply.update({'_id': ObjectId(reply_id)},
                 {
                  'comment_id': request.form.get('comment_id'),
                  'date_time': request.form.get('date_time'),
                  'username': request.form.get('username'),
                  'comment': request.form.get('comment'),
                 })
    return redirect(url_for('discussions'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
