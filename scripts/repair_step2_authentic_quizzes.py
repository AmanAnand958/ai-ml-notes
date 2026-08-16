#!/usr/bin/env python3
"""
Step 2: Replace Generic / Hallucinated Quiz Options in Week 26 with Authentic Questions.
"""

from bs4 import BeautifulSoup
from pathlib import Path

fp26 = Path("pages/weeks/week26.html")
soup = BeautifulSoup(fp26.read_text(encoding='utf-8', errors='replace'), 'html.parser')

AUTHENTIC_QUIZZES_WEEK26 = {
    # Day 185: VLMs
    "quiz-section-185-1": {
        "num": "QUESTION 1 OF 4",
        "q": "How does a modern Vision-Language Model (like GPT-4o or LLaVA) process visual input?",
        "options": [
            ("A", "wrong", "It converts the entire image into raw comma-separated RGB values in the prompt text."),
            ("B", "correct", "It passes image patches through a Vision Encoder (ViT/CLIP) to produce visual token embeddings concatenated with text tokens."),
            ("C", "wrong", "It runs classical OCR to extract text only and discards all visual layout information."),
            ("D", "wrong", "It renders text prompts into PNG images and processes them with pure 2D convolutional filters.")
        ],
        "fb_correct": "✅ Correct! Vision encoders extract patch embeddings that are projected into the LLM token space.",
        "fb_wrong": "❌ Incorrect. VLMs tokenize image patches using a Vision Transformer (ViT) and project them into the LLM embedding space."
    },
    "quiz-section-185-2": {
        "num": "QUESTION 2 OF 4",
        "q": "In Vision-Language Models (VLMs like LLaVA), how are image patch features mapped into the LLM token embedding space?",
        "options": [
            ("A", "correct", "Through a linear or MLP Projection Layer that translates visual feature dimension d_v into LLM hidden dimension d_l."),
            ("B", "wrong", "By directly changing the LLM vocabulary size to 100 million tokens."),
            ("C", "wrong", "By quantizing the weights of the vision encoder to 1-bit integers."),
            ("D", "wrong", "By bypassing tokenization and storing raw pixel arrays in the KV-cache.")
        ],
        "fb_correct": "✅ Correct! A projection layer aligns visual encoder features with the LLM embedding dimension.",
        "fb_wrong": "❌ Incorrect. An MLP or linear projector aligns the visual feature dimension with the language model's hidden representation."
    },
    "quiz-section-185-3": {
        "num": "QUESTION 3 OF 4",
        "q": "What is the primary cost trade-off between detail: 'low' and detail: 'high' in OpenAI Vision APIs?",
        "options": [
            ("A", "wrong", "Detail 'low' processes audio, while detail 'high' processes video."),
            ("B", "correct", "Detail 'low' rescales to 512x512 for a flat 85 tokens, while detail 'high' crops into 512x512 tiles costing 170 tokens per tile."),
            ("C", "wrong", "Detail 'low' only reads monochrome images while detail 'high' supports RGB."),
            ("D", "wrong", "Detail 'low' runs locally on the client CPU while detail 'high' runs on GPU clusters.")
        ],
        "fb_correct": "✅ Correct! Detail 'low' uses a fixed 85 tokens, whereas 'high' breaks high-res images into 512x512 tiles at 170 tokens each.",
        "fb_wrong": "❌ Incorrect. Detail 'low' resizes the image to 512x512 (85 tokens), whereas 'high' tiles the image (170 tokens per 512x512 patch)."
    },
    "quiz-section-185-4": {
        "num": "QUESTION 4 OF 4",
        "q": "When processing high-resolution visual documents with VLMs, how does image tiling prevent information loss?",
        "options": [
            ("A", "correct", "It breaks large images into multiple 512x512 patches with an overview thumbnail, preserving small text and dense table details."),
            ("B", "wrong", "It converts raster images into SVG vector paths."),
            ("C", "wrong", "It applies PCA dimensionality reduction to remove high-frequency noise."),
            ("D", "wrong", "It compresses the document into an animated GIF to reduce sequence length.")
        ],
        "fb_correct": "✅ Correct! Image tiling maintains high resolution for fine text while also providing a global overview context.",
        "fb_wrong": "❌ Incorrect. Tiling preserves native pixel resolution for dense layout details without downsampling artifacts."
    },

    # Day 186: Multimodal RAG
    "quiz-section-186-1": {
        "num": "QUESTION 1 OF 4",
        "q": "In the Image Summarization architecture for Multimodal RAG, what is stored in the Vector Database?",
        "options": [
            ("A", "wrong", "The raw uncompressed RGB pixel bytes."),
            ("B", "correct", "The text embeddings of VLM-generated descriptions/summaries of images alongside metadata pointers."),
            ("C", "wrong", "Pre-trained weights of the vision encoder."),
            ("D", "wrong", "Encrypted user access tokens.")
        ],
        "fb_correct": "✅ Correct! VLM-generated text summaries are embedded with text embedding models and stored in vector DBs.",
        "fb_wrong": "❌ Incorrect. Storing text embeddings of VLM summaries allows standard fast text vector indexing over visual documents."
    },
    "quiz-section-186-2": {
        "num": "QUESTION 2 OF 4",
        "q": "How does ColPali page-level document retrieval revolutionize Multimodal RAG compared to traditional OCR pipelines?",
        "options": [
            ("A", "correct", "It directly embeds whole document page screenshots using multi-vector PaliGemma representations, bypassing fragile OCR and parser heuristics."),
            ("B", "wrong", "It converts PDF documents into SQL insert statements automatically."),
            ("C", "wrong", "It replaces vector databases with relational B-Trees."),
            ("D", "wrong", "It disables text search entirely and only indexes file creation timestamps.")
        ],
        "fb_correct": "✅ Correct! ColPali indexes visual document pages end-to-end with late interaction multi-vector representations.",
        "fb_wrong": "❌ Incorrect. ColPali leverages vision-language embeddings directly on page images without OCR pipelines."
    },
    "quiz-section-186-3": {
        "num": "QUESTION 3 OF 4",
        "q": "When indexing scanned PDF invoices containing complex tables and charts, why is multimodal retrieval superior to text-only extraction?",
        "options": [
            ("A", "correct", "Text-only extraction flattens 2D layout relationships and loses diagram semantics, whereas multimodal approaches preserve spatial context."),
            ("B", "wrong", "Text-only extraction uses 10x more GPU memory than multimodal models."),
            ("C", "wrong", "Multimodal models do not require vector search engines."),
            ("D", "wrong", "Text-only extraction is forbidden by cloud security policies.")
        ],
        "fb_correct": "✅ Correct! Multimodal models preserve spatial layouts, header associations, and visual diagram relationships.",
        "fb_wrong": "❌ Incorrect. Scanned tables and visual graphs lose their row/column alignment when flattened into plain text streams."
    },
    "quiz-section-186-4": {
        "num": "QUESTION 4 OF 4",
        "q": "What is the key advantage of late-interaction multi-vector retrieval (like ColBERT / ColPali) in multimodal search?",
        "options": [
            ("A", "correct", "It retains token/patch-level vector representations and computes max-similarity alignment at query time for fine-grained matching."),
            ("B", "wrong", "It compresses all documents into a single scalar float number."),
            ("C", "wrong", "It completely eliminates the need for token embeddings."),
            ("D", "wrong", "It runs indexing entirely in client JavaScript without servers.")
        ],
        "fb_correct": "✅ Correct! Late interaction preserves granular patch embeddings and performs MaxSim scoring across query and document tokens.",
        "fb_wrong": "❌ Incorrect. Multi-vector late interaction retains patch-level vectors and computes token-to-token alignment."
    },

    # Day 187: Whisper Audio
    "quiz-section-187-1": {
        "num": "QUESTION 1 OF 4",
        "q": "What audio sampling rate and preprocessing feature does OpenAI Whisper expect as input?",
        "options": [
            ("A", "wrong", "44.1 kHz raw WAV PCM audio in stereo."),
            ("B", "correct", "16 kHz mono audio converted into 80-channel (or 128-channel in v3) Log-Mel Spectrograms in 30-second chunks."),
            ("C", "wrong", "MIDI musical event sequences."),
            ("D", "wrong", "MP3 compressed binary bitstreams.")
        ],
        "fb_correct": "✅ Correct! Whisper computes 80/128-channel Log-Mel spectrograms from 16 kHz mono audio in 30s windows.",
        "fb_wrong": "❌ Incorrect. Whisper processes 16 kHz mono audio converted into Log-Mel filterbank spectrograms."
    },
    "quiz-section-187-2": {
        "num": "QUESTION 2 OF 4",
        "q": "In OpenAI Whisper speech-to-text processing, what acoustic representation is fed into the Transformer encoder?",
        "options": [
            ("A", "correct", "A 2D time-frequency Log-Mel Spectrogram matrix passed through 1D convolutional downsampling layers."),
            ("B", "wrong", "A 1D array of phoneme dictionary integers."),
            ("C", "wrong", "Raw uncompressed waveform amplitude values in time domain."),
            ("D", "wrong", "Fourier phase angle vectors.")
        ],
        "fb_correct": "✅ Correct! 1D convolutional layers downsample the 80-channel log-Mel spectrogram before the Transformer encoder.",
        "fb_wrong": "❌ Incorrect. Whisper passes log-Mel spectrograms through two conv1d layers with stride 2 into the encoder."
    },
    "quiz-section-187-3": {
        "num": "QUESTION 3 OF 4",
        "q": "Why is Voice Activity Detection (VAD) critical before running long-form audio through Whisper in production?",
        "options": [
            ("A", "correct", "It filters out silence and background noise, preventing Whisper from hallucinating repeated phantom text during silent intervals."),
            ("B", "wrong", "It increases audio pitch to compress bandwidth."),
            ("C", "wrong", "It converts speech into encrypted hashes."),
            ("D", "wrong", "It reduces GPU memory usage to zero.")
        ],
        "fb_correct": "✅ Correct! Silero-VAD strips silent gaps, eliminating Whisper's known failure mode of hallucinating on silence.",
        "fb_wrong": "❌ Incorrect. Feeding long silent audio chunks into Whisper causes autoregressive hallucination loops."
    },
    "quiz-section-187-4": {
        "num": "QUESTION 4 OF 4",
        "q": "How does Whisper achieve word-level timestamp alignment for audio subtitles and search?",
        "options": [
            ("A", "correct", "By inspecting cross-attention weight matrices between decoder text tokens and encoder audio frames (or using Dynamic Time Warping)."),
            ("B", "wrong", "By guessing constant 500ms intervals per word."),
            ("C", "wrong", "By asking the user to manually type timestamps."),
            ("D", "wrong", "By measuring network packet round-trip times.")
        ],
        "fb_correct": "✅ Correct! Cross-attention alignment tracks which audio frames contributed most to each decoded token.",
        "fb_wrong": "❌ Incorrect. Whisper uses cross-attention weights and DTW alignment to match acoustic frames to generated tokens."
    },

    # Day 188: RecSys Design
    "quiz-section-188-1": {
        "num": "QUESTION 1 OF 4",
        "q": "In enterprise recommendation system design (e.g. YouTube/Netflix), why is a Two-Stage (Candidate Generation + Ranking) architecture used?",
        "options": [
            ("A", "wrong", "Because single-stage models are not supported on Linux operating systems."),
            ("B", "correct", "Candidate generation efficiently filters millions of items to ~1,000 using fast ANN search, allowing heavy ranking models to score the top candidates within latency SLAs."),
            ("C", "wrong", "Because neural networks cannot process more than 100 items at a time."),
            ("D", "wrong", "To duplicate database queries across multiple availability zones.")
        ],
        "fb_correct": "✅ Correct! Fast vector retrieval narrows 10M+ items to 1000, which are then precision-ranked with deep feature cross models.",
        "fb_wrong": "❌ Incorrect. Scoring 10M items with a deep neural network would exceed real-time 50ms latency budgets."
    },
    "quiz-section-188-2": {
        "num": "QUESTION 2 OF 4",
        "q": "In large-scale recommender system design, what is the 'Two-Tower' (User Tower + Item Tower) DSSM architecture?",
        "options": [
            ("A", "correct", "Separate neural networks compute user embeddings and item embeddings independently, enabling real-time dot-product / cosine scoring over pre-computed item indices."),
            ("B", "wrong", "A backup server architecture with two physical data center towers."),
            ("C", "wrong", "A dual-GPU setup where one GPU trains and the second GPU validates."),
            ("D", "wrong", "An ensemble of two random forest classifiers.")
        ],
        "fb_correct": "✅ Correct! User and Item towers map features into a shared embedding space for O(1) ANN vector search.",
        "fb_wrong": "❌ Incorrect. Two-tower models isolate query features and candidate features into decoupled embedding spaces."
    },
    "quiz-section-188-3": {
        "num": "QUESTION 3 OF 4",
        "q": "Why can item embeddings in a Two-Tower model be pre-computed offline, while user embeddings must often be computed online?",
        "options": [
            ("A", "correct", "Item catalog attributes update infrequently and can be indexed in Vector DBs, whereas user state depends on immediate real-time session context."),
            ("B", "wrong", "Item vectors are always smaller in dimension than user vectors."),
            ("C", "wrong", "Item vectors use floating-point numbers while user vectors use strings."),
            ("D", "wrong", "Offline computation is only allowed on candidate models.")
        ],
        "fb_correct": "✅ Correct! Static item embeddings are indexed offline, while dynamic user embeddings are computed at query time.",
        "fb_wrong": "❌ Incorrect. Items change slowly so their embeddings can be indexed in Milvus/Faiss offline, but user session intent is real-time."
    },
    "quiz-section-188-4": {
        "num": "QUESTION 4 OF 4",
        "q": "What loss function is standard for training Two-Tower retrieval models with in-batch negatives?",
        "options": [
            ("A", "correct", "Sampled Softmax or InfoNCE / Cross-Entropy Loss where other items in the mini-batch serve as negative candidates."),
            ("B", "wrong", "Mean Squared Error (MSE) on user ID strings."),
            ("C", "wrong", "L1 Absolute Error on catalog timestamps."),
            ("D", "wrong", "Categorical Hinge Loss with zero temperature.")
        ],
        "fb_correct": "✅ Correct! In-batch negative InfoNCE loss treats batch items as negatives, scaling training efficiency without explicit negative sampling.",
        "fb_wrong": "❌ Incorrect. Sampled Softmax / InfoNCE with in-batch negatives is standard for dual-encoder retrieval systems."
    },

    # Day 189: DSPy Prompt Optimization
    "quiz-section-189-1": {
        "num": "QUESTION 1 OF 4",
        "q": "What fundamental paradigm does DSPy (Declarative Self-improving Python) introduce for LLM application development?",
        "options": [
            ("A", "wrong", "Writing longer strings of manual system prompts in markdown."),
            ("B", "correct", "Treating LLMs as declarative computational modules with signatures and using optimizers/compilers to auto-tune prompts and few-shot exemplars against metric functions."),
            ("C", "wrong", "Replacing Python with specialized C++ assembly compilers."),
            ("D", "wrong", "Training transformer backbones from scratch on single laptops.")
        ],
        "fb_correct": "✅ Correct! DSPy separates declarative program logic (Signatures) from prompt optimization (Teleprompters/Compilers).",
        "fb_wrong": "❌ Incorrect. DSPy compiles declarative modules into optimal few-shot prompts using systematic metric-driven optimizers."
    },
    "quiz-section-189-2": {
        "num": "QUESTION 2 OF 4",
        "q": "In DSPy, how does compiling a `dspy.Program` differ from manual prompt engineering?",
        "options": [
            ("A", "correct", "The compiler systematically searches over prompt instructions and few-shot demonstrations to maximize a defined validation metric score."),
            ("B", "wrong", "The compiler converts Python bytecode into binary machine instructions."),
            ("C", "wrong", "The compiler deletes all intermediate LLM steps to save bandwidth."),
            ("D", "wrong", "The compiler forces all outputs to be single-word yes/no answers.")
        ],
        "fb_correct": "✅ Correct! DSPy compilers (BootstrapFewShot, MIPRO) automatically synthesize effective few-shot demonstrations and prompt variations.",
        "fb_wrong": "❌ Incorrect. DSPy compilation optimizes module prompts and few-shot examples automatically based on validation metrics."
    },
    "quiz-section-189-3": {
        "num": "QUESTION 3 OF 4",
        "q": "What is a `dspy.Signature` in the DSPy architecture?",
        "options": [
            ("A", "correct", "A declarative specification of input fields and output fields (e.g. 'context, question -> answer') that defines the task contract without hardcoded prompt strings."),
            ("B", "wrong", "A cryptographic digital signature verifying API key ownership."),
            ("C", "wrong", "A Python function decorator that calculates execution time in milliseconds."),
            ("D", "wrong", "A vector embedding representing the model author.")
        ],
        "fb_correct": "✅ Correct! Signatures declare input/output specifications cleanly, allowing DSPy to generate and optimize the concrete prompt format.",
        "fb_wrong": "❌ Incorrect. A DSPy Signature defines input and output fields, abstracting away brittle prompt formatting."
    },
    "quiz-section-189-4": {
        "num": "QUESTION 4 OF 4",
        "q": "How does DSPy's `BootstrapFewShotWithRandomSearch` optimizer improve multi-hop RAG pipelines?",
        "options": [
            ("A", "correct", "It simulates pipeline execution over a training set, filters traces where the final metric passes, and selects the most effective demonstration sets."),
            ("B", "wrong", "It fine-tunes all transformer attention weights using backpropagation."),
            ("C", "wrong", "It randomizes network routing across AWS regions."),
            ("D", "wrong", "It encrypts queries using RSA 2048-bit keys.")
        ],
        "fb_correct": "✅ Correct! It boots successful execution traces as high-quality few-shot examples for intermediate pipeline steps.",
        "fb_wrong": "❌ Incorrect. The optimizer bootstraps successful intermediate reasoning steps as dynamic few-shot exemplars."
    },

    # Day 190: Semantic Search System Design
    "quiz-section-190-1": {
        "num": "QUESTION 1 OF 4",
        "q": "When scaling a vector search database to 100M+ vectors, which vector indexing technique provides sub-10ms latency with low RAM footprint?",
        "options": [
            ("A", "wrong", "Exact Flat L2 Euclidean distance search across all uncompressed vectors."),
            ("B", "correct", "HNSW (Hierarchical Navigable Small World) graph combined with Product Quantization (IVF-PQ) or Scalar Quantization (SQ8)."),
            ("C", "wrong", "Linear file scans using grep on CSV files."),
            ("D", "wrong", "Storing vectors in browser LocalStorage.")
        ],
        "fb_correct": "✅ Correct! HNSW with Product Quantization (PQ) compresses vectors 4x-16x and delivers sub-10ms nearest neighbor search.",
        "fb_wrong": "❌ Incorrect. Exact Flat search scales linearly O(N), whereas HNSW + PQ provides logarithmic O(log N) approximate nearest neighbor lookup."
    },
    "quiz-section-190-2": {
        "num": "QUESTION 2 OF 4",
        "q": "When designing an enterprise search engine, how should Dense Vector Search and Lexical BM25 Search be combined?",
        "options": [
            ("A", "correct", "Using Hybrid Search with Reciprocal Rank Fusion (RRF) or a cross-encoder re-ranker to combine semantic recall with exact keyword precision."),
            ("B", "wrong", "By alternating between vector search on odd days and keyword search on even days."),
            ("C", "wrong", "By discarding keyword search entirely because neural vectors solve all search problems."),
            ("D", "wrong", "By concatenating search strings with vector float numbers.")
        ],
        "fb_correct": "✅ Correct! Hybrid Search with RRF merges dense semantic recall (conceptual similarity) with sparse BM25 (exact SKU/product code match).",
        "fb_wrong": "❌ Incorrect. Hybrid search with RRF combines the semantic understanding of dense embeddings with exact keyword precision of BM25."
    },
    "quiz-section-190-3": {
        "num": "QUESTION 3 OF 4",
        "q": "What is the primary benefit of deploying a Cross-Encoder Re-Ranker (e.g. BGE-Reranker or Cohere Rerank) in a search pipeline?",
        "options": [
            ("A", "correct", "It performs full cross-attention between query and retrieved candidates, capturing fine-grained token interactions that dual-encoders miss."),
            ("B", "wrong", "It reduces vector database memory consumption by 90%."),
            ("C", "wrong", "It translates text into audio waveforms."),
            ("D", "wrong", "It bypasses the need for index sharding.")
        ],
        "fb_correct": "✅ Correct! Cross-encoders perform joint cross-attention across query and candidate text, significantly boosting precision on top-50 candidates.",
        "fb_wrong": "❌ Incorrect. Cross-encoders attend across query and document jointly, providing superior ranking accuracy over bi-encoder embeddings."
    },
    "quiz-section-190-4": {
        "num": "QUESTION 4 OF 4",
        "q": "How does Vector Index Sharding with Scatter-Gather architecture handle search traffic scaling?",
        "options": [
            ("A", "correct", "The query is scattered across N index shards in parallel, and a coordinator gathers top-K candidates from each shard before global re-ranking."),
            ("B", "wrong", "Every query is routed to only one random shard and results are returned directly without merging."),
            ("C", "wrong", "Sharding duplicates the entire database on every single CPU core."),
            ("D", "wrong", "Sharding disables vector compression to maximize accuracy.")
        ],
        "fb_correct": "✅ Correct! Scatter-gather queries vector shards concurrently and aggregates top candidates at the API gateway layer.",
        "fb_wrong": "❌ Incorrect. Scatter-gather broadcasts search queries to independent shards and merges the top-K results."
    },

    # Day 191: Final Capstone
    "quiz-section-191-1": {
        "num": "QUESTION 1 OF 4",
        "q": "What constitutes a production-ready Full-Stack AI/ML Engineering portfolio project?",
        "options": [
            ("A", "wrong", "A Jupyter notebook containing un-commented code with no README or deployment instructions."),
            ("B", "correct", "An end-to-end deployed service with reproducible Docker/K8s setup, CI/CD automated tests, evaluation metrics benchmarks, and architectural RFC documentation."),
            ("C", "wrong", "A collection of tutorial code copied verbatim from library documentation."),
            ("D", "wrong", "A screenshot of an LLM chat interface without underlying code.")
        ],
        "fb_correct": "✅ Correct! Production portfolio projects demonstrate end-to-end engineering: evaluation, deployment, testing, and system documentation.",
        "fb_wrong": "❌ Incorrect. Top engineering portfolios highlight end-to-end reliability, testing, benchmarking, and cloud deployment."
    },
    "quiz-section-191-2": {
        "num": "QUESTION 2 OF 4",
        "q": "What key documentation elements make an AI/ML engineering portfolio project standout to hiring managers and tech leads?",
        "options": [
            ("A", "correct", "System Architecture Diagrams (C4/Mermaid), quantitative latency/throughput/cost trade-off analysis, failure mode postmortems, and live interactive demo links."),
            ("B", "wrong", "Long philosophical essays about artificial general intelligence."),
            ("C", "wrong", "Hiding all code behind password-protected zip files."),
            ("D", "wrong", "Listing 50 buzzwords without explaining actual technical contributions.")
        ],
        "fb_correct": "✅ Correct! Architecture diagrams, quantitative benchmarks, trade-off analyses, and live demos showcase senior engineering rigor.",
        "fb_wrong": "❌ Incorrect. Hiring managers look for architecture clarity, latency/cost benchmarks, failure modes, and reproducible setups."
    },
    "quiz-section-191-3": {
        "num": "QUESTION 3 OF 4",
        "q": "In ML System Design interviews, what framework should you follow to structure your end-to-end design?",
        "options": [
            ("A", "correct", "Requirements & Constraints → Data & Features → Modeling & Loss → Serving & Scaling Architecture → Evaluation, Monitoring & Offline/Online Guardrails."),
            ("B", "wrong", "Immediately start writing raw PyTorch training loops on a whiteboard without clarifying requirements."),
            ("C", "wrong", "Suggest buying the largest proprietary model available and ignoring infrastructure cost."),
            ("D", "wrong", "Refuse to discuss latency SLAs and focus exclusively on training accuracy.")
        ],
        "fb_correct": "✅ Correct! Systematic ML system design flows from business constraints through data, model, serving architecture, and evaluation telemetry.",
        "fb_wrong": "❌ Incorrect. High-scoring system design starts with clarifying requirements and latency/cost constraints before diving into architectures."
    },
    "quiz-section-191-4": {
        "num": "QUESTION 4 OF 4",
        "q": "How should an engineer present trade-offs made during ML system design interviews (e.g. accuracy vs latency vs cost)?",
        "options": [
            ("A", "correct", "Quantify operational trade-offs with explicit numbers (e.g. 2-bit quantization saves 60% VRAM with 0.5% perplexity degradation) and propose staged fallback policies."),
            ("B", "wrong", "Claim that there are zero trade-offs and the chosen architecture is flawless in every metric."),
            ("C", "wrong", "Ignore production inference cost and assume unlimited cloud budget."),
            ("D", "wrong", "Avoid discussing failure modes or rollback strategies.")
        ],
        "fb_correct": "✅ Correct! Senior engineers quantify accuracy vs latency vs cost trade-offs with data and justify architectural choices rigorously.",
        "fb_wrong": "❌ Incorrect. Strong candidates articulate explicit trade-offs and explain why their chosen compromise fits the system constraints."
    }
}

