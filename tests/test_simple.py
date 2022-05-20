# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""

import pytest
from docarray import Document, DocumentArray
from jina import Flow, Client
import sys

sys.path.append('..')
from src.text2vec_encoder import Text2vecEncoder

port = 50002


@pytest.fixture(scope='session', params=['torch'])
def make_flow(request):
    f = Flow(port=port).add(name=request.param, uses=Text2vecEncoder)
    with f:
        yield f


@pytest.mark.parametrize('protocol', ['grpc'])
def test_protocols_grpc(protocol):
    f = Flow(port=port + 3, protocol=protocol).add(
        uses=Text2vecEncoder
    )
    with f:
        c = Client(protocol=protocol, port=port + 3)
        r = c.post('/', Document(text='hello, world'))
        print(len(r.to_dict()))
        assert len(r.to_dict()) == 1


@pytest.mark.parametrize('protocol', ['http'])
def test_protocols_http(protocol):
    f = Flow(port=port + 1, protocol=protocol).add(
        uses=Text2vecEncoder
    )
    with f:
        c = Client(protocol=protocol, port=port + 1)
        r = c.post('/', Document(text='hello, world'))
        print(len(r.to_dict()))
        assert len(r.to_dict()) == 1


@pytest.mark.parametrize('protocol', ['websocket'])
def test_protocols_websocket(protocol):
    f = Flow(port=port + 2, protocol=protocol).add(
        uses=Text2vecEncoder
    )
    with f:
        c = Client(protocol=protocol, port=port + 2)
        r = c.post('/', Document(text='hello, world'))
        print(len(r.to_dict()))
        assert len(r.to_dict()) == 1


@pytest.mark.parametrize(
    'inputs',
    [
        DocumentArray([Document(text='hello, world'), Document(text='goodbye, world')]),
        Document(text='hello, world'),
    ],
)
def test_plain_inputs(make_flow, inputs):
    c = Client(port=make_flow.port, protocol='grpc')
    r = c.post('/', inputs if not callable(inputs) else inputs())

    assert r.shape[0] == len(list(inputs)) if not callable(inputs) else len(list(inputs()))


@pytest.mark.parametrize(
    'inputs',
    [
        [Document(text='hello, world'), Document(text='goodbye, world')],
        DocumentArray([Document(text='hello, world'), Document(text='goodbye, world')]),
        lambda: (Document(text='hello, world') for _ in range(10)),
        DocumentArray(
            [
                Document(text='hello, world'),
            ]
        ),
    ],
)
def test_docarray_inputs(make_flow, inputs):
    c = Client(port=make_flow.port, protocol='grpc')
    r = c.post('/', inputs if not callable(inputs) else inputs())
    assert isinstance(r, DocumentArray)
    assert r.embeddings.shape
