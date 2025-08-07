from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["todo_app"]
tasks_collection = db["tasks"]

@app.route('/')
def index():
    # Fetch tasks from MongoDB
    tasks = list(tasks_collection.find())
    return render_template('index.html', tasks=tasks)
'''
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    if task_text:
        tasks_collection.insert_one({"task": task_text})
    return redirect('/')
'''
@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task')
    print("Received task:", task_text)  # ✅ Add this line
    if task_text:
        result = tasks_collection.insert_one({"task": task_text})
        print("Inserted ID:", result.inserted_id)  # ✅ Add this too
    return redirect('/')

@app.route('/delete/<task_id>', methods=['POST', 'DELETE'])
def delete_task(task_id):
    try:
        tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if request.method == 'POST':
            return redirect('/')
        return {'message': 'Task deleted'}, 200
    except Exception as e:
        if request.method == 'POST':
            return redirect('/')
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
