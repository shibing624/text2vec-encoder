# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from jina import Flow, Document

f = Flow().add(
    uses='jinahub+docker://Text2vecEncoder',
    uses_with={'pretrained_model_name_or_path': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'}
)

doc = Document(content='如何更换花呗绑定银行卡')

with f:
    f.post(on='/foo', inputs=doc, on_done=lambda resp: print(resp.docs[0].embedding))
