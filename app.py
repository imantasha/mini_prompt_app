import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize OpenAI client for Groq
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Function to generate response
def generate_response(mode, user_input):
    if not user_input.strip():
        return "⚠️ Please enter a topic or question."

    if mode == "Quiz":
        prompt = (
            f"Create a multiple choice quiz question on this topic: {user_input}.\n"
            "Include 4 answer options labeled A to D, and mention the correct answer."
        )
    elif mode == "Story":
        prompt = f"Write a fun and short story for kids about: {user_input}."
    elif mode == "Math":
        prompt = f"Solve this math problem with detailed steps: {user_input}."
    else:
        return "⚠️ Invalid mode selected."

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Mini Prompt App (Powered by Groq + LLaMA 3.3)")
    gr.Markdown("Choose a mode and enter a topic or question below:")

    mode = gr.Radio(choices=["Quiz", "Story", "Math"], label="Prompt Type", value="Story")
    user_input = gr.Textbox(label="Your Topic or Question", placeholder="E.g. A robot who loves to sing")

    output = gr.Textbox(label="Model Output", lines=10)

    submit_btn = gr.Button("Generate Response")
    submit_btn.click(generate_response, inputs=[mode, user_input], outputs=output)

    gr.Markdown("""
    ### 💡 Example Inputs:
    - Story: "A cat who goes to school"
    - Quiz: "Newton's laws of motion"
    - Math: "Simplify: (3x + 2)(x - 4)"
    """)

# Launch
if __name__ == "__main__":
    demo.launch()
