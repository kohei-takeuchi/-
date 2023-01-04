import os
from django.contrib.gis.utils import LayerMapping
from web.models import depthdata
# Modelとファイルのカラムのマッピング
mapping = {
    '緯度' : "緯度",
    '経度' : "経度",
    '深さ' : '深さ',
    '計測時刻' : '計測時刻',
    '計測機器' : '計測機器',
    '投稿者' : '投稿者',
    '投稿時刻' : '投稿時刻',
    'geom' : 'POINT',
}

# ファイルパス
#geojson_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data',  'do.geojson'))
geojson_file = 'upload/data/do.geojson'
   # 実行
def run(verbose=True):
    lm = LayerMapping(depthdata, geojson_file, mapping, transform=True, encoding='UTF-8')
    lm.save(strict=True, verbose=verbose)
