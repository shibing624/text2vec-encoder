# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""

import subprocess

import pytest
from jina import Document, DocumentArray, Flow
from transform_encoder import Text2vecEncoder

_EMBEDDING_DIM = 768


@pytest.mark.parametrize('request_size', [1, 10, 50, 100])
def test_integration(request_size: int):
    docs = DocumentArray(
        [Document(text='just some random text here') for _ in range(50)]
    )
    with Flow().add(uses=Text2vecEncoder) as flow:
        da = flow.post(
            on='/index',
            inputs=docs,
            request_size=request_size,
        )

    assert len(da) == 50
    for doc in da:
        assert doc.embedding.shape == (_EMBEDDING_DIM,)


@pytest.mark.gpu
@pytest.mark.docker
def test_docker_runtime_gpu(build_docker_image_gpu: str):
    with pytest.raises(subprocess.TimeoutExpired):
        subprocess.run(
            [
                'jina',
                'executor',
                f'--uses=docker://{build_docker_image_gpu}',
                '--gpus',
                'all',
                '--uses-with',
                'device:cuda',
            ],
            timeout=30,
            check=True,
        )

