# zorn.ai / Zorn 1.1

Your own AI coding assistant: your own fine-tuned model, a chat UI with Google login and file/ZIP attachments, and no third-party API key.

## How it works
```
Phone / PC browser  ->  server.js (Google login check, daily limits)  ->  zorn_serve.py (your Zorn 1.1 model)
      public/index.html                  port 3000                              port 8000
```
- `model/train_zorn.py` fine-tunes an open-source coding model (Qwen2.5-Coder) on `model/zorn_data.jsonl` (325+ examples) plus public coding data. The result is the folder `zorn-1.1/`.
- `model/zorn_serve.py` serves that model on an OpenAI-style endpoint (`/v1/chat/completions`).
- `server.js` verifies the Google login, enforces a daily limit per user, and forwards chats to the model.
- `public/index.html` is the mobile-friendly chat UI. `public/lite.html` is a tiny rule-based version with no model.

## Setup (in order)
1. **Train** (GPU needed, e.g. Google Colab or Kaggle): upload the `model/` folder, then
   `pip install -U transformers peft datasets accelerate bitsandbytes` and `python train_zorn.py`.
   Weak GPU? Set `BASE` to the 1.5B model in `train_zorn.py`. The output is `zorn-1.1/`.
2. **Serve the model**: `pip install flask transformers torch accelerate`, then `python zorn_serve.py` (port 8000).
3. **Google login**: in Google Cloud Console create an OAuth Client ID (Web). Add your site URL (for example `http://localhost:3000`) to Authorized JavaScript origins.
4. **Start the app**: `npm install`, then set the variables from `.env.example` and run `npm start`. Open `http://localhost:3000`.

## Using it on a phone
- **Option A: phone as the screen (easiest).** Run the server on a PC or a cloud GPU server. On the phone open `http://<server-ip>:3000` (same Wi-Fi) or your deployed HTTPS URL, then use the browser menu "Add to Home screen". Google login needs an authorized HTTPS (or localhost) origin, so deploy behind HTTPS for real phone use.
- **Option B: the model runs on the phone (offline).** Run `bash model/export_for_mobile.sh` to make `zorn-1.1-q4.gguf`, copy it to the phone, and load it in a GGUF app such as PocketPal AI. Paste the system prompt from `model/Modelfile`. Best with the 1.5B model; expect slow replies on older phones. In this mode there is no Google login or attachment button, because those belong to the web app.

## Attachments
Tap the paperclip to attach text or code files (up to 1 MB each) or a `.zip` (up to 20 MB; up to 40 readable files, skipping `node_modules`, `.git`, builds and binaries). The file text is added to your message. About 24,000 characters per message are sent, so long files are truncated. Images, audio, video, PDFs and other binary files are not supported, because the model is text-only.

## Notes
- The model answers from what it learned in training; it can make mistakes. Always test its code.
- Check the license of any public dataset and base model you use, especially for commercial use.
- `DAILY_LIMIT` (default 100) caps messages per user per day. CPU-only servers will be very slow with a 7B model.
- Extend the dataset by adding rows to `model/gen_*.py` (or directly to `zorn_data.jsonl`) and retraining.
