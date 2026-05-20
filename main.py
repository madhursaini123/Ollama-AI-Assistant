import requests
import json
import sys
import os 
from datetime import datetime

OLLAMA_API_URL = "http://localhost:11434/api/chat"

MODEL_NAME = "mistral"

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a helpful AI assistant created by Madhur Saini. "
        "you are helpful, witty, professional and love technology. "
        "You help with coding problems, interview preparation, and general knowledge questions. "
        "Keep responses clear and concise. "
        "If ask about yourself , explain that you run locally via Ollama. "
    )
}

class AI_Assistant:
    def __init__(self):
        self.conversation_history = []
        self.conversation_history.append(SYSTEM_PROMPT)
        self.running = True
        
    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        
    def chat(self, user_input):
        payload = {
            "model": MODEL_NAME,
            "messages": self.conversation_history,
            "stream": False,
            "options": {
                "temperature":0.7
            }
        }
        
        try:
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
            if response.status_code == 200:
                assisstant_reply = response.json()["message"]["content"]
                return assisstant_reply
            else:
                return f"[error]Ollama returned status {response.status_code}: {response.text}"
        except requests.exceptions.ConnectionError:
            return "[error] cannot connect to Ollama API. Is it running?(Try 'ollama run llama3' in terminal)"
        
        except Exception as e:
            return f"[error] {str(e)}"
        
    def save_conversation(self, filename=None):
        '''script_dir = os.path.dirname(os.path.abspath(__file__))
        save_dir = os.path.join(script_dir, "saved_conversations")
        
        os.makedirs(save_dir, exist_ok=True)
        
        if not os.access(save_dir, os.W_OK):
            print(f"[error] Cannot write to directory '{save_dir}'. Check permissions.")
            return'''
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"AI_Assistant_Conversation_{timestamp}.txt"
        
        filepath = os.path.join(desktop, filename)
            
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"AI Assistant Conversation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n")
                for msg in self.conversation_history:
                    if msg["role"] == "system":
                        continue
                    role_display = "You" if msg["role"] == "user" else "AI Assistant"
                    f.write(f"{role_display}: {msg['content']}\n\n")
                print(f"Conversation saved to {filepath}")
        except Exception as e:
            print(f"Failed to save conversation: {e}")
    
    def clear_history(self):
        self.conversation_history = [SYSTEM_PROMPT]
        print("Conversation history cleared.")
    
    def run(self):
        print("\n"+"="*60)
        print("AI assistant is ready! Type your message below.")
        print("="*60)
        print("/clear - reset conversation history")
        print("/save - save conversation to a text file")
        print("/exit - exit the program")
        print("="*60+"\n")
        
        while self.running:
            try:
                user_input = input("you:").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ["/exit", "quit"]:
                    print("Exiting... Goodbye!")
                    self.running = False
                    break
                
                elif user_input.lower() == "/clear":
                    self.clear_history()
                    continue
                
                elif user_input.lower() == "/save":
                    self.save_conversation()
                    continue
                
                self.add_message("user", user_input)
                print("AI Assistant: ", end="", flush=True)
                reply = self.chat(user_input)
                print(reply)
                self.add_message("assistant", reply)
                
            except KeyboardInterrupt:
                print("\nExiting... Goodbye!")
                break
            except EOFError:
                break


if __name__ == "__main__":
    try:
        test_req = requests.get("http://localhost:11434/api/tags", timeout=5)
        if test_req.status_code != 200:
            print("[error] Cannot connect to Ollama API. Is it running? (Try 'ollama run llama3' in terminal)", test_req.status_code)
            print("Start ollama in another application.")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("[error] Cannot connect to Ollama API.")
        sys.exit(1)
    except Exception as e:
        print(f"[error] {e}")
        sys.exit(1)
    
    assistant = AI_Assistant()
    assistant.run()