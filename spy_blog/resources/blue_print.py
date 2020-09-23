import os
from urllib.parse import urlparse, parse_qsl

import qrcode
from flask.blueprints import Blueprint
from io import BytesIO
from flask import send_file, make_response, Response, current_app, request, abort

from config import static_dir
from models.blog import Website


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


# 记录页面访问的插件
@blue.route('/a_js')
def analyze_script():
    return Response(
        current_app.config['JAVASCRIPT'] % (current_app.config['DOMAIN']),
        mimetype='text/javascript'
    )


@blue.route('/a_gif')
def analyze():
    if not request.args.get('url'):
        abort(404)

    site = Website()

    parsed = urlparse(request.args['url'])
    params = dict(parse_qsl(parsed.query))

    site.domain = parsed.netloc,
    site.url = parsed.path,
    site.title = request.args.get('t') or '',
    site.ip = request.headers.get('X-Forwarded-For', request.remote_addr),
    site.referrer = request.args.get('ref') or '',
    site.headers = dict(request.headers),
    site.user_agent = request.user_agent.browser,
    site.params = params
    site.save_to_db()

    response = Response(current_app.config['BEACON'], mimetype='image/gif')
    response.headers['Cache-Control'] = 'private, no-cache'
    return response
