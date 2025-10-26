from openai import AzureOpenAI
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Azure OpenAI Setup ---
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
)

logger.info("Azure OpenAI client initialized successfully.")

def ask_llm(system_prompt: str, user_prompt: str, model: str = "gpt-4o") -> str:
    logger.info("Sending request to Azure OpenAI...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        logger.info("Received response from Azure OpenAI.")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error occurred while calling Azure OpenAI: {e}")
        return None