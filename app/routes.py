from app import app,db
from flask import Flask, flash, render_template, request, redirect, url_for
from app.models import Todo,Completed

# route of the index page displaying the tasks and buttons to update and delete
@app.route('/', methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)

        # Validation to check if the task name is empty
        if task_content != "":
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return "Error adding to database"
        else:
            flash("Please enter a task name")
            return redirect(url_for('index'))
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        competed_tasks = Completed.query.order_by(Completed.date_completed).all()
        
        return render_template("home.html",tasks=tasks,competed_tasks=competed_tasks)
    
# Api route to delete a task given an id of the task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        completed_task = Completed(content=task_to_delete.content)
        db.session.add(completed_task)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "problem with deleting"

# Api route to update a task given an id of the task
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method=='POST':
        task.content = request.form['content']

        # Validation to check if the task name is empty
        if task.content != "":
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "error updating"
        else:
            flash("Please enter a task name")
            return redirect(url_for('update',id=task.id))
    else:
        return render_template("update.html",task=task)

# Api route to clear completed tasks
@app.route('/clear_all')
def clear():
    try:
        task_to_clear = db.session.query(Completed).delete()
        db.session.commit()
        return redirect('/')
    except:
        db.session.rollback()
