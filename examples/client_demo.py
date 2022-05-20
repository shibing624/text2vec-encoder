# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from src import Client

c = Client(port=50001)

r = c.encode(['如何更换花呗绑定银行卡'])
print('emb size:', len(r[0]), r)
