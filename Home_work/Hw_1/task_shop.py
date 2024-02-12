from flask import Flask, render_template

app = Flask(__name__)


categories = {
    'Одежда': ['Футболки', 'Джинсы', 'Платья'],
    'Обувь': ['Кроссовки', 'Ботинки', 'Сандалии']
}

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/<category>')
def category(category):
    items = categories.get(category)
    if items:
        return render_template('category.html', category=category, items=items)
    else:
        return 'Категория не найдена', 404

@app.route('/<category>/<item>')
def item(category, item):
    return render_template('item.html', item=item)

if __name__ == '__main__':
    app.run(debug=True)
