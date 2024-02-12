from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def news_func():
    news = [
        {
            'title': 'News 1',
            'description': 'This is a brief description of news 1.',
            'date': 'February 10, 2024'
        },
        {
            'title': 'News 2',
            'description': 'This is a brief description of news 2.',
            'date': 'February 11, 2024'
        },
        {
            'title': 'News 3',
            'description': 'This is a brief description of news 3.',
            'date': 'February 12, 2024'
        }
    ]
    return render_template('index.html', news=news)


if __name__ == '__main__':
    app.run(debug=True)
