#!/usr/bin/env python3
"""
Test script to verify both LLM providers work correctly
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_config():
    """Test configuration loading"""
    print("🧪 Testing Configuration...")
    
    try:
        from config import config, LLMProvider
        print(f"✓ Configuration loaded successfully")
        print(f"  Provider: {config.llm_provider}")
        print(f"  Display Name: {config.get_provider_display_name()}")
        
        # Test validation
        is_valid, error_msg = config.validate_provider_config()
        if is_valid:
            print(f"✓ Configuration is valid")
        else:
            print(f"✗ Configuration error: {error_msg}")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_llm_initialization():
    """Test LLM initialization"""
    print("\n🤖 Testing LLM Initialization...")
    
    try:
        from agent import CodeAssistantAgent
        
        # Create agent (this will initialize the LLM)
        agent = CodeAssistantAgent()
        print(f"✓ Agent created successfully")
        print(f"✓ LLM initialized: {type(agent.llm).__name__}")
        
        return True
    except Exception as e:
        print(f"✗ LLM initialization failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    print("\n📦 Testing Dependencies...")
    
    dependencies = [
        ("langchain", "LangChain core"),
        ("langchain_anthropic", "Anthropic integration"),
        ("langchain_aws", "AWS Bedrock integration"),
        ("boto3", "AWS SDK"),
        ("langgraph", "LangGraph"),
        ("rich", "Rich terminal UI"),
        ("pydantic", "Pydantic models"),
    ]
    
    all_good = True
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"✓ {description}")
        except ImportError:
            print(f"✗ {description} - Missing!")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🚀 Claude Code Assistant - Provider Test Suite\n")
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Configuration", test_config),
        ("LLM Initialization", test_llm_initialization),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Results Summary:")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The assistant is ready to use.")
        print("\nTo start the assistant, run:")
        print("  uv run main.py")
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the configuration.")
        if not os.path.exists(".env"):
            print("\n💡 Tip: Copy .env.example to .env and configure your provider:")
            print("  cp .env.example .env")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)