from flask import Flask, render_template,request, redirect, url_for #url_for() is used in base template to connect css
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #initializing flask application
app.app_context().push() # set up an application context with app.app_context() (pta nhi, error dera tha isliye google krke dala ye wala function)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 '/' = relative path | 4 '/' = absolute path
db = SQLAlchemy(app) #initializing database

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String[200], nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self): #to return a str value
        return '<Task %r>' % self.id # %r attaches to %self.id, i.e. task id will be returned as string

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] #request from the form with id==content
        new_task = Todo()
        new_task.content=task_content

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') #returns/redirects to homepage (url is '/')
        except:
            return 'there was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #looks at all the data in order of date_created
        return render_template("index.html", tasks=tasks)
    
# defining the delete task feature
@app.route('/delete/<int:id>')
def delete(id): #delete task by its unique id
    task_to_delete = Todo.query.get_or_404(id) #get task id or raise error 404

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') #returns/redirects to homepage (url is '/')
    except:
        return 'There was an error deleting your task' 
    

# defining the update task feature
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an error updating your task'
    else:
        return render_template('update.html', task=task)

if __name__=="__main__":
    app.run(debug=True)