import openai

class BiasDetectionAgent:
    def __init__(self, model_type, api_key):
        self.model = model_type
        self.api_key = api_key
        openai.api_key = api_key

    def detect_bias(self, text):
        prompt = f"Analyze the following text for potential biases and provide a detailed report:\n\n{text}\n\nConsider political or scientific biases in the way the information is presented. Highlight any tendencies towards specific viewpoints or agendas that may influence the interpretation of the content.\n\nPlease provide an analysis based on the detected biases and explain how they might impact the overall credibility or fairness of the information."
        
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
