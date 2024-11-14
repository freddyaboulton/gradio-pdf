
# `gradio_pdf`
<a href="https://pypi.org/project/gradio_pdf/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_pdf"></a> <a href="https://github.com/freddyaboulton/gradio-pdf/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> <a href="https://huggingface.co/spaces/freddyaboulton/gradio_pdf/discussions" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/%F0%9F%A4%97%20Discuss-%23097EFF?style=flat&logoColor=black"></a>

Easily display PDFs in Gradio

## Installation

```bash
pip install gradio_pdf
```

## Usage

```python

import gradio as gr
from _app import demo as app
import os

_docs = {'PDF': {'description': 'A base class for defining methods that all input/output components should have.', 'members': {'__init__': {'value': {'type': 'Any', 'default': 'None', 'description': None}, 'height': {'type': 'int | None', 'default': 'None', 'description': None}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'info': {'type': 'str | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': None}, 'container': {'type': 'bool', 'default': 'True', 'description': None}, 'scale': {'type': 'int | None', 'default': 'None', 'description': None}, 'min_width': {'type': 'int | None', 'default': 'None', 'description': None}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': None}, 'visible': {'type': 'bool', 'default': 'True', 'description': None}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': None}, 'render': {'type': 'bool', 'default': 'True', 'description': None}, 'load_fn': {'type': 'Callable[..., Any] | None', 'default': 'None', 'description': None}, 'every': {'type': 'float | None', 'default': 'None', 'description': None}}, 'postprocess': {'value': {'type': 'str | None', 'description': None}}, 'preprocess': {'return': {'type': 'str', 'description': None}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': ''}, 'upload': {'type': None, 'default': None, 'description': ''}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'PDF': []}}}
    
abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_pdf`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_pdf/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_pdf"></a> <a href="https://github.com/freddyaboulton/gradio-pdf/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> <a href="https://huggingface.co/spaces/freddyaboulton/gradio_pdf/discussions" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/%F0%9F%A4%97%20Discuss-%23097EFF?style=flat&logoColor=black"></a>
</div>

Easily display PDFs in Gradio
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_pdf
```

## Usage

```python

import gradio as gr
from gradio_pdf import PDF
from pdf2image import convert_from_path
from transformers import pipeline
from pathlib import Path

dir_ = Path(__file__).parent

p = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa",
)

def qa(question: str, doc: str) -> str:
    img = convert_from_path(doc)[0]
    output = p(img, question)
    return sorted(output, key=lambda x: x["score"], reverse=True)[0]['answer']


demo = gr.Interface(
    qa,
    [gr.Textbox(label="Question"), PDF(label="Document")],
    gr.Textbox(),
    examples=[["What is the total gross worth?", str(dir_ / "invoice_2.pdf")],
              ["Whos is being invoiced?", str(dir_ / "sample_invoice.pdf")]]
)

if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `PDF`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["PDF"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["PDF"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function. 
- When used as an output, the component only impacts the return signature of the user function. 

The code snippet below is accurate in cases where the component is used as both an input and an output.



 ```python
def predict(
    value: str
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "PDF-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          PDF: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
        
        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()

```

## `PDF`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
typing.Any
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>height</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>info</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>container</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>load_fn</code></td>
<td align="left" style="width: 25%;">

```python
typing.Optional[typing.Callable[..., typing.Any]][
    typing.Callable[..., typing.Any][Ellipsis, typing.Any],
    None,
]
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">None</td>
</tr>

<tr>
<td align="left"><code>starting_page</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>1</code></td>
<td align="left">None</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` |  |
| `upload` |  |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, the preprocessed input data sent to the user's function in the backend.
- **As input:** Should return, the output data received by the component from the user's function in the backend.

 ```python
 def predict(
     value: str
 ) -> str | None:
     return value
 ```
 
