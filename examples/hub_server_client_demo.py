# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from jina import Flow, Document

f = Flow().add(
    uses='jinahub://Text2vecEncoder',
)

doc = Document(content='如何更换花呗绑定银行卡')

with f:
    r = f.post(on='/', inputs=doc)
    print(r)
