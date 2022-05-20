# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

from docarray import Document, DocumentArray

da = DocumentArray([Document(text='如何更换花呗绑定银行卡'), Document(text='hello'), Document(text='你好'), ])
r = da.post('jinahub://Text2vecEncoder')

print(r.to_json())
