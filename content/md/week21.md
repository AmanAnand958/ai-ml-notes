WEEK 21 · DAY 150
# vLLM & PagedAttention
High-Throughput LLM Serving
⏳ 50 mins
Difficulty: Hard
💬 Hinglish Explanation:
💡 Gotcha: KV Cache Memory Grows Linearly with Sequence Length & Batch Size
In standard transformer inference, storing Key and Value tensors for past tokens requires $2 \times 2 \times n_{\text{layers}} \times n_{\text{heads}} \times d_{\text{head}} \times s$ bytes per token. For long sequences ($s=32k$) and large batches, KV Cache VRAM consumption far exceeds the model weight VRAM! Use vLLM's PagedAttention to eliminate memory fragmentation.
### 🎯 By the end of Day 150, you will:
- Calculate the VRAM footprint of the KV Cache memory bottleneck.
- Serve an LLM using vLLM.
#### 🚦 Before You Start Checklist:
- Linux environment with GPU
## 🧠 Theory
Analogy:
vLLM & PagedAttention
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### PagedAttention
During LLM generation, the Keys and Values of attention are cached. Normally, this memory is pre-allocated and mostly wasted (fragmentation). PagedAttention manages this memory like OS virtual memory (pages), allowing near zero waste and huge batch sizes.
> Diagram: Traditional contiguous KV cache with wasted space versus PagedAttention mapping logical pages to scattered physical blocks

*Paging turns memory fragmentation into free slots that other sequences can use*
*PagedAttention = virtual memory for the KV cache*
python
```python
# Running an OpenAI-compatible server using vLLM
# In your terminal:
# vllm serve --model mistralai/Mistral-7B-Instruct-v0.1 --gpu-memory-utilization 0.9 --max-model-len 4096

# Accessing it via OpenAI Python Client:
from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="EMPTY"
)

response = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    messages=[{"role": "user", "content": "Explain PagedAttention."}],
)
print(response.choices[0].message.content)
```
### 🤔 Predict the Output
What happens if `gpu-memory-utilization` is set to 1.0?
Check
## ⚡ Tasks
**Task 1: Offline Batch Inference · MEDIUM · ⏱ 45 mins**
Write a script using vLLM's `LLM` class for offline batch generation (no server).
**Bonus Task: Benchmark Throughput · MEDIUM · MED · ⏱ 45 mins**
Using locust or a simple loop, compare requests/sec for HuggingFace pipeline vs vLLM with 10 concurrent requests.
**Task**
## 🧪 Day 150 Knowledge Check
**Q:** What problem does PagedAttention solve?
  - Network latency
  - KV Cache memory fragmentation
  - GPU compute speed
## 🧪 Applied Extension Checks
**Q:** Concept check — for vLLM & PagedAttention, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling vLLM & PagedAttention.
  - B) Adopt vLLM & PagedAttention without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing vLLM & PagedAttention?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for vLLM & PagedAttention?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** vLLM
> An open-source library for fast LLM inference and serving.
**Flashcard:** PagedAttention
> Divides KV cache into blocks (pages) to eliminate memory fragmentation.
**Flashcard:** Continuous Batching
> vLLM's ability to add new requests to an in-progress batch without waiting for all sequences to finish.
### ✅ Key Takeaways
"Never use `transformers` pipelines in production APIs. Always use vLLM or TGI."
- KV Cache grows linearly with sequence length.
- vLLM enables massive concurrent batching.
## 📚 Recommended Resources
⚡
#### vLLM Blog
Original PagedAttention blog post
WEEK 21 · DAY 151
# FlashAttention & Speculative Decoding
Hardware-Aware Optimizations
⏳ 50 mins
Difficulty: Hard
💬 Hinglish Explanation:
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### 🎯 By the end of Day 151, you will:
- Implement and evaluate the GPU memory hierarchy.
- Implement and evaluate Speculative Decoding mechanics.
#### 🚦 Before You Start Checklist:
- Knowledge of standard Self-Attention
## 🧠 Theory
Analogy:
FlashAttention & Speculative Decoding
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### FlashAttention-2
Standard attention materializes an N x N matrix in HBM (slow). FlashAttention computes attention using tiling to fit blocks into SRAM (fast) and never writes the full N x N matrix.
python
```python
# HuggingFace transformers natively supports FlashAttention-2
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1", 
    torch_dtype=torch.bfloat16, 
    attn_implementation="flash_attention_2", # Requires Ampere GPU or newer
    device_map="auto"
)
```
### Speculative Decoding
A smaller, faster "draft" model guesses the next K tokens. The large "target" model verifies all K tokens in a single parallel forward pass. Correct tokens are kept; incorrect ones are rejected and regenerated.
### 🤔 Predict the Output
Does Speculative Decoding change the final output of the large model?
Check
## ⚡ Tasks
**Task 1: vLLM Speculative Setup · MEDIUM · EASY · ⏱ 45 mins**
Write the CLI argument for running vLLM with speculative decoding using `speculator` model.
**Bonus Task: Measure Attention FLOPs · MEDIUM · HARD · ⏱ 45 mins**
Calculate the theoretical FLOPs for attention on a sequence of 4096 tokens with embedding dim 4096. Show working.
**Task**
## 🧪 Day 151 Knowledge Check
**Q:** What hardware constraint does FlashAttention overcome?
  - GPU Compute (FLOPS) limit
  - GPU Memory Bandwidth (HBM) IO limit
  - CPU Clock Speed
