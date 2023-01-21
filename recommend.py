import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
import openai
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

class Recommendation:
    def __init__(self, username: str):
        self.username = username
        self.root = tk.Tk()
        self.root.title("Recommendations")
        self.root.geometry("350x400")
        self.root.tk.call("source", "./oakridge-codefest/forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row = 0, column = 1, padx = 10)

        button = ttk.Button(self.frame, text = "Get Recommendations", style = "Accent.TButton", command = self.giveReccomendation)
        button.grid(row = 0, column = 1)

        self.root.update()
        sidebar = Sidebar(self.root, self.username)

        self.root.mainloop()
    
    def giveReccomendation(self):
        text = self.giverec()
        myLabel = ttk.Label(self.frame, text = text)
        myLabel.grid(row = 1, column = 1)

    def giverec(self):
        openai.api_key = API_KEY
        file1 = open("./oakridge-codefest/text1.txt","r").read()
        file2 = open("./oakridge-codefest/text2.txt","r").read()
        dataset = [file1, file2]

        model = "davinci"
        prompt = "Fine-tune the model to give similar results when asked for reccomendations on possible events to be conducted to be more environmentally conscious: " + " | " .join(dataset)   


        response = openai.Completion.create(
            engine = model,
            prompt = prompt,
            temperature = 0.5,
            max_tokens = 1024,
            top_p = 1,
            frequency_penalty = 1,
            presence_penalty = 1,
        )


        return response["choices"][0]["text"]