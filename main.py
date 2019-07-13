   

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc





app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:sowmya123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):      
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')



    def __init__(self, username, password):
        self.username = username
        self.password = password



    def __repr__(self):
        return self.username

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST', 'GET'])

def blog():
    if request.args.get('id'):
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        return render_template('singleblog.html', title="Build-A-Blog", blog=blog)
    else:
        #blogs = Blog.query.all()
        blogs = Blog.query.order_by(Blog.id.desc()).all()
        return render_template('blog.html', title="Build-A-Blog", blogs=blogs)



@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['body']
        
        blog_error=''
        title_error=''


        if blog_content == '':
           blog_error = "Please make sure you have some content."

        if blog_title == '':
            title_error = "Title Required"

        
        


        if blog_error != '' or title_error!='':
            return render_template('newpost.html', title="Build-A-Blog", 
            blog_title=blog_title, blog_content=blog_content, blog_error=blog_error, title_error=title_error)

        else:
            new_blog = Blog(blog_title, blog_content)
            db.session.add(new_blog)
            db.session.commit()

            recent_post = Blog.query.filter_by(title=blog_title).first()
            id = recent_post.id
            blog = Blog.query.filter_by(id=id).first()
            return redirect("/blog?id=" + str(id))
    else:
        return render_template('newpost.html', title="Build-A-Blog - New Post")

# @app.route('/blog')

# def index():
      
#     blogs = Blog.query.order_by("Blog.id desc").all()
#     return render_template('blog.html',title="Your Blog Name Here!", blogs=blogs)        


if __name__ == '__main__':
    app.run()