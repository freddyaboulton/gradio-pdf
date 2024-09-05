
import gradio as gr
from gradio_pdf import PDF
from pathlib import Path

dir_ = Path(__file__).parent


def qa(question: str, doc: str) -> str:
    return doc


demo = gr.Interface(
    qa,
    [gr.Textbox(label="Question"), PDF(label="Document",
                                       value=str(dir_ / "sample_invoice.pdf"))],
    gr.Textbox(),
    examples=[["What is the total gross worth?", str(dir_ / "invoice_2.pdf")],
              ["Whos is being invoiced?", str(dir_ / "sample_invoice.pdf")]]
)

if __name__ == "__main__":
    demo.launch()