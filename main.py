#!/usr/bin/env python3
"""
Main entry point for the Claude Code Assistant

A minimalist AI coding assistant using LangGraph and MCP
Supports both Anthropic and AWS Bedrock providers
"""
import asyncio
import sys
from agent import CodeAssistantAgent
from config import config
from rich.console import Console

console = Console()


async def main():
    """Main function to run the assistant"""
    
    # Validate configuration
    is_valid, error_msg = config.validate_provider_config()
    if not is_valid:
        console.print(f"[bold red]❌ Configuration Error: {error_msg}[/bold red]")
        
        if config.llm_provider.value == "anthropic":
            console.print("[yellow]Please set your Anthropic API key in .env file:[/yellow]")
            console.print("[yellow]ANTHROPIC_API_KEY=sk-ant-xxxxx[/yellow]")
            console.print("[yellow]Or switch to Bedrock by setting: LLM_PROVIDER=bedrock[/yellow]")
        else:
            console.print("[yellow]Please ensure AWS credentials are configured for Bedrock access[/yellow]")
            console.print("[yellow]You can use IAM roles, AWS profiles, or environment variables[/yellow]")
        
        sys.exit(1)
    
    # Display provider information
    console.print(f"[green]🤖 Using LLM Provider: {config.get_provider_display_name()}[/green]")
    
    # Initialize agent
    agent = CodeAssistantAgent()
    
    try:
        # Async initialization
        await agent.initialize()
        
        # Run the interactive loop
        await agent.run()
        
    except KeyboardInterrupt:
        console.print("\n[bold cyan]👋 Interrupted by user[/bold cyan]")
    except Exception as e:
        console.print(f"[bold red]❌ Fatal error: {e}[/bold red]")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        await agent.cleanup()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
