import gradio as gr
from gradio_pdf import PDF
from pathlib import Path

dir_ = Path(__file__).parent.resolve()


def update_document(value: str, page: int):
    if value == "A17_FlightPlan":
        starting_page=50
    elif value == "dictionary":
        starting_page=10
    else:
        starting_page = 2
    return PDF(value=str(dir_ / f"{value}.pdf"), starting_page=page)


# with gr.Blocks() as demo:
#     with gr.Row():
#         with gr.Column():
#             dd = gr.Dropdown(choices=["A17_FlightPlan", "dictionary", "textbook"])
#             update = gr.Button("Update")
#         with gr.Column():
#             pdf = PDF()
    
#     update.click(update_document, dd, pdf)

# demo.launch()

gr.Interface(
    fn=update_document,
    inputs=[gr.Radio(["A17_FlightPlan", "dictionary", "textbook"], label="Select a PDF document"),
            gr.Number(value=1, minimum=1, maximum=1000, step=1)],
    outputs=PDF(),
    title="Update PDF",
).launch()