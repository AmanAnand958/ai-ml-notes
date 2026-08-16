#!/usr/bin/env python3
"""
Step 3: Enrich Task Reference Implementations in Weeks 5 and 9 with authentic, topic-specific algorithmic code.
"""

from bs4 import BeautifulSoup
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# 1. ENRICH WEEK 5 TASKS
# ─────────────────────────────────────────────────────────────────────────────
fp5 = Path("pages/weeks/week5.html")
soup5 = BeautifulSoup(fp5.read_text(encoding='utf-8'), 'html.parser')

WEEK5_TASK_SOLUTIONS = {
    "day-31": '''# Solution for Task: NumPy train_test_split from scratch
import numpy as np

def train_test_split_scratch(X: np.ndarray, y: np.ndarray, test_size: float = 0.2, random_state: int = 42):
    np.random.seed(random_state)
    n_samples = len(X)
    shuffled_indices = np.random.permutation(n_samples)
    test_count = int(n_samples * test_size)
    
    test_idx = shuffled_indices[:test_count]
    train_idx = shuffled_indices[test_count:]
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

# Verification
X_sample = np.arange(20).reshape(10, 2)
y_sample = np.arange(10)
X_tr, X_te, y_tr, y_te = train_test_split_scratch(X_sample, y_sample, test_size=0.3)
print(f"Train samples: {len(X_tr)}, Test samples: {len(X_te)}")''',

    "day-32": '''# Solution for Task: NumPy Regression Metrics Suite
import numpy as np

def compute_regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    errors = y_true - y_pred
    mse = np.mean(errors ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(errors))
    
    ss_res = np.sum(errors ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    r2 = 1 - (ss_res / (ss_tot + 1e-10))
    
    return {"MSE": round(mse, 4), "RMSE": round(rmse, 4), "MAE": round(mae, 4), "R2": round(r2, 4)}

# Verification
y_t = np.array([3.0, -0.5, 2.0, 7.0])
y_p = np.array([2.5, 0.0, 2.0, 8.0])
print("Regression Metrics:", compute_regression_metrics(y_t, y_p))''',

    "day-33": '''# Solution for Task: Imbalanced Classification Metrics Report
import numpy as np

def compute_classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (tp + tn) / len(y_true)
    
    return {"Accuracy": round(accuracy, 4), "Precision": round(precision, 4), "Recall": round(recall, 4), "F1": round(f1, 4)}

y_t = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
y_p = np.array([1, 0, 1, 0, 0, 1, 1, 0, 1, 0])
print("Classification Report:", compute_classification_metrics(y_t, y_p))''',

    "day-36": '''# Solution for Task: KNN Classifier from Scratch
import numpy as np

class KNNClassifierScratch:
    def __init__(self, k: int = 3):
        self.k = k
        
    def fit(self, X: np.ndarray, y: np.ndarray):
        self.X_train = X
        self.y_train = y
        
    def predict(self, X: np.ndarray) -> np.ndarray:
        predictions = []
        for sample in X:
            # Euclidean distances
            distances = np.linalg.norm(self.X_train - sample, axis=1)
            # Top-k nearest neighbors
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            # Majority vote
            majority_label = np.bincount(k_labels).argmax()
            predictions.append(majority_label)
        return np.array(predictions)

# Verification
X_tr = np.array([[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]])
y_tr = np.array([0, 0, 0, 1, 1, 1])
knn = KNNClassifierScratch(k=3)
knn.fit(X_tr, y_tr)
print("Predicted labels for test points:", knn.predict(np.array([[2, 2], [7, 6]])))'''
}

for did, sol_code in WEEK5_TASK_SOLUTIONS.items():
    d_sec = soup5.find('div', id=did)
    if d_sec:
        tb = d_sec.find('div', class_='task-body')
        if tb:
            pre = tb.find('pre')
            if pre:
                pre.string = sol_code
                print(f"  ✅ Injected authentic algorithmic code for Week 5 {did}")

fp5.write_text(str(soup5), encoding='utf-8')

# ─────────────────────────────────────────────────────────────────────────────
# 2. ENRICH WEEK 9 TASKS (CNNs & Vision)
# ─────────────────────────────────────────────────────────────────────────────
fp9 = Path("pages/weeks/week9.html")
soup9 = BeautifulSoup(fp9.read_text(encoding='utf-8'), 'html.parser')

WEEK9_TASK_SOLUTIONS = {
    "day-59": '''# Solution for Task: 2D Convolution Forward Layer in NumPy
import numpy as np

def conv2d_forward(image: np.ndarray, kernel: np.ndarray, stride: int = 1, padding: int = 0) -> np.ndarray:
    if padding > 0:
        image = np.pad(image, ((padding, padding), (padding, padding)), mode='constant')
        
    H, W = image.shape
    kH, kW = kernel.shape
    out_H = (H - kH) // stride + 1
    out_W = (W - kW) // stride + 1
    
    output = np.zeros((out_H, out_W))
    for i in range(0, out_H):
        for j in range(0, out_W):
            region = image[i*stride : i*stride + kH, j*stride : j*stride + kW]
            output[i, j] = np.sum(region * kernel)
            
    return output

# Verification
img = np.random.randn(8, 8)
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
conv_out = conv2d_forward(img, sobel_x, stride=1, padding=1)
print(f"Input: (8, 8) -> Conv Output Shape: {conv_out.shape}")''',

    "day-60": '''# Solution for Task: Max Pooling Forward and Mask Generator
import numpy as np

def max_pool2d_forward(image: np.ndarray, pool_size: int = 2, stride: int = 2):
    H, W = image.shape
    out_H = (H - pool_size) // stride + 1
    out_W = (W - pool_size) // stride + 1
    
    output = np.zeros((out_H, out_W))
    for i in range(out_H):
        for j in range(out_W):
            patch = image[i*stride : i*stride + pool_size, j*stride : j*stride + pool_size]
            output[i, j] = np.max(patch)
            
    return output

img = np.array([[1, 3, 2, 4], [5, 6, 7, 8], [9, 0, 1, 2], [3, 4, 5, 6]])
print("Pooled 2x2 Feature Map:\n", max_pool2d_forward(img, pool_size=2, stride=2))''',

    "day-63": '''# Solution for Task: Bounding Box Intersection over Union (IoU)
import numpy as np

def compute_iou(box1: list, box2: list) -> float:
    # box format: [x1, y1, x2, y2]
    xA = max(box1[0], box2[0])
    yA = max(box1[1], box2[1])
    xB = min(box1[2], box2[2])
    yB = min(box1[3], box2[3])
    
    inter_area = max(0, xB - xA) * max(0, yB - yA)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    
    union_area = float(box1_area + box2_area - inter_area)
    return inter_area / union_area if union_area > 0 else 0.0

boxA = [50, 50, 150, 150]
boxB = [100, 100, 200, 200]
print(f"Calculated IoU: {compute_iou(boxA, boxB):.4f}")'''
}

for did, sol_code in WEEK9_TASK_SOLUTIONS.items():
    d_sec = soup9.find('div', id=did)
    if d_sec:
        tb = d_sec.find('div', class_='task-body')
        if tb:
            pre = tb.find('pre')
            if pre:
                pre.string = sol_code
                print(f"  ✅ Injected authentic algorithmic code for Week 9 {did}")

fp9.write_text(str(soup9), encoding='utf-8')

print("\n🎉 STEP 3 COMPLETE: ALL TASK REFERENCE SOLUTIONS ENRICHED WITH AUTHENTIC CODE!")
