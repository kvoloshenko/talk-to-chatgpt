from flask import Flask, request, json, flash
from werkzeug.utils import secure_filename
import os

# Функции для Flask
# UPLOAD_FOLDER = '/content/sample_data'
UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = {'wav'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return f"Running Flask on Google Colab!"

@app.route('/chat', methods=['POST'])
def chat():
    data = json.loads(request.data)
    print(type(data), f'chat data={data}')
    system_content = data['system_content']
    user_content = data['user_content']
    # completion = get_answer_gpt(system_content, user_content)
    # answer = completion.choices[0].message.content
    answer = 'test_answer'
    data['answer'] = answer
    print(f'return data={data}')
    return data


@app.route('/transcript', methods=['POST'])
# https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
def transcript():
    print("transcript")


    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return 'No file part'
    file = request.files['file']
    print(type(file))
    args = request.args
    print(type(args), f'args={args}')
    language = request.args.get('language')
    print(type(language), f'language={language}')


    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return 'No file part'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    my_file_1 = UPLOAD_FOLDER + "/"+ filename
    print(f'my_file_1={my_file_1}')
    # my_file_2 ='/content/sample_data/myrecording.wav'
    # print(f'my_file_2={my_file_2}')

    # transcript= get_transcript(my_file_2)
    transcript = 'test_transcript'

    data = {"transcript": transcript}
    print(f'return data={data}')
    return data


@app.route('/db_create', methods=['POST'])
def db_create():
    data = json.loads(request.data)
    print(f'db_create data={data}')
    knowledge_base_url = data['knowledge_base_url']
    ba = data['ba']
    # db, db_file_name, chunk_num = chat_gpt.create_db(knowledge_base_url, ba)
    # data['db_file_name'] = db_file_name
    # data['chunk_num'] = chunk_num
    return data

if __name__ == "__main__":
    port_no = 5000
    app.run(port=port_no)