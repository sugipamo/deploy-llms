from fastapi import FastAPI
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from pydantic import BaseModel
import os

# FastAPIアプリケーションの作成
app = FastAPI()

# Hugging Faceトークンを環境変数から取得
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN environment variable is not set!")

# Hugging Face Hubにログイン
try:
    login(hf_token)
    print("Successfully logged in to Hugging Face.")
except Exception as e:
    print(f"Failed to log in to Hugging Face: {e}")
    raise

# モデルとトークナイザーの読み込み
model_name = "google/gemma-2-2b-jpn-it"  # Hugging Face Hubのモデル名
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)

@app.get("/")
def read_root():
    return {"message": "Gemma-2-2b-jpn-it server is running!"}

class PromptRequest(BaseModel):
    prompt: str
    max_length: int = 200  # デフォルト値を指定
    min_length: int = 50   # デフォルト値を指定
    temperature: float = 0.7
    top_k: int = 50
    top_p: float = 0.9

@app.post("/generate/")
def generate_text(request: PromptRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=request.max_length,
        min_length=request.min_length,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        do_sample=True  # サンプリングを有効化
    )
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": generated_text}