## 🧪 Applied Extension Checks
**Q:** Concept check — for FlashAttention & Speculative Decoding, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling FlashAttention & Speculative Decoding.
  - B) Adopt FlashAttention & Speculative Decoding without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing FlashAttention & Speculative Decoding?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for FlashAttention & Speculative Decoding?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** Speculative Decoding
> Drafting K tokens with a small model, verifying in 1 parallel pass with a large model. Lossless speedup!
**Flashcard:** Tiling (FlashAttention)
> Computing attention block-by-block in fast SRAM instead of writing the full N x N matrix to slow HBM.
**Flashcard:** Draft Model (Speculative)
> A smaller, fast model that proposes K tokens speculatively for the large model to verify in one pass.
### ✅ Key Takeaways
"LLM generation is memory-bound, not compute-bound. FlashAttention fixes training, Speculative Decoding fixes generation!"
- FlashAttention is mathematically exact.
- Speculative decoding only gives speedups if the draft model is highly accurate but much smaller.
## 📚 Recommended Resources
🤗
#### HF Inference Docs
Optimizing GPU inference
WEEK 21 · DAY 152
# Quantization
AWQ, GPTQ, GGUF & Llama.cpp
⏳ 50 mins
Difficulty: Medium
💬 Hinglish Explanation:
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### 🎯 By the end of Day 152, you will:
- Implement Post-Training Quantization (PTQ).
- Run models using `llama.cpp` on CPU/Mac.
#### 🚦 Before You Start Checklist:
- Understanding of FP16 vs INT4
## 🧠 Theory
Analogy:
Quantization
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### Quantization Formats
- **GPTQ / AWQ:** Designed for GPU inference. AWQ (Activation-aware Weight Quantization) protects "salient" weights to minimize accuracy loss.
- **GGUF:** The format used by `llama.cpp`. Optimized for CPU/Apple Silicon (M1/M2/M3) inference.
python
```python
# Running AWQ in vLLM
# vllm serve \
# --model mistralai/Mistral-7B-Instruct-v0.2 \
# --quantization awq

# Using llama-cpp-python in code
from llama_cpp import Llama
llm = Llama(
    model_path="./mistral-7b-instruct-v0.1.Q4_K_M.gguf",  
    n_gpu_layers=-1, # Offload everything to GPU if available (Metal on Mac)
    n_ctx=2048,
)
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32)
print(output['choices'][0]['text'])
```
### 🤔 Predict the Output
A 7B parameter model in FP16 takes ~14GB VRAM. Roughly how much VRAM does it take in INT4?
Check
## ⚡ Tasks
**Task 1: BitsAndBytes in Transformers · MEDIUM · ⏱ 45 mins**
Write a script to load a model in 4-bit precision using HuggingFace `bitsandbytes`.
**Task**
## 🧪 Day 152 Knowledge Check
**Q:** Which format is best for running LLMs on a MacBook M3?
  - GPTQ
  - GGUF (via llama.cpp)
  - AWQ
## 🧪 Applied Extension Checks
**Q:** Concept check — for Quantization, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling Quantization.
  - B) Adopt Quantization without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing Quantization?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for Quantization?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** AWQ
