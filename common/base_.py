import ssl
import urllib.request
from flask import render_template


def query(args, header=None):
    """
    Request IP query interface
    :param args:
    :param header:
    :return:
    """
    url_ = 'https://ip-api.com/json/%s?lang=zh-CN' % args.strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
    }
    ssl_ = urllib.request.urlopen(
        urllib.request.Request(url_, headers=headers), context=ssl.SSLContext()
    )
    json = eval(ssl_.read().decode('utf-8'))
    if 'fail' not in json['status']:
        if 'curl' not in str(header):
            return render_template('index.html', agr_=json)
        else:
            curl = ("IP     %s\n" % json['query'] + "地址:  %s\n" % json['country'] + "地区:  %s\n" % json['regionName']
                    + "城市:  %s\n" % json['city'] + "ISP_:  %s\n" % json['isp'] + "VPN_:  https://pyvpn.net\n")
            return curl % json
    else:
        return "<h1>%s</h1>" % json['message']
