# AI-Agent-Analysis

## Overview

AI-Agent-Analysis is a comprehensive tool designed to process, analyze, and summarize text files using various AI models. It integrates multiple agents for bias detection, quality assessment, and subject matter expertise analysis.

## Features

- Bias Detection: Analyze text for potential biases.
- Quality Assessment: Evaluate the quality of the text.
- Subject Matter Expertise Analysis: Gain insights from a subject matter expert.
- Summary Compilation: Generate a summary report combining the results from different analyses.

## Requirements

- Python 3.8+
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:

   git clone https://github.com/joshuasaji123/Ai-Agent-Analysis.git
   cd Ai-Agent-Analysis

2. Install dependencies:

   pip install -r requirements.txt

3. Set up environment variables:

   Create a `.env` file in the root directory of the project and add your OpenAI API key:

   OPENAI_API_KEY=your_openai_api_key

## Usage

1. Prepare your text file:

   Ensure you have a text file (`text.txt`) placed in the `docs` folder of the project.

2. Run the project:

   python app/main.py

   The script will read the text file, segment it if necessary, and process it using the selected AI models. The results will be displayed in the console.

## Configuration

By default, the project uses the OpenAI model. You can specify the model type in the `app/main.py` file.

Example Configuration in `app/main.py`:

model_type = "gpt-4"  # OpenAI model

## Logging

The project includes logging to track the time taken for each analysis and to handle errors. Logs are written to `app.log`.

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push the branch to your fork.
4. Create a pull request describing your changes.

## License

This project is licensed under the MIT License.

## Acknowledgements

Special thanks to the developers of OpenAI for their powerful AI models.
