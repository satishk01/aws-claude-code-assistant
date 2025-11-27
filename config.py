"""
Configuration management for the Claude Code Assistant
Supports both Anthropic and AWS Bedrock providers
"""
import os
from enum import Enum
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    BEDROCK = "bedrock"
    ANTHROPIC = "anthropic"


class Config(BaseModel):
    """Configuration settings for the assistant"""
    
    # LLM Provider settings
    llm_provider: LLMProvider = LLMProvider.BEDROCK  # Default to Bedrock
    
    # Anthropic settings
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # AWS Bedrock settings
    aws_region: str = "us-east-1"
    bedrock_model: str = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    # Common LLM settings
    temperature: float = 0.0
    max_tokens: int = 4096
    
    # Database settings
    checkpoint_db_path: str = "checkpoints.db"
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables"""
        config = cls()
        
        # Get provider from environment (default to bedrock)
        provider = os.getenv("LLM_PROVIDER", "bedrock").lower()
        if provider in ["anthropic", "claude"]:
            config.llm_provider = LLMProvider.ANTHROPIC
        else:
            config.llm_provider = LLMProvider.BEDROCK
        
        # Anthropic settings
        config.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        config.anthropic_model = os.getenv("ANTHROPIC_MODEL", config.anthropic_model)
        
        # AWS Bedrock settings
        config.aws_region = os.getenv("AWS_REGION", config.aws_region)
        config.bedrock_model = os.getenv("BEDROCK_MODEL", config.bedrock_model)
        
        # Common settings
        config.temperature = float(os.getenv("LLM_TEMPERATURE", config.temperature))
        config.max_tokens = int(os.getenv("LLM_MAX_TOKENS", config.max_tokens))
        
        return config
    
    def validate_provider_config(self) -> tuple[bool, str]:
        """
        Validate that the selected provider has required configuration
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.llm_provider == LLMProvider.ANTHROPIC:
            if not self.anthropic_api_key:
                return False, "ANTHROPIC_API_KEY is required when using Anthropic provider"
        
        elif self.llm_provider == LLMProvider.BEDROCK:
            # For Bedrock, we rely on AWS credentials (IAM role, profile, etc.)
            # No specific validation needed here as boto3 will handle it
            pass
        
        return True, ""
    
    def get_provider_display_name(self) -> str:
        """Get human-readable provider name"""
        if self.llm_provider == LLMProvider.ANTHROPIC:
            return f"Anthropic Claude ({self.anthropic_model})"
        elif self.llm_provider == LLMProvider.BEDROCK:
            return f"AWS Bedrock ({self.bedrock_model})"
        return "Unknown Provider"


# Global configuration instance
config = Config.from_env()