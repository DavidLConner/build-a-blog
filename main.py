from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blogpost(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/blogs', methods=['POST', 'GET'])
def index():
    blogs=Blogpost.query.all()
    blog_id = request.args.get('id')
    

    if blog_id:
        post = Blogpost.query.get(blog_id)
        return render_template('blog-ID.html', title="Blog Post", post=post)    
    else:
 
        return render_template('blogs.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    if request.method == 'POST':   
        title = request.form['title']
        body = request.form['body']

        new_blog = Blogpost(title, body)
        db.session.add(new_blog)
        db.session.commit()

        if (title) or (body) == "":
            return redirect('/blogs')
        else:
            flash('Fields cannot be left empty.')
    else:
        return render_template('newpost.html')    


if __name__ == '__main__':
    app.run()