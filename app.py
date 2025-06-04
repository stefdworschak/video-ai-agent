import gradio as gr

def analyse_video(text):
    return {'text': text, 'analysis': 'This is a dummy analysis of the text.'}

server = gr.Interface(
    fn=analyse_video,
    inputs=gr.Textbox(placeholder="Enter text to analyze..."),
    outputs=gr.JSON(),
    title="Text video Analysis",
    description="Analyze the video of text using an agent"
)

if __name__ == "__main__":
    server.launch(mcp_server=True)

