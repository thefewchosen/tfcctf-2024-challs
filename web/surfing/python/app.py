from flask import Flask, request, render_template,jsonify
import requests

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def get_url():
    # Get the URL parameter from the request
    url = request.args.get('url', '')
    
    # Ensure the URL starts with http:// or https:// to mitigate risks
    if not (url.startswith('http://google.com/') or url.startswith('https://google.com/')):
        return jsonify({'error': 'Hacking detected, url must start with http://google.com/'}), 400
    
    url = url + '.png'
    
    response = requests.get(url)
    
    result = response.text
    
    if(result):
        print(result)

    # Return the result of the command
    return jsonify({'output': result})

@app.route('/', methods=['GET'])
def home():
    return(render_template('index.html'))


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
