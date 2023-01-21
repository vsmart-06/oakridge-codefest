#pip install openai
#key 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
import openai
class recommend:
    def __init__(self):
        openai.api_key = "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"
        file1 = open("/Users/asheera/Desktop/train/text1.txt","r").read()
        #print(file1)
        file2= open("/Users/asheera/Desktop/train/text2.txt","r").read()
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
        print(response["choices"][0]["text"])

ChatGPT()