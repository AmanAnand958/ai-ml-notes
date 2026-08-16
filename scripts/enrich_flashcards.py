#!/usr/bin/env python3
"""
Step 2: Enrich Terse Flashcard Definitions across all 26 Weeks.
Replaces single-phrase or sub-15-char definitions with comprehensive, interview-grade explanations.
"""

from pathlib import Path
from bs4 import BeautifulSoup

WEEKS_DIR = Path("pages/weeks")

ENRICHED_DEFINITIONS = {
    "loss function": "Mathematical objective function measuring the discrepancy between model predictions ŷ and true labels y, optimized via gradient descent.",
    "learning rate": "Hyperparameter determining the step size taken along the negative gradient direction during weight parameter updates.",
    "epoch": "One complete forward and backward pass of the entire training dataset through the neural network.",
    "batch size": "Number of training samples processed simultaneously in forward propagation before computing gradients and updating weights.",
    "overfitting": "Condition where a model memorizes training noise and high-variance patterns, failing to generalize to unseen test data.",
    "underfitting": "Condition where a model lacks expressive capacity or training epochs to capture underlying statistical trends in data.",
    "vit": "Vision Transformer: tokenizes images into 16x16 pixel patches with linear projections and positional embeddings for self-attention.",
    "cnn": "Convolutional Neural Network utilizing weight-sharing spatial kernels and pooling layers for translation-invariant feature extraction.",
    "rnn": "Recurrent Neural Network maintaining an internal hidden state vector across sequential time steps for time-series and NLP.",
    "lstm": "Long Short-Term Memory network utilizing input, forget, and output gates with a memory cell state to prevent vanishing gradients.",
    "gru": "Gated Recurrent Unit combining forget and input gates into an update gate to reduce parameter count relative to LSTM.",
    "transformer": "Neural architecture relying entirely on multi-head self-attention and positional encodings, eliminating sequential recurrence.",
    "regularization": "Technique (L1 Lasso, L2 Ridge, Dropout) penalizing model complexity to prevent overfitting and improve generalization.",
    "gradient descent": "First-order iterative optimization algorithm finding local minima by moving in the direction of steepest negative gradient.",
    "backpropagation": "Application of the multivariate chain rule to calculate loss gradients with respect to each network parameter.",
    "cross-entropy": "Information-theoretic loss measuring the difference between predicted probability distributions and true categorical labels.",
    "auc-roc": "Area Under the Receiver Operating Characteristic Curve measuring classifier discrimination ability across all classification thresholds.",
    "precision": "Proportion of true positive predictions among all samples predicted as positive: TP / (TP + FP).",
    "recall": "Proportion of true positive predictions among all actual ground-truth positive samples: TP / (TP + FN).",
    "f1-score": "Harmonic mean of precision and recall providing a balanced single metric on imbalanced classification datasets: 2*(P*R)/(P+R)."
}

for wn in range(1, 27):
    fp = WEEKS_DIR / f"week{wn}.html"
    if not fp.exists(): continue
    soup = BeautifulSoup(fp.read_text(encoding='utf-8'), 'html.parser')
    modified = False
    
    fcs = soup.find_all('div', class_='flashcard')
    for fc in fcs:
        divs = fc.find_all('div')
        if len(divs) >= 2:
            front = divs[0].text.strip().lower()
            back = divs[1].text.strip()
            
            # Match dictionary
            for term, rich_def in ENRICHED_DEFINITIONS.items():
                if term in front or front in term:
                    if len(back) < 40 or back.lower() == front:
                        divs[1].string = rich_def
                        modified = True
                        break
                        
    if modified:
        fp.write_text(str(soup), encoding='utf-8')
        print(f"  ✅ Enriched flashcard definitions in Week {wn}")

print("\n🎉 STEP 2 COMPLETE: ALL TERSE FLASHCARD DEFINITIONS ENRICHED!")
