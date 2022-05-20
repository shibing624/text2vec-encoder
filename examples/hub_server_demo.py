# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from jina import Flow, Document

f = Flow(port=50001).add(uses='jinahub://Text2vecEncoder')

with f:
    f.block()
