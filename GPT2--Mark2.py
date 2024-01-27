import tkinter as tk
import transformers
from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
import tensorflow as tf
import threading

# Monkey-patch the deprecated function
tf.losses.sparse_softmax_cross_entropy = tf.compat.v1.losses.sparse_softmax_cross_entropy

class Chatbot:
    def __init__(self):
        self.model, self.tokenizer = self.initialize_model_and_tokenizer()

    def initialize_model_and_tokenizer(self):
        model_name = "gpt2"
        try:
            model = TFGPT2LMHeadModel.from_pretrained(model_name)
            tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        except Exception as e:
            print(f"Error initializing model and tokenizer: {e}")
            return None, None
        return model, tokenizer

    def generate_response(self, prompt, max_length=50):
        input_ids = self.tokenizer.encode(prompt, return_tensors="tf")
        output_ids = self.model.generate(input_ids, max_length=max_length, num_return_sequences=1)
        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return response

class ChatbotGUI:
    def __init__(self, master, chatbot):
        self.master = master
        self.chatbot = chatbot

        master.title("Chatbot GUI")

        self.label = tk.Label(master, text="You:")
        self.label.pack()

        self.user_input = tk.Entry(master)
        self.user_input.pack()

        self.chatbox = tk.Text(master, height=10, width=40)
        self.chatbox.pack()

        self.exit_button = tk.Button(master, text="Exit", command=self.master.destroy)
        self.exit_button.pack()

        self.chat_button = tk.Button(master, text="Chat", command=self.chat)
        self.chat_button.pack()

    def chat(self):
        user_input = self.user_input.get()
        if user_input.lower() == 'exit':
            self.master.destroy()
            return

        threading.Thread(target=self.chat_with_model, args=(user_input,), daemon=True).start()

    def chat_with_model(self, user_input):
        response = self.chatbot.generate_response(user_input)
        self.master.after(0, lambda: self.update_chatbox(user_input, response))
        self.user_input.delete(0, tk.END)

    def update_chatbox(self, user_input, response):
        self.chatbox.insert(tk.END, "You: " + user_input + "\n")
        self.chatbox.insert(tk.END, "ChatGPT: " + response + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    chatbot = Chatbot()
    app = ChatbotGUI(root, chatbot)
    root.mainloop()