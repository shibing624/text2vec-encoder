# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import inspect
import os
import sys

if __name__ == '__main__':
    from jina import Flow

    f = Flow.load_config(
        'config.yml' if len(sys.argv) == 1 else sys.argv[1],
        extra_search_paths=[os.path.dirname(inspect.getfile(inspect.currentframe()))],
    )
    with f:
        f.block()