# Update quizzes in soup
for q_id, q_data in AUTHENTIC_QUIZZES_WEEK26.items():
    q_elem = soup.find('div', id=q_id)
    if q_elem:
        new_q_soup = BeautifulSoup(f'''
<div class="quiz-block" id="{q_id}">
  <div class="quiz-num">{q_data["num"]}</div>
  <div class="quiz-q">{q_data["q"]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{q_data["options"][0][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">A</span>{q_data["options"][0][2]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{q_data["options"][1][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">B</span>{q_data["options"][1][2]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{q_data["options"][2][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">C</span>{q_data["options"][2][2]}</div>
  <div class="quiz-opt" onclick="quiz(this,'{q_data["options"][3][1]}','{q_id}')" onkeydown="if(event.key==='Enter'||event.key===' ')this.click()" role="button" tabindex="0"><span class="quiz-letter">D</span>{q_data["options"][3][2]}</div>
  <div class="quiz-feedback correct-fb" id="{q_id}-correct" style="display:none;">{q_data["fb_correct"]}</div>
  <div class="quiz-feedback wrong-fb" id="{q_id}-wrong" style="display:none;">{q_data["fb_wrong"]}</div>
</div>
''', 'html.parser')
        q_elem.replace_with(new_q_soup.find('div', class_='quiz-block'))

fp26.write_text(str(soup), encoding='utf-8')
print("✅ Replaced all generic quiz options with authentic topic-specific quizzes in Week 26!")
