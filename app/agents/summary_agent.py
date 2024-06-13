import openai
import os

class SummaryAgent:
    def __init__(self, model_type, api_key):
        self.model = model_type
        self.api_key = api_key
        openai.api_key = api_key

    def compile_summary(self, bias_analysis, quality_analysis, sme_analysis):
        prompt = f"Compile a summary based on the analyses:\n\nBias Analysis:\n{bias_analysis}\n\nQuality Analysis:\n{quality_analysis}\n\nSME Analysis:\n{sme_analysis}"
        
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
