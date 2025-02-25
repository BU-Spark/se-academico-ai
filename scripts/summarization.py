# SE-ACADMICO-AI/scripts/summarization.py

from paperqa import Settings, ask

import os
os.environ["OPENAI_API_KEY"] = "EMPTY"


'''
This script uses the paper-qa library to answer questions about a given paper.
Put the paper in the papers folder and run the script.
Refer to the paper-qa documentation for more information.
https://github.com/Future-House/paper-qa?tab=readme-ov-file#where-do-i-get-papers
Default model is openai-4.0
'''


local_llm_config = {
    "model_list": [
        {
            "model_name": "ollama/llama3.2",
            "litellm_params": {
                "model": "ollama/llama3.2",
                "api_base": "http://localhost:11434",
               
            },
        }
    ]
}

answer_response = ask(
    "What are the challenges this essay addressed?",
    settings=Settings(
        llm="ollama/llama3.2",
        llm_config=local_llm_config,
        summary_llm="ollama/llama3.2",
        summary_llm_config=local_llm_config,
        embedding="ollama/mxbai-embed-large",
        embedding_config=local_llm_config,
        
        paper_directory="./papers",
    ),
)

