
import gradio as gr
from gradio_pdf_redaction import PDF
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


EXAMPLES = [
    ["What is the total gross worth?", str(dir_ / "invoice_2.pdf")],
    ["Whos is being invoiced?", str(dir_ / "sample_invoice.pdf")],
]


def create_demo():
    return gr.Interface(
        qa,
        [gr.Textbox(label="Question"), PDF(label="Document")],
        gr.Textbox(),
        examples=EXAMPLES,
        cache_examples=False,
    )


# Required for `gradio cc dev` hot reload — must be a module-level Blocks/Interface.
demo = create_demo()

if __name__ == "__main__":
    demo.launch()
