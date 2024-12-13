import os

from dotenv import load_dotenv
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from PIL import Image, ImageOps

from constants import PROCESSED_FOLDER, UPLOAD_FOLDER
from service import (add_gaussian_noise, plot_color_distribution,
                     recaptcha_verification)

load_dotenv()

app = Flask(__name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recaptcha_response = request.form.get("g-recaptcha-response")
        if not recaptcha_response:
            flash("Пожалуйста, подтвердите, что вы не робот.", "danger")
            return redirect(url_for("index"))
        if not recaptcha_verification(recaptcha_response):
            flash("Не удалось подтвердить, что вы не робот."
                  " Попробуйте снова.", "danger")
            return redirect(url_for("index"))
        file = request.files['image']
        noise_level = int(request.form.get('noise_level', 10))
        if file and 0 <= noise_level <= 100:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            image = Image.open(filepath)
            image = ImageOps.exif_transpose(image)
            noisy_image = add_gaussian_noise(image, noise_level)
            processed_path = os.path.join(
                PROCESSED_FOLDER,
                f'noisy_{os.path.basename(filepath)}'
            )
            noisy_image.save(processed_path)
            original_hist_path = os.path.join(
                PROCESSED_FOLDER,
                f'original_hist_{os.path.basename(filepath)}'
            )
            noisy_hist_path = os.path.join(
                PROCESSED_FOLDER,
                f'noisy_hist_{os.path.basename(filepath)}'
            )
            plot_color_distribution(image, original_hist_path)
            plot_color_distribution(noisy_image, noisy_hist_path)
            return render_template(
                'result.html',
                original_image=filepath,
                noisy_image=processed_path,
                original_hist_path=original_hist_path,
                noisy_hist_path=noisy_hist_path

            )
        else:
            flash("Некорректные данные. Попробуйте снова.", "danger")
            return redirect(url_for("index"))
    return render_template('index.html')


if app.debug:
    @app.route('/media/upload/<filename>')
    def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    @app.route('/media/process/<filename>')
    def process_file(filename):
        return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
