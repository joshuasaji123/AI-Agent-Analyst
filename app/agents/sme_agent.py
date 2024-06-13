import openai
import os

class SMEAgent:
    def __init__(self, model_type, api_key):
        self.model = model_type
        self.api_key = api_key
        openai.api_key = api_key

    def provide_insight(self, text):
        prompt = f"As a subject matter expert, provide insights and recommendations on the following text:\n\n{text}"
        
        if "gpt-" in self.model:
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "system", "content": prompt}]
                )
                return response['choices'][0]['message']['content'].strip()
            except Exception as e:
                return f"Error processing request: {str(e)}"
        else:
            try:
                response = openai.Completion.create(model=self.model, prompt=prompt)
                return response.choices[0].text.strip()
            except Exception as e:
                return f"Error processing request: {str(e)}"

    def _load_prompt(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f"Prompt file '{filepath}' not found."
