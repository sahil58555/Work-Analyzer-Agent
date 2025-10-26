#!/usr/bin/env python3
"""
Simple runner script for work_impact_agent
"""

from work_impact_agent import work_impact_agent

def main():
    print("Work Impact Agent Runner")
    print("="*50)
    
    # Get user input
    user_prompt = input("\nEnter your prompt (or press Enter for default): ").strip()
    
    if not user_prompt:
        user_prompt = "Please provide a leadership summary of my work."
    
    print(f"\nProcessing with prompt: {user_prompt}")
    print("="*50)
    
    try:
        response = work_impact_agent(user_prompt=user_prompt)
        
        if response:
            print("\n" + "="*80)
            print("GENERATED SUMMARY:")
            print("="*80)
            print(response)
        else:
            print("No response received from LLM")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()