from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///learning.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy (app)

class Learning(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) 
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        learning=Learning(title=title, desc=desc)
        db.session.add(learning)
        db.session.commit()
    allLearning = Learning.query.all()
    return render_template('index.html', allLearning=allLearning)
   
@app.route('/show')
def products():
    allLearning = Learning.query.all()
    print(allLearning)
    return 'this is products page'
@app.route('/update/<int:sno>' , methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        updlearning = Learning.query.filter_by(sno=sno).first()
        updlearning.title=title
        updlearning.desc=desc
        db.session.add(updlearning)
        db.session.commit()
        return redirect("/")
    updlearning = Learning.query.filter_by(sno=sno).first()   
    return render_template('update.html', updlearning=updlearning)
@app.route('/delete/<int:sno>')
def delete(sno):
    dellearning = Learning.query.filter_by(sno=sno).first()
    db.session.delete(dellearning)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
