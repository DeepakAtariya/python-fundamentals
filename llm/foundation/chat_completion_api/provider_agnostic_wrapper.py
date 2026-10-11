# You will build a thin provider-agnostic wrapper so the same code can talk to OpenAI, Anthropic, and a local model (Ollama/Together), swapping with a config flag

class ChatCompletionProvider:
    def __init__(self, provider: str) -> None:
        self.provider = provider
    
    def createProvider(self):
        provider = self.provider
        match provider:
            case "OpenAI":
                return "OpenAI"
            case "Anthropic":
                return "Anthropic"
            case "Ollama" | "Together":
                return provider
            case _:
                raise ValueError(f"Unsupported provider: {provider}")
    
    
                
            