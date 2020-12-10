from flask import Flask, request, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from common.base_ import query

app = Flask(__name__)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["48000 per day", "2000 per hour"]
)


@app.route('/', methods=['GET'])
@limiter.limit("2/second", override_defaults=False)
def index():
    """
    浏览器及CURL路由入口
    :return:
    """
    curl, remote = request.headers, request.headers.get('X-Real-IP')
    return query(args=remote, header=curl)


@app.route('/v1/', methods=['GET'])
@limiter.limit("1/second", override_defaults=False)
def main_():
    """
    独立路由,响应表单查询
    :return:
    """
    request_ = request.args.get('address')
    if request_:
        return query(args=request_, header=None)
    else:
        return redirect(url_for('index'))
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=False)
