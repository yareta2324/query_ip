from flask import Flask, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from common.base_ import query

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["48000 per day", "2000 per hour"]
)


@app.route('/', methods=['GET'])
@limiter.limit("1/second", override_defaults=False)
def index():
    """browser and the CURL route"""
    rel_ip = request.headers.get('X-Real-IP')
    header = request.headers
    return query(args=rel_ip, header=header)


@app.route('/v1/', methods=['GET'])
@limiter.limit("1/second", override_defaults=False)
def main_():
    """Responding to form queries"""
    request_ = request.args.get('address')
    if request_:
        return query(args=request_, header=None)
    else:
        return redirect(url_for('index'))
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
