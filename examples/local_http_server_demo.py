# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import os
import sys
from jina import Flow

sys.path.append('..')
from src import Text2vecEncoder

pwd_path = os.path.abspath(os.path.dirname(__file__))

f = Flow(protocol='http', port=50003).add(uses=Text2vecEncoder)
with f:
    f.block()

# Then, run "sh http_get.sh" get result.
