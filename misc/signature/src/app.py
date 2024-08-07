from flask import Flask, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import base64
import tempfile
import predict

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["20 per minute"]
)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def index():
    if request.method == 'POST':
        image_data = request.form.get('signature')
        image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)

        # Save the image as a PNG file and make a prediction
        with tempfile.NamedTemporaryFile(suffix='.png', dir='/tmp') as f:
            f.write(image_bytes)
            f.seek(0)
            status = predict.predict(f.name)

            if status:
                with open('flag.txt', 'r') as g:
                    flag = g.read()
                return 'Access granted! ' + flag
            else:
                return f'Access denied! The signature is not genuine!'

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
