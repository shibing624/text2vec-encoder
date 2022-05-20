# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from jina import Client, Document, DocumentArray

c = Client(port=50001)

r = c.post(on='/encode', inputs=Document(text='hello'))
print(r, 'emb size:', len(r.to_dict()[0]['embedding']))

docs = DocumentArray(Document(text='如何更换花呗绑定银行卡'))
r = c.post(on='/encode', inputs=docs)
print(type(r.to_dict()), 'emb size:', len(r.to_dict()[0]['embedding']))

r = c.post(on='/encode', inputs=DocumentArray(Document(text='如何更换花呗绑定银行卡') for _ in range(20)), request_size=10)
print(len(r.to_dict()))
print([len(i['embedding']) for i in r.to_dict()])

sentences = ['如何更换花呗绑定银行卡', '你好'] * 20


def my_input():
    for s in sentences:
        yield Document(text=s)


print("---")
r = c.post('/', inputs=my_input, request_size=8)
print(r, type(r.to_dict()), len(r.to_dict()), 'emb size:', len(r.to_dict()[0]['embedding']))
