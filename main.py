from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    __bind__="todo"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class Users(db.Model):
    __bind__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def mainPage():
    if request.method == 'POST':
        try: #when user Sign In
            userName = request.form['signcontent']
            password = request.form['signpass']
            if len(userName)!=0 and len(password)!=0:
                new_User= Users(username=userName,password=password)
                try:
                    db.session.add(new_User)
                    db.session.commit()
                    return redirect('/data/'+str(new_User.id))
                except:
                    return 'There was an issue adding your task'
        except: #when user Log In
            userName = request.form['content']
            password = request.form['pass']
            new_User= Users(username=userName,password=password)
            users = Users.query.order_by(Users.date_created).all()
            for user in users:
                if  user.username == userName and user.password == password:
                    found=1
                    return redirect('/data/'+str(user.id))
                    break
        return redirect('/')#if nothing happens then just stay at main page
    else:
        return render_template('login_data.html')



@app.route('/data/<string:id>', methods=['POST', 'GET'])
def index(id): #To DO page
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content,user_id=int(id))
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/data/'+id)
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        found=0
        todo=[]
        for task in tasks:
            if task.user_id == int(id):
                todo.append(task)   
                found=1
        if found == 1:
            return render_template('data.html', tasks=todo, user_id=id)
        return render_template('data.html', user_id=id)
        


@app.route('/delete/<int:id>/<int:cur_id>/<string:content>')
def delete(id,cur_id,content):
    tasks = Todo.query.order_by(Todo.date_created).all()
    cur_task=[]
    cur_content=[]

    for task in tasks:
        if task.user_id ==id:
            cur_task.append(task)
            cur_content.append(task.content)
    try:
        db.session.delete(cur_task[cur_content.index(content)])
        db.session.commit()
        return redirect('/data/'+str(id))
    except:
        return 'There was a problem deleting that task'



@app.route('/update/<int:id>/<int:cur_id>/<string:content>', methods=['GET', 'POST'])
def update(id,cur_id,content):
    tasks = Todo.query.order_by(Todo.date_created).all()
    cur_task=[]
    cur_content=[]

    for task in tasks:
        if task.user_id ==id:
            cur_task.append(task)
            cur_content.append(task.content)


    if request.method == 'POST':
        cur_task[cur_content.index(content)].content = request.form['content']  

        try:
            db.session.commit()
            return redirect('/data/'+str(id))
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=cur_task[cur_content.index(content)], user_id=id)


if __name__ == "__main__":
    app.run(debug=True)