> Activation-aware Weight Quantization. Only quantizes weights that don't heavily impact activations. GPU focused.
**Flashcard:** llama.cpp
> A C/C++ port of LLMs highly optimized for CPU inference and Apple Metal.
**Flashcard:** Q4_K_M
> A GGUF quantization variant: 4-bit weights with a mixed k-quants strategy for best quality/speed.
### ✅ Key Takeaways
"Quantization lets you run state-of-the-art models on consumer hardware with minimal accuracy loss."
- The Bloke (HuggingFace) provides pre-quantized versions of almost all models.
- 4-bit quantization reduces memory by roughly 75%.
## 📚 Recommended Resources
🦙
#### llama.cpp Github
CPU Inference Engine
WEEK 21 · DAY 153
# QLoRA & PEFT
Parameter-Efficient Fine-Tuning
⏳ 60 mins
Difficulty: Hard
💬 Hinglish Explanation:
💡 Gotcha: QLoRA Target Modules Selection
When applying QLoRA, target only the Attention linear layers (`q_proj`, `v_proj`) by default for minimal memory. However, targeting all linear layers (including MLP projections) yields significantly higher task fine-tuning performance at a slight increase in trainable parameters.
### 🎯 By the end of Day 153, you will:
- Derive the dimensions for Low-Rank Adaptation (LoRA) math.
- Implement a QLoRA training script using TRL.
#### 🚦 Before You Start Checklist:
- Basic PyTorch knowledge
## 🧠 Theory
Analogy:
QLoRA & PEFT
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### LoRA Math
Instead of updating a huge weight matrix $W$, we freeze $W$ and add a low-rank decomposition $A \times B$.
Where $W \in \mathbb{R}^{d \times k}$, $A \in \mathbb{R}^{d \times r}$, $B \in \mathbb{R}^{r \times k}$. Rank $r$ is very small (e.g., 16).
### QLoRA Setup
python
```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from trl import SFTTrainer

# 1. Load Base Model in 4-bit
bnb_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf", quantization_config=bnb_config)

# 2. Setup LoRA Config
peft_config = LoraConfig(
    r=16, 
    lora_alpha=32, 
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# 3. Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    dataset_text_field="text",
    max_seq_length=512,
    args=training_args,
)
trainer.train()
```
### 🤔 Predict the Output
After training, how do we get the final deployable model?
Check
## ⚡ Tasks
**Task 1: Merging LoRA Weights · MEDIUM · ⏱ 45 mins**
Write the script to merge the trained LoRA adapter back into the base model.
**Bonus Task: Inspect Trainable Params · MEDIUM · MED · ⏱ 45 mins**
After get_peft_model(), call model.print_trainable_parameters() and verify it is <1% of total params for r=16.
**Task**
## 🧪 Day 153 Knowledge Check
**Q:** Why is `lora_alpha` important in the configuration?
  - It acts as a scaling factor for the adapter weights against the base weights
  - It determines the learning rate
  - It defines the rank of the matrix
## 🧪 Applied Extension Checks
**Q:** Concept check — for QLoRA & PEFT, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling QLoRA & PEFT.
  - B) Adopt QLoRA & PEFT without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing QLoRA & PEFT?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for QLoRA & PEFT?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** LoRA
> Low-Rank Adaptation. Freezes base weights, trains tiny A and B matrices.
**Flashcard:** QLoRA
> Quantized LoRA. Base model is in 4-bit, adapters are in 16-bit. Drastically reduces training VRAM.
**Flashcard:** r (LoRA Rank)
> The inner dimension of LoRA matrices. Higher r = more trainable params, more expressiveness, higher RAM usage.
### ✅ Key Takeaways
"QLoRA makes fine-tuning 7B-13B models accessible to anyone with a 24GB GPU!"
- Target `q_proj` and `v_proj` first, but targeting all linear layers yields better results.
- Adapters are tiny (e.g. 50MB) and easily swappable at inference time.
## 📚 Recommended Resources
🤗
#### TRL Docs
Supervised Fine-tuning Trainer
WEEK 21 · DAY 154
# DPO, ORPO & GRPO
Alignment without Reward Models
⏳ 50 mins
Difficulty: Hard
💬 Hinglish Explanation:
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### 🎯 By the end of Day 154, you will:
- Implement and evaluate Direct Preference Optimization (DPO).
- Implement and evaluate ORPO and GRPO (DeepSeek's method).
#### 🚦 Before You Start Checklist:
- practical application with SFT (Supervised Fine Tuning)
## 🧠 Theory
Analogy:
DPO, ORPO & GRPO
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### DPO (Direct Preference Optimization)
Instead of PPO (Reinforcement Learning), DPO uses a reference model to mathematically optimize the policy directly based on a dataset of `(prompt, chosen, rejected)` triplets.
python
```python
from trl import DPOTrainer
from transformers import TrainingArguments

# Dataset requires columns: prompt, chosen, rejected
training_args = TrainingArguments(output_dir="./dpo_model", per_device_train_batch_size=4)

dpo_trainer = DPOTrainer(
    model,                 # The model we are training
    model_ref,             # The frozen reference model (usually the SFT model)
    args=training_args,
    beta=0.1,              # Temperature parameter for DPO loss
    train_dataset=dataset,
    tokenizer=tokenizer,
)
dpo_trainer.train()
```
### ORPO (Odds Ratio Preference Optimization)
ORPO combines SFT and DPO into a single step! It penalizes rejected responses directly in the SFT loss, eliminating the need for a reference model.
### 🤔 Predict the Output
What is a major hardware advantage of ORPO over DPO?
Check
## ⚡ Tasks
**Task 1: DPO Formatting · MEDIUM · EASY · ⏱ 45 mins**
Format a raw dataset entry into the structure required by DPOTrainer.
**Task**
## 🧪 Day 154 Knowledge Check
**Q:** What does the Beta parameter control in DPO?
  - How much the model is allowed to deviate from the reference model
  - The learning rate multiplier
  - The number of training epochs
## 🧪 Applied Extension Checks
**Q:** Concept check — for DPO, ORPO & GRPO, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling DPO, ORPO & GRPO.
  - B) Adopt DPO, ORPO & GRPO without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing DPO, ORPO & GRPO?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for DPO, ORPO & GRPO?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** DPO
