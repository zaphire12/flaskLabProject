import os

import matplotlib.pyplot as plt
import numpy as np
import requests
import tensorflow as tf
from PIL import Image


def add_gaussian_noise(image, noise_level):
    """Добавляет Gaussian Noise к изображению с использованием TensorFlow."""
    np_image = np.array(image) / 255.0  # Нормализация
    noise = tf.random.normal(
        shape=np_image.shape,
        mean=0.0,
        stddev=noise_level / 100.0
    )  # Генерация шума
    noisy_image = tf.clip_by_value(
        np_image + noise,
        0.0,
        1.0
    )  # Ограничение значений в диапазоне [0, 1]
    noisy_image = (noisy_image * 255).numpy().astype(np.uint8)
    return Image.fromarray(noisy_image)


def plot_color_distribution(image, output_path):
    """Создает график распределения цветов."""
    np_image = np.array(image)
    plt.figure(figsize=(8, 4))
    for i, color in enumerate(['Red', 'Green', 'Blue']):
        plt.hist(
            np_image[..., i].flatten(),
            bins=256,
            alpha=0.5,
            label=color,
            color=color.lower()
        )
    plt.title('Распределение цвета')
    plt.xlabel('Интенсивность')
    plt.ylabel('Частота')
    plt.legend()
    plt.savefig(output_path)
    plt.close()


def recaptcha_verification(recaptcha_response):
    verification = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": os.getenv(
                'SECRET_CAPTCHA',
                '6Ld-w5oqAAAAALQR2S86-mo6Ij0CjBrhBREOtA_i'
            ),
            "response": recaptcha_response,
        }
    )
    result = verification.json()
    if not result.get("success"):
        return False
    return True
