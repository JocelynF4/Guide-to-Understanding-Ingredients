# test_setup.py — confirms all libraries installed and API key loads
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Test 1: import every library we'll need
import cv2                          # webcam control
import streamlit                    # UI framework
import openai                       # OpenAI API
from PIL import Image               # image handling
from dotenv import load_dotenv      # reads .env file
import os                           # lets us grab environment variables
import base64                       # for encoding images later
import io                           # for keeping images in memory (not disk)

print("✅ All libraries imported successfully")

# Test 2: load the API key from .env
load_dotenv()                                        # reads your .env file
api_key = os.getenv("OPENAI_API_KEY")               # grabs the key value

if api_key and api_key.startswith("sk-"):           # quick sanity check
    print("✅ API key loaded from .env correctly")
else:
    print("❌ API key not found or looks wrong — check your .env file")

# Test 3: confirm versions
print(f"✅ OpenCV version: {cv2.__version__}")
print(f"✅ Streamlit version: {streamlit.__version__}")
print(f"✅ OpenAI SDK version: {openai.__version__}")

print("\n🎉 Phase 1 complete — ready to build!")