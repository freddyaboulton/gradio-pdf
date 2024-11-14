<h1 style='text-align: center; margin-bottom: 1rem'> Gradio PDF 📕 </h1>

<div style="display: flex; flex-direction: row; justify-content: center">
<img style="display: block; padding-right: 5px; height: 20px;" alt="Static Badge" src="https://img.shields.io/pypi/v/gradio_pdf"> 
<a href="https://github.com/freddyaboulton/gradio-pdf" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"></a>
</div>

Easily display PDFs in Gradio

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
Any
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
Callable[Ellipsis, Any] | None
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
 