> Direct Preference Optimization. Aligns models using chosen/rejected pairs without RLHF. Requires a frozen reference model.
**Flashcard:** ORPO
> Odds Ratio Preference Optimization. Does SFT and Alignment in one step without a reference model.
**Flashcard:** GRPO
> Group Relative Policy Optimization. Used by DeepSeek-R1 for chain-of-thought reasoning training without a reference model.
### ✅ Key Takeaways
"Alignment is what turns a base text-predictor into a helpful assistant. DPO made alignment accessible."
- DPO is the industry standard replacing RLHF.
- GRPO (Group Relative Policy Optimization) is used by DeepSeek R1 for massive scale reasoning reinforcement.
## 📚 Recommended Resources
📄
#### DPO Paper
Direct Preference Optimization
WEEK 21 · DAY 155
# Synthetic Data & Deduplication
Data Engineering for LLMs
⏳ 45 mins
Difficulty: Medium
💬 Hinglish Explanation:
💡 Gotcha: Feature Store Training-Serving Skew
Training-serving skew happens when feature logic defined in training pipelines differs from real-time online serving logic. Use a unified Feature Store (like Feast) to guarantee consistent point-in-time joins.
### 🎯 By the end of Day 155, you will:
- Generate synthetic conversational data via LLMs.
- Deduplicate data using MinHash / LSH.
#### 🚦 Before You Start Checklist:
- Knowledge of Jaccard Similarity
## 🧠 Theory
Analogy:
Synthetic Data & Deduplication
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### Deduplication using Datasketch
Exact deduplication is easy. But fuzzy deduplication (finding almost similar texts) requires MinHash and Locality Sensitive Hashing (LSH) to scale over millions of rows.
python
```python
from datasketch import MinHash, MinHashLSH

# Create an LSH index
lsh = MinHashLSH(threshold=0.8, num_perm=128)

def get_minhash(text):
    m = MinHash(num_perm=128)
    for word in text.split():
        m.update(word.encode('utf8'))
    return m

m1 = get_minhash("How to cook pasta in boiling water")
m2 = get_minhash("How to cook pasta with boiling water")

lsh.insert("m1", m1)
result = lsh.query(m2)
print("Duplicates found:", result) # Returns ['m1']
```
### 🤔 Predict the Output
Why do we use MinHash instead of calculating Cosine Similarity for every pair?
Check
## ⚡ Tasks
**Task 1: Magpie Approach · MEDIUM · ⏱ 45 mins**
Write a system prompt to generate high-quality instruction data (like Magpie/Evol-Instruct).
**Bonus Task: Quality Filter · MEDIUM · MED · ⏱ 45 mins**
Write a script that uses an LLM to score each generated instruction 1-5 for complexity and filter out scores below 3.
**Task**
## 🧪 Day 155 Knowledge Check
**Q:** What does the `threshold` parameter in MinHashLSH control?
  - The maximum number of characters allowed
  - The minimum Jaccard similarity to be considered a duplicate
  - The batch size for processing
## 🧪 Applied Extension Checks
**Q:** Concept check — for Synthetic Data & Deduplication, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling Synthetic Data & Deduplication.
  - B) Adopt Synthetic Data & Deduplication without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing Synthetic Data & Deduplication?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for Synthetic Data & Deduplication?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** MinHash
