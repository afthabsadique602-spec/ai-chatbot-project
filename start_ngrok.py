import sys
from pyngrok import ngrok

try:
    public_url = ngrok.connect(5000)
    print("SUCCESS: ", public_url)
    
    # Keep the script running
    ngrok_process = ngrok.get_ngrok_process()
    ngrok_process.proc.wait()
except Exception as e:
    print(f"FAILED: {e}")
