# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
from jina import Flow
from src import Text2vecEncoder
import os

pwd_path = os.path.abspath(os.path.dirname(__file__))

config_path = os.path.join(pwd_path, '../src/config.yml')
# Heavy-lifting jobs should be put into an Executor if possible.
# For instance, sending high-resolution images to the Flow can be time-consuming.
# 多个执行器处理，模型预测提速
f = Flow.load_config(config_path).add(uses=Text2vecEncoder, replicas=2)
with f:
    f.block()
