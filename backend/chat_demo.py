import json
import os
import sys
from dotenv import load_dotenv

# Ensure backend can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.scheme import Scheme
from backend.rag.vector_store import index_schemes
from backend.conversation.conversation_manager import ConversationManager

load_dotenv()

def main():
    print("=================================================")
    print("SCHEMECONNECT AI")
    print("Government Scheme Eligibility Assistant")
    print("=================================================")
    
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'schemes.json')
        
    with open(data_path, 'r') as f:
        schemes_data = json.load(f)
        
    all_schemes = [Scheme(**item) for item in schemes_data]
    index_schemes(all_schemes)
    
    manager = ConversationManager(all_schemes)
    
    print("\nAssistant:")
    print("I can help you find relevant government schemes. How can I help you today?")
    print("(Type 'quit' or 'exit' to stop)\n")
    
    while True:
        try:
            user_input = input("User:\n")
            if user_input.lower() in ['quit', 'exit']:
                break
                
            response = manager.process_message(user_input)
            print(f"\nAssistant:\n{response}\n")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
