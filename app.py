from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_api_key():
    with open('config.txt') as f:
        return f.readline().strip()

DEEPL_API_KEY = get_api_key()

def translate(text, target_lang):
    url = 'https://api-free.deepl.com/v2/translate'
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_lang
    }
    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise Exception('Failed to translate text: {}'.format(response.content))
    return response.json()['translations'][0]['text']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def translate_text():
    dutch_text = request.form['dutch_text']
    english_text = translate(dutch_text, 'EN-US')
    chinese_text = translate(dutch_text, 'ZH')
    return render_template('index.html', dutch_text=dutch_text, english_text=english_text, chinese_text=chinese_text)

if __name__ == '__main__':
    app.run(debug=True)