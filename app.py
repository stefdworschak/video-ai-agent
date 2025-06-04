import gradio as gr

def analyse_youtube(text):
    return {'text': text, 'analysis': 'This is a dummy analysis of the text.'}

demo = gr.Interface(
    fn=analyse_youtube,
    inputs=gr.Textbox(placeholder="Enter text to analyze..."),
    outputs=gr.JSON(),
    title="Text Youtube Analysis",
    description="Analyze the Youtube of text using an agent"
)

if __name__ == "__main__":
    demo.launch(mcp_server=True)

