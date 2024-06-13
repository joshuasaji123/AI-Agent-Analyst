import os
import time
import openai
import logging
from dotenv import load_dotenv
from agents.bias_detection_agent import BiasDetectionAgent
from agents.quality_assessment_agent import QualityAssessmentAgent
from agents.sme_agent import SMEAgent
from agents.summary_agent import SummaryAgent

# Load environment variables from .env file
load_dotenv()

# Fetch the OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to read text from file
def read_text_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

# Function for waiting animation with metrics tracking
def waiting_animation(seconds, api_function, api_function_name, *args, **kwargs):
    try:
        start_time = time.time()
        response = api_function(*args, **kwargs)
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        print(f"{api_function_name} completed. Time Taken: {time_taken} s")
        logging.info(f"{api_function_name} took {time_taken} seconds.")
        return {"time_taken": time_taken, "result": response}
    except Exception as e:
        error_message = f"Error processing {api_function_name}: {str(e)}"
        print(error_message)
        logging.error(error_message)
        return {"time_taken": 0, "result": None}

def segment_and_process_text(text, max_tokens=8192):
    segments = []
    if len(text) <= max_tokens:
        segments.append(text)
    else:
        # Split text into segments of max_tokens length
        for i in range(0, len(text), max_tokens):
            segments.append(text[i:i+max_tokens])
    return segments

def main():
    # Assuming text.txt is in the docs folder
    text_filepath = "docs/text.txt"
    model_type = "gpt-4"  # Example model type

    # Read text from the file
    content = read_text_from_file(text_filepath)

    # Segment the content into parts that fit within the token limit
    text_segments = segment_and_process_text(content)

    # Display segmenting message if needed
    if len(text_segments) > 1:
        print("Segmenting in progress...")

    # Initialize agents
    bias_agent = BiasDetectionAgent(model_type, OPENAI_API_KEY)
    quality_agent = QualityAssessmentAgent(model_type, OPENAI_API_KEY)
    sme_agent = SMEAgent(model_type, OPENAI_API_KEY)
    summary_agent = SummaryAgent(model_type, OPENAI_API_KEY)

    # Perform analyses using each agent
    total_time = 0
    all_bias_results = []
    all_quality_results = []
    all_sme_results = []

    for segment in text_segments:
        bias_analysis = waiting_animation(3, bias_agent.detect_bias, "Bias Analysis", segment)
        if bias_analysis["result"]:
            all_bias_results.append(bias_analysis["result"])

        quality_analysis = waiting_animation(3, quality_agent.evaluate, "Quality Assessment", segment)
        if quality_analysis["result"]:
            all_quality_results.append(quality_analysis["result"])

        sme_analysis = waiting_animation(3, sme_agent.provide_insight, "SME Analysis", segment)
        if sme_analysis["result"]:
            all_sme_results.append(sme_analysis["result"])

        # Update total time with the maximum time taken among the analyses of this segment
        total_time += max(bias_analysis["time_taken"], quality_analysis["time_taken"], sme_analysis["time_taken"])

    # Combine results into a final comprehensive report
    final_bias_report = "\n\n".join(all_bias_results)
    final_quality_report = "\n\n".join(all_quality_results)
    final_sme_report = "\n\n".join(all_sme_results)

    full_report = f"""
    Full Report:
    
    Bias Analysis:
    {final_bias_report}
    
    Quality Assessment:
    {final_quality_report}
    
    SME Analysis:
    {final_sme_report}
    """

    print("Compiling summary...")
    summary = waiting_animation(3, summary_agent.compile_summary, "Summary Compilation", final_bias_report, final_quality_report, final_sme_report)
    if summary["result"]:
        total_time += summary["time_taken"]
        print(f"Summary: {summary['result']}\n")
        logging.info(f"Summary Output: {summary['result']}")
    else:
        print(f"Failed to compile Summary.\n")

    print(full_report)
    print(f"Total time taken: {total_time} seconds")

if __name__ == "__main__":
    main()
