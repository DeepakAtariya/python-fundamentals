# You will build a thin provider-agnostic wrapper so the same code can talk to OpenAI, Anthropic, and a local model (Ollama/Together), swapping with a config flag
import os

from dotenv import load_dotenv  # type: ignore
from openai import OpenAI

class ChatCompletionProvider:
    client: OpenAI | str
    def __init__(self, provider: str) -> None:
        self.provider = provider
    
    def createProvider(self) -> None: 
        provider = self.provider
        match provider:
            case "OpenAI":
                self.client = OpenAI(api_key=os.environ.get("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
            case "Anthropic":
                self.client = "Anthropic"
            case "Ollama" | "Together":
                self.client = provider
            case _:
                raise ValueError(f"Unsupported provider: {provider}")
            
    def invoke(self, input:str) ->str:

        match self.provider:
            case "OpenAI":
                self.client = OpenAI(api_key=os.environ.get("GROQ_API_KEY"), base_url="https://api.groq.com/openai/v1")
            case "Anthropic":
                self.client = "Anthropic"
            case "Ollama" | "Together":
                self.client = provider
            case _:
                raise ValueError(f"Unsupported provider: {provider}")
          
         
         
         return ''
            