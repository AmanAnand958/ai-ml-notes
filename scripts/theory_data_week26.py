"""
Theoretical content definitions for:
- Week 26: Multimodal AI & System Design (Days 185 - 191)
"""

THEORY_WEEKS_26 = {
    # ═════════════════════════════════════════════════════════════════════
    # WEEK 26: MULTIMODAL AI & SYSTEM DESIGN (Days 185 - 191)
    # ═════════════════════════════════════════════════════════════════════
    185: """<h3 class="sh3">1. Vision-Language Models (VLMs) & Cross-Modal Projectors</h3>
<p>
Vision-Language Models (e.g. <strong>LLaVA</strong>, <strong>Qwen-VL</strong>, <strong>CLIP</strong>) bridge computer vision and natural language processing. A visual encoder (Vision Transformer / ViT) divides an image into non-overlapping patches (e.g. $14 \times 14$), projects them into visual patch embeddings, and transforms them into the LLM's text embedding space using a multimodal projector (MLP or Cross-Attention Perceiver):
</p>
<div class="mermaid">
graph LR
  Img["Input Image (336x336)"] --> ViT["Vision Transformer (ViT-L/14)"]
  ViT --> Patches["576 Visual Patch Tokens (dim: 1024)"]
  Patches --> MLP["Multimodal Projection Layer (MLP / Cross-Attention)"]
  MLP --> VisTokens["Projected Visual Tokens (dim: 4096)"]
  Prompt["Text Prompt Tokens: 'Describe this image'"] --> Embed["Text Embedding"]
  VisTokens & Embed --> LLM["Autoregressive LLM (Llama-3 / Mistral)"]
  LLM --> Resp["Generated Textual Description"]
</div>
<div class="diagram-cap">Vision-Language Model (VLM) Architecture: ViT Patch Tokenization, Multimodal Projection, and LLM Decoding.</div>

<h3 class="sh3">2. Patch Token Sizing Formulation</h3>
<div class="math-block">
$$N_{\text{patches}} = \left( \frac{H}{P} \right) \times \left( \frac{W}{P} \right)$$
</div>
<p>
For a $336 \times 336$ image with patch size $P = 14$, the visual encoder generates $(336/14) \times (336/14) = 24 \times 24 = 576$ visual token embeddings.
</p>""",

    186: """<h3 class="sh3">1. Multimodal RAG: Image & Text Retrieval</h3>
<p>
Enterprise knowledge bases contain rich multimodal documents with tables, charts, screenshots, and diagrams that pure text extraction fails to represent. Multimodal RAG addresses this through two primary paradigms:
</p>
<div class="mermaid">
graph TD
  Doc["Multimodal PDF (Text + Charts + Tables)"] --> Route{"Multimodal Strategy"}
  Route --> MultiVector["1. Multi-Vector Late-Interaction (ColPali)\n(Embed document page screenshots directly via VLM)"]
  Route --> JointEmbed["2. Shared Embedding Space (CLIP)\n(Text & image embeddings in unified cosine space)"]
  Route --> CaptionExtract["3. Structured Image Summarization\n(VLM generates rich textual captions for tables/charts, indexed in text vector DB)"]
</div>
<div class="diagram-cap">Multimodal RAG Strategies: ColPali Screenshot Indexing, CLIP Shared Embeddings, and VLM Chart Captioning.</div>""",

    187: """<h3 class="sh3">1. Audio Processing & Speech Recognition with OpenAI Whisper</h3>
<p>
OpenAI Whisper is an encoder-decoder Transformer trained on 680,000 hours of multilingual audio. The raw audio waveform is resampled to 16kHz, converted into an 80-channel log-Mel spectrogram with 25ms windows, and processed through convolutional downsampling layers into the Transformer encoder.
</p>
<div class="mermaid">
graph LR
  Audio["Raw Audio (16kHz Waveform)"] --> Mel["80-Channel Log-Mel Spectrogram"]
  Mel --> Conv["2x 1D Conv Layers (Stride 2)"]
  Conv --> Enc["Transformer Encoder"]
  Enc --> Dec["Autoregressive Transformer Decoder"]
  Dec --> Tokens["Timestamped Transcript Tokens"]
</div>
<div class="diagram-cap">OpenAI Whisper ASR Architecture: Log-Mel Spectrogram, Conv Downsampling, and Encoder-Decoder Sequence-to-Sequence Modeling.</div>""",

    188: """<h3 class="sh3">1. Principal ML System Design: Recommendation System at Scale</h3>
<p>
Designing a personalized recommendation system serving 100M+ active users at 50,000 QPS with p99 latency &lt; 50ms requires a multi-stage funnel architecture:
</p>
<div class="mermaid">
graph TD
  Corpus["Item Corpus (100M Items)"] --> Stage1["1. Candidate Retrieval (Dual-Tower Two-Tower Embeddings)\n100M -> 1,000 items (&lt; 10ms)"]
  Stage1 --> Stage2["2. Heavy Ranking (DeepFM / DLRM Multi-Task Neural Net)\n1,000 -> 100 items (&lt; 25ms)"]
  Stage2 --> Stage3["3. Re-ranking & Business Rules (Diversity, Deduplication, Freshness)\n100 -> 20 items (&lt; 5ms)"]
  Stage3 --> User["Final Personalized Feed for User"]
</div>
<div class="diagram-cap">Four-Stage Recommendation Funnel: Candidate Generation, Heavy Scoring, Re-ranking, and Delivery.</div>

<h3 class="sh3">2. Online Feature Store & Point-in-Time Correctness</h3>
<p>
Using a dual-tier Feature Store (Redis for online low-latency retrieval &lt; 2ms, Feast/Snowflake for offline training sets) guarantees point-in-time correctness, preventing data leakage during training.
</p>""",

    189: """<h3 class="sh3">1. DSPy: Programmatic Prompt Optimization & Compilation</h3>
<p>
Manually tweaking string prompts is fragile, unversioned, and brittle across model upgrades. <strong>DSPy (Declarative Self-improving Python)</strong> separates the program definition (Signatures and Modules like <code>dspy.ChainOfThought</code>, <code>dspy.ReAct</code>) from prompt tuning. DSPy compilers (teleprompters like <strong>MIPROv2</strong> and <strong>BootstrapFewShotWithRandomSearch</strong>) optimize prompts and select optimal few-shot demonstrations mathematically against a reward metric.
</p>
<div class="mermaid">
graph TD
  Program["DSPy Program (Signatures + Modules)"] & Dataset["Training Examples"] & Metric["Evaluation Metric"] --> Compiler["DSPy Optimizer / Teleprompter (MIPRO)"]
  Compiler --> Search["Bayesian / Coordinate Search over Prompts & Few-Shot Demonstrations"]
  Search --> Compiled["Compiled DSPy Program (Outperforms Hand-Crafted Prompts)"]
</div>
<div class="diagram-cap">DSPy Compilation Workflow: Transforming Declarative Modules and Metrics into Optimized Prompt Pipelines.</div>""",

    190: """<h3 class="sh3">1. Principal ML System Design: Billion-Scale Semantic Search</h3>
<p>
Architecting a semantic search system over 1 Billion document embeddings with sub-30ms global latency SLAs, real-time index updates, and dynamic multi-tenant filtering.
</p>
<div class="mermaid">
graph TD
  User["User Search Query"] --> Edge["Edge AI Gateway / Query Analyzer"]
  Edge --> Cache["Semantic Query Cache (Hit: &lt; 3ms)"]
  Cache -->|Miss| SearchCluster["Distributed Qdrant / Milvus Cluster (HNSW + PQ)"]
  SearchCluster --> Partition1["Partition Shard 1"]
  SearchCluster --> Partition2["Partition Shard 2"]
  Partition1 & Partition2 --> Gather["Gather Top-K Candidates"]
  Gather --> Rerank["Cross-Encoder GPU Reranker (Top 200 -> Top 10)"]
  Rerank --> Output["Final Ranked Search Results"]
</div>
<div class="diagram-cap">Billion-Scale Distributed Vector Search Architecture with Multi-Shard Clustering and Cross-Encoder Reranking.</div>""",

    191: """<h3 class="sh3">1. 191-Day AI/ML Mastery: Final Capstone & Principal Review</h3>
<p>
Congratulations on completing the 191-Day AI/ML Curriculum! You have traversed the complete stack of modern artificial intelligence:
</p>
<div class="mermaid">
graph TD
  M1["Month 1: Mathematical Foundations\n(Linear Algebra, Calculus, Statistics, NumPy, Pandas)"] --> M2["Month 2: Classical Machine Learning\n(Regression, Trees, Ensembles, SVMs, PCA)"]
  M2 --> M3["Month 3: Deep Learning & Neural Networks\n(PyTorch, Backprop, Optimizers, CNNs, RNNs)"]
  M3 --> M4["Month 4: NLP & Transformers\n(Word2Vec, Self-Attention, BERT, GPT)"]
  M4 --> M5["Month 5: Production MLOps & Cloud\n(FastAPI, Docker, Kubernetes, MLflow, Airflow, AWS, GCP)"]
  M5 --> M6["Month 6: Frontier Generative AI\n(RAG, Agents, vLLM, QLoRA, DPO, VLMs, Principal System Design)"]
</div>
<div class="diagram-cap">191-Day AI/ML Comprehensive Curriculum Progression: Foundations to Frontier AI Systems.</div>"""
}
