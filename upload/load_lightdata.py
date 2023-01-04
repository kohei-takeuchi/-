import os
from django.contrib.gis.utils import LayerMapping
from web.models import lightdata
# Modelとファイルのカラムのマッピング
mapping = {
    '緯度' : "緯度",
    '経度' : "経度",
    '深さ' : '深さ', 
    'geom' : 'POINT',
}
# ファイルパス
geojson_file = 'upload/data/light.geojson'
   # 実行
def run(verbose=True):
    lm = LayerMapping(lightdata, geojson_file, mapping, transform=True, encoding='UTF-8')
    lm.save(strict=True, verbose=verbose)
