import os
from django.contrib.gis.utils import LayerMapping
from web.models import purchasedata
# Modelとファイルのカラムのマッピング
mapping = {
    'lat' : "lat",
    'lon' : "lon",
    'rank' : 'rank',  
    'ID' : 'ID',
    'time' : 'time',
    'geom' : 'POLYGON',
}
# ファイルパス
geojson_file = 'upload/data/purchase.geojson'
   # 実行
def run(verbose=True):
    lm = LayerMapping(purchasedata, geojson_file, mapping, transform=True, encoding='UTF-8')
    lm.save(strict=True, verbose=verbose)
