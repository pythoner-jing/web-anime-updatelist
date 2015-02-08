# -*- coding: utf-8 -*-

import settings
import urllib2
import collections

from flask import Flask, render_template, current_app
from flask.ext.socketio import SocketIO, emit
from lxml import etree

app = Flask(__name__)
app.config.from_object(settings)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('update')
def handle_update():
    content = urllib2.urlopen(current_app.config['CRAWL_SITE']).read()
    tree = etree.HTML(content)
    links = tree.xpath("//ul[@class='newUpdate']/descendant::a")
    dates = tree.xpath("//ul[@class='newUpdate']/descendant::span/text()")
    data = collections.OrderedDict()
    for l, d in zip(links, dates):
        if not data.has_key(d):
            data[d] = []
        data[d].append(l)
    emit('update', render_template('update-list.html', data=data))


@socketio.on('detail')
def handle_detail(path, id):
    url = "".join([current_app.config['CRAWL_SITE'], path])
    content = urllib2.urlopen(url).read()
    tree = etree.HTML(content)
    raw = tree.xpath("//div[@id='dowtab']/br[3]/following-sibling::*")
    img = tree.xpath("//div[@id='dowtab']/descendant::img")

    for i in img:
        if not i.attrib['src'].startswith('http'):
            i.set('src', ''.join([current_app.config['CRAWL_SITE'], i.attrib['src']]))

        i.set('style', 'width:100%;height:auto;')
        if i.attrib.has_key('width') and i.attrib['width'] == '0':
            i.set('style', 'display:none;')
        if i.attrib.has_key('height') and i.attrib['height'] == '0':
            i.set('style', 'display:none;')


    # for x in raw:
        # for y in x.findall('img'):
            # y.set('style', 'width:100%;height:auto;')

    data = "".join(map(lambda x: etree.tostring(x, encoding='utf-8').strip(), raw))
    emit('detail', {'data': data, 'id': id})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
