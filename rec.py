import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
import openai

class recommendation:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Recommendations")
        self.root.geometry("350x400")
        self.root.tk.call("source", "./forest-dark.tcl")
        ttk.Style().theme_use("forest-dark")

        frame=ttk.Frame(self.root)
        frame.grid(row=0, column=1, padx=10)

        def giveReccomendation():
            obj = recommendation.giveRec()
            myLabel = ttk.Label(frame, text=obj, style="Accent.TLabel").gride(row=1, column=1)

        button = ttk.Button(frame, text="GET RECOMMENDATIONS", style="Accent.TButton", command=giveReccomendation).grid(row=0, column=1)
        ttk.Style().configure('TButton')

        self.root.update()
        sidebar = Sidebar(self.root)

        self.root.mainloop()

    def giveRec():
            openai.api_key = "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"
            file1 = open("C:/Users/Arushi/OneDrive/Desktop/Codefest/text1.txt","r").read()
            #print(file1)
            file2= open("C:/Users/Arushi/OneDrive/Desktop/Codefest/text2.txt","r").read()
            dataset = [file1, file2]

            # Define the model and the prompt
            model = "davinci"
            prompt = "Fine-tune the model to give similar results when asked for reccomendations on possible events to be conducted to be more environmentally conscious: "+ " | " .join(dataset)   

            # Fine-tune the model
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1,
            )

            # Print the generated text
            #print(response)
            return (response["choices"][0]["text"])

recommendation()