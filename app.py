from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@cluster0.kbfqt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

@app.route('/')
def home(): 
  return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    # return jsonify({'msg': 'GET request complete!'})
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    # return jsonify({'msg': 'POST request complete!'})
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    # Menerima file dari sisi server
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]
    filename = f'file-{mytime}.{extension}' 
    save_to = f'static/{filename}' # save image ke folder static
    file.save(save_to) 
    
    # Membuat profile di sisi client
    profile = request.files["profile_give"]
    extension = profile.filename.split('.')[-1]
    profilename = f'profile-{mytime}.{extension}'
    save_to = f'static/{profilename}' # save image ke folder static
    profile.save(save_to) 

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file': filename,
        'profile': profilename,
        'title': title_receive,
        'content': content_receive,
        'time': time,
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=5000, debug=True)