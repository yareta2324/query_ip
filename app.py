import ssl
import urllib.request
from flask import Flask, request, render_template, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app, key_func=get_remote_address, default_limits=["300 per day", "60 per hour"]
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


def query(args, header=None):
    """
    此函数方法用于API查询
    :return: 
    """""
    url = 'http://ip-api.com/json/%s?lang=zh-CN' % args.strip()
    result = urllib.request.Request(url)
    ssl_ = urllib.request.urlopen(result, context=ssl.SSLContext())
    json = eval(ssl_.read().decode('utf-8'))
    if 'fail' not in json['status']:
        curl = ("IP     %s\n" % json['query'] + "地址:  %s\n" % json['country'] + "地区:  %s\n" % json['regionName'] +
                "城市:  %s\n" % json['city'] + "ISP_:  %s\n" % json['isp'] + "VPN_:  https://pyvpn.net\n")
        if 'curl' not in str(header):
            return render_template('index.html', agr_=json)
        else:
            return curl % json
    else:
        return "<h1>%s</h1>" % json['message']


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
