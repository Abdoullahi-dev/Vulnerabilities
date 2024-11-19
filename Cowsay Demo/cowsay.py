from flask import Flask, request, render_template
import subprocess

from pyexpat.errors import messages

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ''
    try:
        message = request.form.get('CowInput', 'You need to have a message, or the site freezes, it\'s kinda annoying.')
        print(message)
        if message != '':
            output = subprocess.check_output(f"cowsay {message}", shell=True).decode('utf8')
        print(output)
    except Exception as e:
        print(e)
    return render_template("cowsay.html", cowsay_message=output)


if __name__ == '__main__':
    app.run(debug=True)
