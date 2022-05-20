# Text2vecEncoder

**Text2vecEncoder** wraps the torch-version of transformers from huggingface. It encodes text data into dense vectors.

**Text2vecEncoder** receives [`Documents`](https://docs.jina.ai/fundamentals/document/) with `text` attributes.
The `text` attribute represents the text to be encoded. This Executor will encode each `text` into a dense vector and store them in the `embedding` attribute of the `Document`.


## Usage

From source deployment:

examples: [examples/client_demo.py](examples/client_demo.py)

```python
from docarray import Document, DocumentArray

da = DocumentArray([Document(text='如何更换花呗绑定银行卡'), Document(text='hello'), Document(text='你好'), ])
r = da.post('jinahub://Text2vecEncoder')

print(r.to_json())
```

output:
```shell
"embedding": [-0.0004445354570634663, -0.2973471283 ...]
```


Use the prebuilt images from Jina Hub in your Flow and encode an text into a dense vector.


```python
from jina import Flow, Document

f = Flow().add(uses='jinahub+docker://Text2vecEncoder')

doc = Document(content='如何更换花呗绑定银行卡')

with f:
    f.post(on='/encode', inputs=doc, on_done=lambda resp: print(resp.docs[0].embedding))
```


### Set `volumes`

With the `volumes` attribute, you can map the cache directory to your local cache directory, in order to avoid downloading 
the model each time you start the Flow.

```python
from jina import Flow

flow = Flow().add(
    uses='jinahub+docker://Text2vecEncoder',
    volumes='.cache/huggingface:/root/.cache/huggingface'
)
```

Alternatively, you can reference the docker image in the `yml` config and specify the `volumes` configuration.

`flow.yml`:

```yaml
jtype: Flow
executors:
  - name: encoder
    uses: 'jinahub+docker://Text2vecEncoder'
    volumes: '.cache/huggingface:/root/.cache/huggingface'
```

And then use it like so:
```python
from jina import Flow

flow = Flow.load_config('flow.yml')
```


### Use other pre-trained models
You can specify the model to use with the parameter `pretrained_model_name_or_path`:
```python
from jina import Flow, Document

f = Flow().add(
    uses='jinahub+docker://Text2vecEncoder',
    uses_with={'pretrained_model_name_or_path': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'}
)

doc = Document(content='如何更换花呗绑定银行卡')

with f:
    f.post(on='/encode', inputs=doc, on_done=lambda resp: print(resp.docs[0].embedding))
```

You can check the supported pre-trained models [here](https://huggingface.co/transformers/pretrained_models.html)

### Use GPUs
To enable GPU, you can set the `device` parameter to a cuda device.
Make sure your machine is cuda-compatible.
If you're using a docker container, make sure to add the `gpu` tag and enable 
GPU access to Docker with `gpus='all'`.
Furthermore, make sure you satisfy the prerequisites mentioned in 
[Executor on GPU tutorial](https://docs.jina.ai/tutorials/gpu_executor/#prerequisites).

```python

from jina import Flow, Document

f = Flow().add(
    uses='jinahub+docker://Text2vecEncoder/gpu',
    uses_with={'device': 'cuda'}, gpus='all'
)

doc = Document(content='如何更换花呗绑定银行卡')

with f:
    f.post(on='/encode', inputs=doc, on_done=lambda resp: print(resp.docs[0].embedding))
```

## Reference
- [Huggingface Transformers](https://huggingface.co/transformers/pretrained_models.html)
