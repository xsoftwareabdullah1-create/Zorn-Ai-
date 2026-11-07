# Zorn 1.1 — fine-tune a strong open-source coder on YOUR data + public coding data.
# pip install -U transformers peft datasets accelerate bitsandbytes
# Needs a GPU. 7B in 4-bit fits a 15 GB GPU; merging needs ~16+ GB system RAM (Kaggle/Colab Pro). Weak setup? use the 1.5B.
import gc, torch
from datasets import concatenate_datasets, load_dataset
from peft import LoraConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
from transformers import (AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
                          DataCollatorForLanguageModeling, Trainer, TrainingArguments)

BASE = "Qwen/Qwen2.5-Coder-7B-Instruct"   # "...-1.5B-Instruct" for small GPUs/phones, "...-32B-Instruct" for big GPUs
USE_4BIT = True                           # QLoRA
EXTRA_N = 3000                            # rows of public multi-language coding data to mix in (0 = off; check its license)
SYSTEM = ("You are Zorn 1.1, a smart AI assistant and coding agent. Always reply in English. "
          "First think step by step inside <think></think>, then give the final answer.")

bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
dtype = torch.bfloat16 if bf16 else torch.float16
tok = AutoTokenizer.from_pretrained(BASE)
q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=dtype) if USE_4BIT else None
model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=dtype, device_map="auto", quantization_config=q)
if USE_4BIT: model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, LoraConfig(r=32, lora_alpha=64, lora_dropout=0.05, task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]))
model.print_trainable_parameters()

own = load_dataset("json", data_files="zorn_data.jsonl")["train"]
parts = [own] * 3                         # repeat your data so Zorn's style sticks
if EXTRA_N:
    try:
        e = load_dataset("ise-uiuc/Magicoder-OSS-Instruct-75K", split="train").shuffle(seed=1).select(range(EXTRA_N))
        parts.append(e.map(lambda x: {"question": x["problem"],
                    "thinking": "Understand the task, choose a clean approach, then write complete, working code.",
                    "answer": x["solution"]}, remove_columns=e.column_names))
    except Exception as ex:
        print("Skipping public dataset:", ex)
ds = concatenate_datasets(parts).shuffle(seed=7)

def fmt(ex):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": ex["question"]},
            {"role": "assistant", "content": "<think>\n" + ex["thinking"] + "\n</think>\n" + ex["answer"]}]
    return tok(tok.apply_chat_template(msgs, tokenize=False), truncation=True, max_length=1536)
ds = ds.map(fmt, remove_columns=ds.column_names)

Trainer(model=model,
        args=TrainingArguments(output_dir="out", num_train_epochs=1, per_device_train_batch_size=1,
                               gradient_accumulation_steps=16, learning_rate=1e-4, logging_steps=10,
                               gradient_checkpointing=True, bf16=bf16, fp16=not bf16,
                               save_strategy="no", report_to="none"),
        train_dataset=ds, data_collator=DataCollatorForLanguageModeling(tok, mlm=False)).train()

model.save_pretrained("zorn-1.1-lora")
del model; gc.collect(); torch.cuda.empty_cache()
base = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=dtype, device_map="cpu")
merged = PeftModel.from_pretrained(base, "zorn-1.1-lora").merge_and_unload()
merged.save_pretrained("zorn-1.1"); tok.save_pretrained("zorn-1.1")
print("Saved your model to ./zorn-1.1")
