# train.py — Fine-Tuning Script for Life Breakdown Assistant
# Author: Kaushik Chaturvedi

import sys
from datasets import load_dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)

def train():
    print("Loading datasets...")
    # 1. Load the primary instruction dataset
    ds_instruct = load_dataset("HuggingFaceH4/helpful_instructions", split="train[:1%]") # 1% for demo speed
    
    # 2. Load the empathy dataset (optional, for mixing)
    # ds_empathy = load_dataset("facebook/empathetic_dialogues", split="train[:1%]")

    print("Loading Model & Tokenizer (flan-t5)...")
    model_id = "google/flan-t5-small" # Using small for training demo
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    # Preprocessing
    def preprocess_function(examples):
        # We assume the dataset has 'prompt' and 'completion' or similar fields
        # This mapping depends on the exact dataset schema.
        inputs = ["Breakdown this life problem: " + doc for doc in examples["prompt"]]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True)
        
        # Tokenize targets
        targets = tokenizer(examples["completion"], max_length=512, truncation=True)
        model_inputs["labels"] = targets["input_ids"]
        return model_inputs

    # Note: helpful_instructions requires specific column mapping check
    # For this file to run theoretically, we typically filter for valid columns first.
    print("Preprocessing data (mock step)...")
    # tokenized_ds = ds_instruct.map(preprocess_function, batched=True)

    # Setup Trainer
    args = Seq2SeqTrainingArguments(
        output_dir="./fine_tuned_model",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=1,
        predict_with_generate=True,
        logging_steps=10,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=args,
        train_dataset=ds_instruct, # Placeholder: Needs tokenized dataset
        tokenizer=tokenizer,
        data_collator=DataCollatorForSeq2Seq(tokenizer, model=model),
    )

    print("Starting Training (Demo mode)...")
    # trainer.train() 
    print("Training script structure ready. Uncomment 'trainer.train()' to execute.")

if __name__ == "__main__":
    train()