> A probabilistic data structure used to quickly estimate the Jaccard similarity between two sets.
**Flashcard:** Synthetic Data
> Data generated by a larger, smarter LLM (Teacher) to train a smaller LLM (Student).
**Flashcard:** Evol-Instruct
> A method to create complex training data by prompting GPT-4 to evolve simple instructions (make harder, add constraints).
### ✅ Key Takeaways
"A model is only as good as its data. 1,000 high-quality, deduped examples > 100,000 messy ones."
- Duplicates in training data cause catastrophic memorization and overfitting.
- Synthetic data must be filtered for "AI-isms" (e.g., "As an AI language model...").
## 📚 Recommended Resources
🧹
#### Datasketch
Python library for MinHash LSH
WEEK 21 · DAY 156
# Capstone: Deploying a Custom Fine-Tuned Model
Data Prep -> QLoRA -> Merge -> vLLM Server
⏳ 120 mins
Difficulty: CAPSTONE
💬 Hinglish Explanation:
💡 Gotcha: Common Pitfalls in Day-156
Always validate underlying data assumptions, check tensor shape alignments, and verify hyperparameter scaling before running production training or evaluation loops.
### 🎯 By the end of Day 156, you will:
- Execute a full lifecycle LLM deployment.
- Serve your fine-tuned model via API.
#### 🚦 Before You Start Checklist:
- Reviewed Days 150-155
- Google Colab Pro / RunPod account
## 🧠 Theory
Analogy:
Capstone: Deploying a Custom Fine-Tuned Model
💡 Gotcha & Common Pitfall Warning:
Always double check tensor dimensions, verify data types before matrix operations, and ensure feature scaling is fitted strictly on the training set to prevent data leakage.
### The Lifecycle
```mermaid
graph LR
                    A[Raw Data] --> B[MinHash Dedup]
                    B --> C[ChatML Formatting]
                    C --> D[QLoRA SFT]
                    D --> E[Merge Weights]
                    E --> F[vLLM Inference]
```
python
```python
# Final Deployment Checklist Command
# After merging weights, run:
# vllm serve \
#   --model ./my-finetuned-llama3 \
#   --tensor-parallel-size 1 \
#   --max-model-len 4096 \
#   --dtype auto
```
### 🤔 Predict the Output
Why do we use ChatML format ( `<|im_start|>user\n...<|im_end|>` ) during fine tuning?
Check
## ⚡ Tasks
**Task 1: Full Implementation Pipeline · MEDIUM · CAPSTONE · ⏱ 45 mins**
Create a Colab notebook for the dataset generation, TRL training loop, model merge, and Gradio chat interface; run each stage and record the outputs.
**Task**
## 🧪 Day 156 Knowledge Check
**Q:** Can you serve a QLoRA adapter directly in vLLM without merging?
  - Yes, vLLM supports multi-LoRA serving dynamically
  - No, it must be merged first
  - Only on CPUs
## 🧪 Applied Extension Checks
**Q:** Concept check — for Capstone: Deploying a Custom Fine-Tuned Model, which evaluation approach is most defensible?
  - A) Use a task-specific baseline and measure quality, latency, cost, and failure modes before scaling Capstone: Deploying a Custom Fine-Tuned Model.
  - B) Adopt Capstone: Deploying a Custom Fine-Tuned Model without a baseline because a larger system is automatically better.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Debugging check — what should you verify first when implementing Capstone: Deploying a Custom Fine-Tuned Model?
  - A) Reproduce the issue with a small deterministic fixture, then inspect inputs, configuration, dependencies, and expected outputs.
  - B) Skip reproduction and immediately increase model size or production traffic.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
**Q:** Production scenario — what control belongs in a launch plan for Capstone: Deploying a Custom Fine-Tuned Model?
  - A) Use a canary or staged rollout with quality and latency telemetry, budget/security checks, and a tested rollback path.
  - B) Ship globally after one successful demo and assume there are no operational risks.
  - C) Remove evaluation so the team can move faster.
  - D) Hard-code credentials and environment-specific values.
## 🃏 Revision Flashcards
**Flashcard:** ChatML
> A standard chat template structure ensuring the model knows exactly when a system, user, or assistant is speaking.
**Flashcard:** Multi-LoRA Serving
> Serving a single base model in VRAM but applying different LoRA adapters on a per-request basis.
**Flashcard:** Chat Template
> A Jinja2 template (tokenizer.chat_template) that formats messages into the exact string the model was trained on.
### ✅ Key Takeaways
"You now possess the skills to create custom enterprise AI models that outperform generic GPT-4 on narrow tasks!"
- Data prep takes 80% of the time, training 10%, deployment 10%.
- Multi-LoRA is the future of scalable SaaS platforms.
## 📚 Recommended Resources
📖
#### vLLM LoRA
Docs on serving multiple LoRAs
