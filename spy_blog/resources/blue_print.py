import os

import qrcode
from flask.blueprints import Blueprint
from io import BytesIO
from flask import send_file, make_response

from config import static_dir


blue = Blueprint('blue', __name__)


@blue.route('/image/qrcode')
def qr_code():
    qr = qrcode.QRCode(
        version=4,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data('123')
    qr.make(fit=True)
    img = qr.make_image()

    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')


@blue.route('/image/<img_name>')
def images(img_name):
    with open(os.path.join(static_dir, 'images', img_name), 'rb') as f:
        res = make_response(f.read())
        res.headers['Content-Type'] = 'image/png'
        return res

