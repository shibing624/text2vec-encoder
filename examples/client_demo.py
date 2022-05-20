# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from jina import Client, Document, DocumentArray
import json

c = Client(port=49979)

r = c.post(on='/encode', inputs=Document(text='hello'))
print(r, r.to_json())

docs = DocumentArray(Document(content='如何更换花呗绑定银行卡'), Document(content='你好'))
r = c.post(on='/encode', inputs=docs)
print(type(r.to_json()), r.to_json(), )

r = c.post(on='/bar', inputs=DocumentArray(Document(text='如何更换花呗绑定银行卡') for _ in range(20)), request_size=10)
print(len(r.to_json()))
print([len(i['embedding']) for i in json.loads(r.to_json())])
