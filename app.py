from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        noise_level = request.form.get('noise_level')
        if file and noise_level:
            return f"Файл: {file.filename}, Уровень шума: {noise_level}"
        else:
            return "Ошибка: не удалось получить файл или параметр"
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
