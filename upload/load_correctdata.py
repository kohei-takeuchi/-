import os
from django.contrib.gis.utils import LayerMapping
from web.models import correctdata
# Modelとファイルのカラムのマッピング
mapping = {
    '緯度' : "緯度",
    '経度' : "経度",
    '深さ' : '深さ', 
    '最終変更時刻':'最終変更時刻',
    'geom' : 'POLYGON',
}
# ファイルパス
geojson_file = 'upload/data/correct.geojson'
   # 実行
def run(verbose=True):
    lm = LayerMapping(correctdata, geojson_file, mapping, transform=True, encoding='UTF-8')
    lm.save(strict=True, verbose=verbose)
