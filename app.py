import random
import string

from flask import Flask, render_template

app = Flask(__name__)
rand = random.Random


def generate_word(count):
    return ''.join(random.choices(string.ascii_lowercase, k=count))


def generate_text():
    return ' '.join([generate_word(random.randint(a=3, b=7)) for _ in range(10)])


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html', text=generate_text())


if __name__ == '__main__':
    app.run()
