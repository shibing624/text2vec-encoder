# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description: 
"""
import numpy as np
import mimetypes
from docarray import DocumentArray, Document


class Client:
    def __init__(self, **kwargs):
        """Create a Clip client object that connects to the Clip server.

        Server scheme is in the format of `scheme://netloc:port`, where
            - scheme: one of grpc, websocket, http, grpcs, websockets, https
            - netloc: the server ip address or hostname
            - port: the public port of the server

        :param server: the server URI
        """

        from jina import Client

        self._client = Client(**kwargs)
        self._results = DocumentArray()

    def _get_post_payload(self, content, kwargs):
        return dict(
            on='/',
            inputs=self._iter_doc(content),
            request_size=kwargs.get('batch_size', 256),
            total_docs=len(content) if hasattr(content, '__len__') else None,
        )

    @property
    def _unboxed_result(self):
        if self._results.embeddings is None:
            raise ValueError(
                'empty embedding returned from the server. '
                'This often due to a mis-config of the server, '
                'restarting the server or changing the serving port number often solves the problem'
            )
        return self._results.embeddings if self._return_plain else self._results

    def _iter_doc(self, content):
        self._return_plain = True
        for c in content:
            if isinstance(c, str):
                self._return_plain = True
                _mime = mimetypes.guess_type(c)[0]
                if _mime and _mime.startswith('image'):
                    yield Document(uri=c).load_uri_to_blob()
                else:
                    yield Document(text=c)
            elif isinstance(c, Document):
                if c.content_type in ('text', 'blob'):
                    self._return_plain = False
                    yield c
                elif not c.blob and c.uri:
                    c.load_uri_to_blob()
                    self._return_plain = False
                    yield c
                elif c.tensor is not None:
                    yield c
                else:
                    raise TypeError(f'unsupported input type {c!r} {c.content_type}')
            else:
                raise TypeError(f'unsupported input type {c!r}')

    def _gather_result(self, r):
        r = r.data.docs
        self._results.extend(r)

    def encode(self, content, **kwargs):
        if isinstance(content, str):
            raise TypeError(
                f'content must be an Iterable of [str, Document], try `.encode(["{content}"])` instead'
            )
        self._results = DocumentArray()
        self._client.post(
            **self._get_post_payload(content, kwargs), on_done=self._gather_result
        )
        return self._unboxed_result
