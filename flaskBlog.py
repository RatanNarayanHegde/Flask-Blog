from flask import Flask,render_template

app= Flask(__name__)

posts = [
    {
        'author': 'Ratan Hegde',
        'title': 'Blog Post 1',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus, mollitia?'
        'date_pub': 'June 14 2020'
    },
    {
        'author': 'Shubham Kumtole',
        'title': 'Blog Post 2',
        'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus, mollitia?'
        'date_pub': 'June 13 2020'
    }
]

@app.route("/")
def home():
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='About')


if __name__=='__main__':
    app.run(debug=True)