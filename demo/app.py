import gradio as gr
from gradio_pdf import PDF


with gr.Blocks() as demo:
    pdf = PDF(label="Upload a PDF", value='/Users/freddy/Documents/pdf_sample/sample_pdf.pdf', min_width="500%")

    name = gr.Textbox()
    pdf.upload(lambda f: f, pdf, name)

demo.launch()