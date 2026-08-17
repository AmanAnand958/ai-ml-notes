#!/usr/bin/env python3
"""
Phase 3 Fix Script — Pass 2
============================
- K7: Fix week 3 tb-proj badge_class (missed in Pass 1)
- U9: Replace skeleton solution_code (has # TODO: placeholder) 
  with real implementations for all remaining K2-fixed tasks
- K3: Replace generic RandomForest solution_code with topic-specific code
"""

import os
import re
import yaml
import shutil
from datetime import datetime

ROOT     = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT, 'src/data')
BACKUP_DIR = os.path.join(ROOT, 'scripts', f'backup_pass2_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
os.makedirs(BACKUP_DIR, exist_ok=True)

class LiteralStr(str): pass
def literal_representer(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)
yaml.add_representer(LiteralStr, literal_representer)

def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def deep_literal(obj):
    if isinstance(obj, dict): return {k: deep_literal(v) for k,v in obj.items()}
    if isinstance(obj, list): return [deep_literal(v) for v in obj]
    if isinstance(obj, str) and '\n' in obj: return LiteralStr(obj)
    return obj

def save_yaml(path, data):
    data = deep_literal(data)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

# ─────────────────────────────────────────────────────────────────────────────
# Real solution_code for every remaining skeleton-generated task
# Keyed by (week_n, day_id)
# ─────────────────────────────────────────────────────────────────────────────

REAL_SOLUTIONS = {

    # Week 4, Day 29: Dimensionality Reduction — PCA
    (4, 29): '''# Day 29: Dimensionality Reduction — PCA
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_digits

# Load high-dimensional dataset (64 features)
X, y = load_digits(return_X_y=True)
print(f"Original: {X.shape}")

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA retaining 95% variance
pca = PCA(n_components=0.95, svd_solver='full')
X_pca = pca.fit_transform(X_scaled)

print(f"PCA reduced: {X_pca.shape}")
print(f"Components retained: {pca.n_components_}")
print(f"Total variance retained: {pca.explained_variance_ratio_.sum():.4f}")

# Scree plot data
cum_var = np.cumsum(pca.explained_variance_ratio_)
n_for_80 = np.argmax(cum_var >= 0.80) + 1
n_for_95 = np.argmax(cum_var >= 0.95) + 1
print(f"Components for 80% variance: {n_for_80}")
print(f"Components for 95% variance: {n_for_95}")

# Reconstruct and measure error
X_reconstructed = pca.inverse_transform(X_pca)
X_reconstructed = scaler.inverse_transform(X_reconstructed)
reconstruction_error = np.mean((X - X_reconstructed) ** 2)
print(f"Reconstruction MSE: {reconstruction_error:.4f}")

# Assertions
assert X_pca.shape[0] == X.shape[0], "Row count mismatch after PCA"
assert X_pca.shape[1] < X.shape[1], "PCA must reduce dimensionality"
assert pca.explained_variance_ratio_.sum() >= 0.94, "Must retain ≥94% variance"
assert n_for_95 < X.shape[1], "Need fewer than 64 components for 95% variance"
print("✅ PCA assertions passed")''',

    # Week 4, Day 30: Month 1 Capstone: Math & Prep Mastery
    (4, 30): '''# Day 30: Month 1 Capstone — Math & Prep Integration
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

# Integrate everything from Month 1: linear algebra, stats, Pandas, NumPy, PCA
np.random.seed(42)

# 1. Linear algebra: eigendecomposition
A = np.array([[4, 2], [1, 3]], dtype=float)
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"Eigenvalues of A: {eigenvalues}")
assert len(eigenvalues) == 2, "2x2 matrix must have 2 eigenvalues"

# 2. Statistics: mean, std, correlation
data = pd.DataFrame({
    'feature1': np.random.normal(5, 2, 200),
    'feature2': np.random.normal(0, 1, 200),
    'target':   np.random.randint(0, 2, 200)
})
corr = data.corr()
print(f"Correlation matrix shape: {corr.shape}")
assert corr.shape == (3, 3), "Correlation must be 3x3"

# 3. Preprocessing pipeline
X = data[['feature1', 'feature2']].values
y = data['target'].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
assert np.allclose(X_scaled.mean(axis=0), 0, atol=1e-10), "Scaled mean must be ~0"
assert np.allclose(X_scaled.std(axis=0), 1, atol=1e-10), "Scaled std must be ~1"

# 4. PCA
pca = PCA(n_components=1)
X_pca = pca.fit_transform(X_scaled)
print(f"PCA explained: {pca.explained_variance_ratio_[0]:.4f}")

# 5. Classification
clf = LogisticRegression()
scores = cross_val_score(clf, X_scaled, y, cv=5)
print(f"CV accuracy: {scores.mean():.4f} ± {scores.std():.4f}")

# Month 1 final assertions
assert X_pca.shape == (200, 1), f"PCA shape wrong: {X_pca.shape}"
assert scores.mean() > 0.4, "Classifier should beat random chance"
print("✅ Month 1 Capstone: all math & prep assertions passed")''',

    # Week 5, Day 31: What is Machine Learning? Core Framework
    (5, 31): '''# Day 31: What is Machine Learning? — Core Framework
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

# Demonstrate the 3 ML paradigms with minimal examples
# 1. Supervised Learning — regression
np.random.seed(42)
X_sup = np.random.rand(200, 1) * 10
y_sup = 3 * X_sup.ravel() + np.random.randn(200) * 2

X_tr, X_te, y_tr, y_te = train_test_split(X_sup, y_sup, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_tr, y_tr)
r2 = r2_score(y_te, model.predict(X_te))
print(f"Supervised (Linear Reg) R²: {r2:.4f}")

# 2. Unsupervised Learning — k-means clustering
from sklearn.cluster import KMeans
X_unsup = np.vstack([
    np.random.normal([0,0], 0.5, (50,2)),
    np.random.normal([3,3], 0.5, (50,2)),
    np.random.normal([6,0], 0.5, (50,2)),
])
km = KMeans(n_clusters=3, random_state=42, n_init='auto')
labels = km.fit_predict(X_unsup)
unique_labels = len(set(labels))
print(f"Unsupervised (KMeans) clusters found: {unique_labels}")

# 3. The ML workflow: train/val/test split
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
Xi, yi = load_iris(return_X_y=True)
svc_scores = cross_val_score(SVC(kernel='rbf'), Xi, yi, cv=5)
print(f"Cross-val accuracy (SVM on Iris): {svc_scores.mean():.4f}")

# Core ML framework assertions
assert r2 > 0.9, f"Linear regression R² too low: {r2}"
assert unique_labels == 3, "K-means should recover 3 clusters"
assert svc_scores.mean() > 0.90, "SVM on Iris should exceed 90%"
print("✅ ML Core Framework assertions passed")''',

    # Week 5, Day 37: Week 5 Capstone
    (5, 37): '''# Day 37: Week 5 Capstone — End-to-End Scikit-learn Pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np

np.random.seed(42)
n = 600

df = pd.DataFrame({
    'age':       np.random.randint(18, 70, n).astype(float),
    'income':    np.random.exponential(50000, n),
    'education': np.random.choice(['HS','College','Graduate'], n),
    'region':    np.random.choice(['North','South','East','West'], n),
    'churn':     np.random.randint(0, 2, n),
})
# Inject some missing values
df.loc[np.random.choice(n, 40, replace=False), 'age'] = np.nan
df.loc[np.random.choice(n, 25, replace=False), 'income'] = np.nan

X = df.drop(columns='churn')
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build a full sklearn pipeline
numeric_features = ['age', 'income']
categorical_features = ['education', 'region']

numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler()),
])
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features),
])

full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier',   GradientBoostingClassifier(n_estimators=50, random_state=42)),
])

full_pipeline.fit(X_train, y_train)
preds = full_pipeline.predict(X_test)
print(classification_report(y_test, preds))

cv_scores = cross_val_score(full_pipeline, X, y, cv=5, scoring='f1')
print(f"CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

assert full_pipeline.named_steps['preprocessor'] is not None
assert cv_scores.mean() > 0.4, "Pipeline F1 must exceed 0.4"
print("✅ Week 5 Capstone pipeline assertions passed")''',

    # Week 6, Day 43: SVR + Tree-Based Regression
    (6, 43): '''# Day 43: SVR + Tree-Based Regression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error
import numpy as np

X, y = fetch_california_housing(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    'SVR': Pipeline([('scaler', StandardScaler()), ('svr', SVR(C=10, epsilon=0.1))]),
    'RF':  RandomForestRegressor(n_estimators=50, random_state=42),
    'GBM': GradientBoostingRegressor(n_estimators=50, learning_rate=0.1, random_state=42),
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    r2  = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    results[name] = {'r2': r2, 'mae': mae}
    print(f"{name:5s}: R²={r2:.4f}, MAE={mae:.4f}")

best_model = max(results, key=lambda k: results[k]['r2'])
print(f"Best model: {best_model} (R²={results[best_model]['r2']:.4f})")

assert results['RF']['r2'] > 0.7, f"RF R² too low: {results['RF']['r2']}"
assert results['GBM']['r2'] > 0.7, f"GBM R² too low: {results['GBM']['r2']}"
assert all(r['r2'] > 0 for r in results.values()), "All models must have positive R²"
print("✅ SVR + Tree-Based Regression assertions passed")''',

    # Week 6, Day 44: Capstone End-to-End House Price
    (6, 44): '''# Day 44: Capstone — End-to-End House Price Prediction
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error

X_raw, y = fetch_california_housing(return_X_y=True, as_frame=True)
X_raw['rooms_per_household'] = X_raw['AveRooms'] / X_raw['HouseAge'].clip(lower=1)
X_raw['bedrooms_per_room']   = X_raw['AveBedrms'] / X_raw['AveRooms'].clip(lower=0.1)

X = X_raw.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ridge + Polynomial features
ridge_pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('poly',   PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)),
    ('ridge',  Ridge(alpha=10.0)),
])
ridge_pipe.fit(X_train, y_train)
ridge_r2 = r2_score(y_test, ridge_pipe.predict(X_test))

# GBM
gbm = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1,
                                 max_depth=4, random_state=42)
gbm.fit(X_train, y_train)
gbm_r2 = r2_score(y_test, gbm.predict(X_test))
gbm_mae = mean_absolute_error(y_test, gbm.predict(X_test))

print(f"Ridge+Poly R²: {ridge_r2:.4f}")
print(f"GBM R²:        {gbm_r2:.4f}, MAE: {gbm_mae:.4f}")

# Feature importance
fi = pd.Series(gbm.feature_importances_, index=X_raw.columns).sort_values(ascending=False)
print(f"Top 3 features: {fi.index[:3].tolist()}")

assert ridge_r2 > 0.5, f"Ridge R² too low: {ridge_r2}"
assert gbm_r2 > 0.7, f"GBM R² too low: {gbm_r2}"
assert 'MedInc' in fi.index[:3], "MedInc should be a top feature"
print("✅ House Price Capstone assertions passed")''',

    # Week 7, Day 49: Customer Churn EDA + Feature Engineering
    (7, 49): '''# Day 49: Customer Churn — EDA + Feature Engineering
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

np.random.seed(42)
n = 1000

df = pd.DataFrame({
    'tenure':        np.random.randint(1, 72, n),
    'monthly_charges': np.random.uniform(20, 120, n),
    'contract':      np.random.choice(['Month-to-month', 'One year', 'Two year'], n, p=[0.55, 0.25, 0.20]),
    'payment_method': np.random.choice(['Electronic check', 'Credit card', 'Bank transfer', 'Mailed check'], n),
    'internet_service': np.random.choice(['DSL', 'Fiber optic', 'No'], n, p=[0.34, 0.44, 0.22]),
    'churn':         np.random.choice([0, 1], n, p=[0.73, 0.27])
})

# Feature engineering
df['total_charges'] = df['tenure'] * df['monthly_charges']
df['is_month_to_month'] = (df['contract'] == 'Month-to-month').astype(int)
df['has_fiber'] = (df['internet_service'] == 'Fiber optic').astype(int)
df['charges_per_month_ratio'] = df['monthly_charges'] / (df['tenure'] + 1)

# Encode categoricals
le = LabelEncoder()
for col in ['contract', 'payment_method', 'internet_service']:
    df[col + '_enc'] = le.fit_transform(df[col])

# Analysis
churn_by_contract = df.groupby('contract')['churn'].mean().round(3)
print("Churn rate by contract:")
print(churn_by_contract)

correlations = df.select_dtypes(include='number').corr()['churn'].abs().sort_values(ascending=False)
print(f"\nTop 5 correlations with churn:\n{correlations[1:6]}")

# Assertions
assert 'total_charges' in df.columns
assert 'is_month_to_month' in df.columns
assert df['total_charges'].notna().all(), "No missing total_charges"
assert churn_by_contract['Month-to-month'] > churn_by_contract['Two year'], "Month-to-month should have higher churn"
print("✅ Churn EDA + Feature Engineering assertions passed")''',

    # Week 7, Day 50: Customer Churn — Modeling
    (7, 50): '''# Day 50: Customer Churn — Modeling, Comparison & Tuning
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score

np.random.seed(42)
n = 1000

# Churn dataset with engineered features
X = np.column_stack([
    np.random.randint(1, 72, n),           # tenure
    np.random.uniform(20, 120, n),         # monthly_charges
    np.random.randint(0, 2, n),            # is_month_to_month
    np.random.randint(0, 2, n),            # has_fiber
    np.random.uniform(1, 60, n),           # charges_per_month_ratio
])
# Churn: higher probability with month-to-month + high charges
prob = 0.1 + 0.3 * X[:, 2] + 0.005 * (X[:, 1] - 60).clip(0)
prob = np.clip(prob, 0.05, 0.85)
y = (np.random.rand(n) < prob).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

models = {
    'LogReg': LogisticRegression(class_weight='balanced'),
    'RF':     RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
    'GBM':    GradientBoostingClassifier(n_estimators=100, random_state=42),
}

for name, clf in models.items():
    X_tr = X_train_s if name == 'LogReg' else X_train
    X_te = X_test_s if name == 'LogReg' else X_test
    clf.fit(X_tr, y_train)
    preds = clf.predict(X_te)
    proba = clf.predict_proba(X_te)[:, 1]
    auc = roc_auc_score(y_test, proba)
    print(f"{name:8s}: AUC={auc:.4f}")

best_auc = roc_auc_score(y_test, models['GBM'].predict_proba(X_test)[:, 1])
assert best_auc > 0.6, f"GBM AUC too low: {best_auc}"
print("✅ Churn Modeling assertions passed")''',

    # Week 7, Day 51: Customer Churn — Flask API
    (7, 51): '''# Day 51: Customer Churn — Flask API Deployment
from flask import Flask, request, jsonify
import numpy as np
import pickle
import os

# Build and serialize a churn model
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler

np.random.seed(42)
n = 800
X = np.random.rand(n, 5)
y = (X[:, 0] + X[:, 2] > 1.0).astype(int)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = GradientBoostingClassifier(n_estimators=50, random_state=42)
model.fit(X_scaled, y)

# Serialize model and scaler
MODEL_PATH  = '/tmp/churn_model.pkl'
SCALER_PATH = '/tmp/churn_scaler.pkl'
with open(MODEL_PATH, 'wb') as f: pickle.dump(model, f)
with open(SCALER_PATH, 'wb') as f: pickle.dump(scaler, f)

# Flask app
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': 'GBMChurn-v1.0'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = data.get('features')
    if not features or len(features) != 5:
        return jsonify({'error': 'Provide exactly 5 features'}), 400
    X_in = scaler.transform([features])
    proba = model.predict_proba(X_in)[0, 1]
    label = int(model.predict(X_in)[0])
    return jsonify({'churn_probability': round(float(proba), 4), 'prediction': label})

# Test with Flask test client
with app.test_client() as client:
    # Health check
    r = client.get('/health')
    assert r.status_code == 200
    assert b'healthy' in r.data

    # Prediction
    r2 = client.post('/predict', json={'features': [0.8, 0.2, 0.9, 0.1, 0.6]})
    assert r2.status_code == 200
    body = r2.get_json()
    assert 'churn_probability' in body
    assert 0.0 <= body['churn_probability'] <= 1.0

    # Error case
    r3 = client.post('/predict', json={'features': [1.0]})
    assert r3.status_code == 400

for f in [MODEL_PATH, SCALER_PATH]:
    os.remove(f)
print("Flask churn API:", body)
print("✅ Flask API assertions passed")''',

    # Week 12, Day 82-86: Seq2Seq Image Captioning Capstone parts
    (12, 82): '''# Day 82: Image Captioning Capstone Part 1 — Dataset & Visual Grid
import numpy as np
from collections import Counter
import re

# Simulated COCO-style caption dataset
np.random.seed(42)
CAPTIONS = [
    "a dog playing in the park", "two cats sitting on a sofa",
    "a red car parked on the street", "children running in the playground",
    "a woman reading a book near the window", "birds flying over the ocean",
    "a sunset over the mountains with clouds", "a man cycling on a path",
    "fresh fruits on a wooden table", "a crowded city street at night",
] * 50  # 500 image-caption pairs

def build_vocab(captions, min_freq=2):
    """Build vocabulary from captions."""
    tokens = []
    for cap in captions:
        tokens.extend(re.findall(r'\w+', cap.lower()))
    freq = Counter(tokens)
    vocab = ['<PAD>', '<SOS>', '<EOS>', '<UNK>'] + [w for w, f in freq.items() if f >= min_freq]
    return {w: i for i, w in enumerate(vocab)}, vocab

def tokenize(caption, word2idx, max_len=20):
    """Convert caption to padded token indices."""
    tokens = ['<SOS>'] + re.findall(r'\w+', caption.lower()) + ['<EOS>']
    indices = [word2idx.get(t, word2idx['<UNK>']) for t in tokens]
    if len(indices) < max_len:
        indices += [word2idx['<PAD>']] * (max_len - len(indices))
    return indices[:max_len]

word2idx, vocab = build_vocab(CAPTIONS)
print(f"Vocab size: {len(vocab)}")

tokenized = np.array([tokenize(cap, word2idx) for cap in CAPTIONS])
print(f"Tokenized shape: {tokenized.shape}")

# Assertions
assert len(vocab) > 30, f"Vocab too small: {len(vocab)}"
assert tokenized.shape == (500, 20), f"Shape wrong: {tokenized.shape}"
assert tokenized[:, 0].mean() == word2idx['<SOS>'], "First token should be <SOS>"
print("✅ Dataset & vocabulary assertions passed")''',

    (12, 83): '''# Day 83: Image Captioning Capstone Part 2 — Attention-Augmented Decoder
import numpy as np

def scaled_dot_product_attention(Q, K, V):
    """Core attention mechanism: softmax(QK^T/sqrt(d_k)) * V"""
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    # Softmax
    scores -= scores.max(axis=-1, keepdims=True)
    attn_weights = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)
    return attn_weights @ V, attn_weights

class BahdanauAttention:
    """Additive (Bahdanau) attention: score = v^T tanh(W1*h + W2*s)"""
    def __init__(self, d_hidden):
        np.random.seed(42)
        self.W1 = np.random.randn(d_hidden, d_hidden) * 0.01
        self.W2 = np.random.randn(d_hidden, d_hidden) * 0.01
        self.v  = np.random.randn(d_hidden) * 0.01

    def compute(self, encoder_states, decoder_state):
        """encoder_states: (T_enc, d), decoder_state: (d,)"""
        energy = np.tanh(encoder_states @ self.W1.T + decoder_state @ self.W2.T)  # (T, d)
        scores = energy @ self.v  # (T,)
        weights = np.exp(scores - scores.max()) / np.exp(scores - scores.max()).sum()
        context = weights @ encoder_states  # (d,)
        return context, weights

# Test attention mechanisms
T_enc, d = 10, 64
encoder_outputs = np.random.randn(T_enc, d)
decoder_state   = np.random.randn(d)

# Bahdanau
attn = BahdanauAttention(d)
context, weights = attn.compute(encoder_outputs, decoder_state)
print(f"Context vector shape: {context.shape}")
print(f"Attention weights sum: {weights.sum():.6f}")

# Scaled dot-product
Q = decoder_state.reshape(1, -1)
K = encoder_outputs
V = encoder_outputs
sdpa_out, sdpa_weights = scaled_dot_product_attention(Q, K, V)

assert context.shape == (d,), f"Context shape wrong: {context.shape}"
assert np.allclose(weights.sum(), 1.0, atol=1e-6), "Attention weights must sum to 1"
assert sdpa_weights.shape == (1, T_enc)
print("✅ Attention mechanism assertions passed")''',

    (12, 84): '''# Day 84: Image Captioning Capstone Part 3 — Training & BLEU Evaluation
import numpy as np
from collections import Counter

def compute_bleu(reference: list, hypothesis: list, n: int = 4) -> float:
    """Compute corpus BLEU score (simplified, no brevity penalty for demo)."""
    precisions = []
    for gram_n in range(1, n + 1):
        ref_ngrams  = Counter(zip(*[reference[i:] for i in range(gram_n)]))
        hyp_ngrams  = Counter(zip(*[hypothesis[i:] for i in range(gram_n)]))
        matches = sum((hyp_ngrams & ref_ngrams).values())
        total   = max(sum(hyp_ngrams.values()), 1)
        precisions.append(matches / total)

    # Geometric mean of precisions
    if min(precisions) == 0:
        return 0.0
    log_avg = np.mean([np.log(p) for p in precisions])
    return float(np.exp(log_avg))

# Simulate epoch training with decreasing loss
class SimpleSeq2Seq:
    def __init__(self, vocab_size=50, d_model=64):
        np.random.seed(42)
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.loss = 3.5  # initial cross-entropy

    def train_epoch(self, lr=0.01):
        """Simulate one training epoch."""
        self.loss *= (1 - lr * 0.3 + np.random.randn() * 0.01)
        self.loss = max(self.loss, 0.5)
        return self.loss

    def generate(self, length=8):
        """Simulate greedy decoding."""
        return list(np.random.randint(4, self.vocab_size, length))

model = SimpleSeq2Seq()
losses = []
for epoch in range(10):
    loss = model.train_epoch()
    losses.append(loss)
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1}: loss={loss:.4f}")

# BLEU evaluation
reference  = [5, 12, 3, 7, 9, 14, 2, 6]
hypothesis = [5, 12, 3, 8, 9, 14, 2, 6]  # slight error
bleu = compute_bleu(reference, hypothesis, n=4)
print(f"BLEU-4 score: {bleu:.4f}")

assert losses[-1] < losses[0], "Loss should decrease over training"
assert 0.0 <= bleu <= 1.0, f"BLEU out of range: {bleu}"
print("✅ Training + BLEU evaluation assertions passed")''',

    (12, 85): '''# Day 85: Image Captioning Capstone Part 4 — Greedy vs Beam Search
import numpy as np

def greedy_decode(logits_sequence):
    """Greedy decoding: take argmax at each step."""
    return [np.argmax(step) for step in logits_sequence]

def beam_search(logits_sequence, beam_width=3, eos_token=2):
    """
    Beam search decoding.
    logits_sequence: list of (vocab_size,) arrays, one per step
    Returns: list of token ids (best beam)
    """
    # Each beam: (score, token_sequence)
    beams = [(0.0, [])]
    completed = []

    for step_logits in logits_sequence:
        probs = np.exp(step_logits - step_logits.max())
        probs /= probs.sum()  # softmax
        log_probs = np.log(probs + 1e-9)

        new_beams = []
        for score, seq in beams:
            top_k = np.argsort(log_probs)[-beam_width:]
            for token in top_k:
                new_score = score + log_probs[token]
                new_seq = seq + [int(token)]
                if int(token) == eos_token:
                    completed.append((new_score / len(new_seq), new_seq))
                else:
                    new_beams.append((new_score, new_seq))

        # Keep top beam_width beams
        new_beams.sort(key=lambda x: -x[0])
        beams = new_beams[:beam_width]

    if not completed:
        # Return best beam
        return max(beams, key=lambda x: x[0] / max(len(x[1]),1))[1]
    return max(completed, key=lambda x: x[0])[1]

# Test both decoders
np.random.seed(42)
vocab_size = 30
T = 8  # sequence length
logits = [np.random.randn(vocab_size) for _ in range(T)]

greedy_out = greedy_decode(logits)
beam_out   = beam_search(logits, beam_width=3)

print(f"Greedy output: {greedy_out}")
print(f"Beam search output: {beam_out}")
print(f"Greedy length: {len(greedy_out)}, Beam length: {len(beam_out)}")

assert len(greedy_out) == T, "Greedy should have T outputs"
assert len(beam_out) >= 1, "Beam search must produce output"
assert all(0 <= t < vocab_size for t in greedy_out), "All tokens must be in vocab range"
print("✅ Greedy vs Beam Search assertions passed")''',

    (12, 86): '''# Day 86: Image Captioning Capstone Part 5 — Gradio-style Web Deployment
# Simulates a Gradio UI for image captioning (no actual Gradio install required)
import numpy as np
import json

class CaptioningModel:
    """Mock image captioning model for deployment demo."""
    TEMPLATES = [
        "a {adj} {obj} {action} in the {location}",
        "{count} {obj}s {action} on a {location}",
        "a person {action} near a {obj} in the {location}",
    ]
    VOCAB = {
        'adj': ['small', 'large', 'colorful', 'wooden', 'bright'],
        'obj': ['dog', 'cat', 'car', 'tree', 'bird'],
        'action': ['playing', 'resting', 'running', 'sitting', 'flying'],
        'location': ['park', 'street', 'beach', 'garden', 'room'],
        'count': ['two', 'three', 'several', 'many'],
    }

    def predict(self, image_array: np.ndarray) -> dict:
        """Generate caption for an image array."""
        np.random.seed(int(image_array.sum()) % 2**31)
        template = np.random.choice(self.TEMPLATES)
        caption = template.format(**{k: np.random.choice(v) for k, v in self.VOCAB.items()})
        confidence = float(np.random.uniform(0.65, 0.95))
        return {'caption': caption, 'confidence': round(confidence, 4)}

def gradio_predict_fn(image_array: np.ndarray) -> str:
    """Gradio-compatible prediction function."""
    model = CaptioningModel()
    result = model.predict(image_array)
    return json.dumps(result, indent=2)

# Simulate Gradio deployment test
test_images = [np.random.randint(0, 255, (224, 224, 3)) for _ in range(5)]
outputs = [gradio_predict_fn(img) for img in test_images]

for i, out in enumerate(outputs):
    result = json.loads(out)
    print(f"Image {i+1}: {result['caption']} (confidence={result['confidence']})")

# Assertions
for out in outputs:
    result = json.loads(out)
    assert 'caption' in result
    assert 'confidence' in result
    assert 0.5 < result['confidence'] <= 1.0
    assert len(result['caption'].split()) >= 5, "Caption should be ≥5 words"

print("✅ Gradio deployment assertions passed")''',

    # Week 14, Day 100: Deployment & Model Serving Capstone
    (14, 100): '''# Day 100: Capstone Part 2 — Model Serving & Deployment
from flask import Flask, request, jsonify
import numpy as np
import pickle, os

# Train a production-ready model
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

np.random.seed(42)
X = np.random.randn(500, 8)
y = (X[:, 0] + X[:, 2] - X[:, 5] > 0.5).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_train)
X_te_s = scaler.transform(X_test)
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_tr_s, y_train)
test_acc = model.score(X_te_s, y_test)
print(f"Test accuracy: {test_acc:.4f}")

# Serialize
MODEL_PATH = '/tmp/day100_model.pkl'
SCALER_PATH = '/tmp/day100_scaler.pkl'
with open(MODEL_PATH, 'wb') as f: pickle.dump(model, f)
with open(SCALER_PATH, 'wb') as f: pickle.dump(scaler, f)

# Flask serving app
app = Flask(__name__)
_model = pickle.load(open(MODEL_PATH, 'rb'))
_scaler = pickle.load(open(SCALER_PATH, 'rb'))

@app.route('/health')
def health(): return jsonify({'status': 'ok', 'version': '1.0', 'accuracy': round(test_acc, 4)})

@app.route('/predict', methods=['POST'])
def predict():
    body = request.get_json()
    features = body.get('features')
    if not features or len(features) != 8:
        return jsonify({'error': 'Exactly 8 features required'}), 400
    X_in = _scaler.transform([features])
    pred = int(_model.predict(X_in)[0])
    prob = float(_model.predict_proba(X_in)[0].max())
    return jsonify({'prediction': pred, 'confidence': round(prob, 4)})

with app.test_client() as c:
    r_health = c.get('/health')
    r_predict = c.post('/predict', json={'features': [0.5]*8})
    r_error   = c.post('/predict', json={'features': [1.0]})
    assert r_health.status_code == 200
    assert r_predict.status_code == 200
    assert r_error.status_code == 400
    body = r_predict.get_json()
    assert 'prediction' in body and body['prediction'] in [0, 1]

for f in [MODEL_PATH, SCALER_PATH]: os.remove(f)
print("✅ Model Serving Capstone assertions passed")''',

    # Week 15, Day 106: LLM Agents & Tool Use
    (15, 106): '''# Day 106: LLM Agents & Tool Use
from typing import Callable, Dict, Any, List, Optional
import json, re, math

# Define agent tools
class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register(self, name: str, fn: Callable, description: str):
        self._tools[name] = {'fn': fn, 'description': description}

    def call(self, name: str, **kwargs) -> str:
        if name not in self._tools:
            return f"Error: Tool '{name}' not found. Available: {list(self._tools.keys())}"
        try:
            return str(self._tools[name]['fn'](**kwargs))
        except Exception as e:
            return f"Error calling {name}: {e}"

    def schema(self) -> List[dict]:
        return [{'name': k, 'description': v['description']} for k, v in self._tools.items()]

# Register tools
registry = ToolRegistry()

registry.register("calculator", lambda expression: eval(expression, {"__builtins__": {}, "math": math}),
                  "Evaluate a math expression. Example: '2 ** 10' or 'math.sqrt(144)'")

registry.register("weather", lambda city: json.dumps({"city": city, "temp_c": 22, "condition": "sunny"}),
                  "Get current weather for a city. Input: city name string.")

registry.register("word_count", lambda text: f"{len(text.split())} words, {len(text)} chars",
                  "Count words and characters in text.")

# Simulate agent loop
class ToolCallingAgent:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.max_steps = 5

    def run(self, task: str) -> str:
        """Simplified agent: parse tool calls from task description."""
        # For testing: extract tool calls from task description using regex
        tool_pattern = re.compile(r'(\w+)\(([^)]+)\)')
        matches = tool_pattern.findall(task)

        results = []
        for tool_name, args_str in matches:
            result = self.registry.call(tool_name, expression=args_str) if tool_name == 'calculator' \
                else self.registry.call(tool_name, city=args_str.strip('"\'')) if tool_name == 'weather' \
                else self.registry.call(tool_name, text=args_str.strip('"\''))
            results.append(f"{tool_name}({args_str}) = {result}")

        return '\n'.join(results) if results else "No tool calls found in task."

agent = ToolCallingAgent(registry)
output = agent.run("Calculate: calculator(2**10 + math.sqrt(144))")
print(f"Calculator result: {output}")

weather = registry.call("weather", city="Mumbai")
wc = registry.call("word_count", text="Transformer models use self-attention mechanisms")

print(f"Weather: {weather}")
print(f"Word count: {wc}")

assert "1024" in output or "1036" in output, f"Calculator failed: {output}"
weather_data = json.loads(weather)
assert weather_data['city'] == "Mumbai"
assert "words" in wc
print("✅ LLM Agents & Tool Use assertions passed")''',

    # Week 15, Day 107: Capstone Agentic Systems
    (15, 107): '''# Day 107: Capstone — Agentic Systems (Full Pipeline)
from typing import Dict, List, Callable, Optional, Any
import json, re

# Full agentic pipeline: Plan → Execute → Reflect → Synthesize

class AgentMemory:
    """Working memory for agent context."""
    def __init__(self, max_items: int = 20):
        self.short_term: List[Dict] = []
        self.max_items = max_items

    def add(self, role: str, content: str):
        self.short_term.append({'role': role, 'content': content})
        if len(self.short_term) > self.max_items:
            self.short_term.pop(0)

    def to_context(self) -> str:
        return '\n'.join(f"{m['role']}: {m['content']}" for m in self.short_term[-10:])

class Planner:
    """Breaks goal into subtask steps."""
    def plan(self, goal: str) -> List[str]:
        return [
            f"Step 1: Analyze the goal: {goal}",
            "Step 2: Gather relevant information",
            "Step 3: Execute core computation",
            "Step 4: Validate results",
            f"Step 5: Synthesize final answer for: {goal}"
        ]

class Executor:
    """Executes individual plan steps."""
    def execute(self, step: str, context: str) -> str:
        if "Analyze" in step:
            return f"Goal analysis complete. Key components identified."
        elif "Gather" in step:
            return "Information gathered from knowledge base and tools."
        elif "Execute" in step:
            return "Core computation executed. Result: 42.0 (simulated)"
        elif "Validate" in step:
            return "Validation passed. Result within expected bounds."
        elif "Synthesize" in step:
            return "Synthesis complete. Final answer compiled."
        return f"Step completed: {step[:50]}"

class ReflectiveCritic:
    """Evaluates execution quality."""
    def reflect(self, step_results: List[str]) -> dict:
        issues = [r for r in step_results if 'error' in r.lower() or 'failed' in r.lower()]
        return {
            'quality_score': max(0.0, 1.0 - 0.2 * len(issues)),
            'issues': issues,
            'recommendation': 'Proceed to synthesis' if not issues else 'Retry failed steps'
        }

# Full pipeline execution
goal = "Analyze ML model performance trends and recommend optimization strategy"

memory = AgentMemory()
planner = Planner()
executor = Executor()
critic = ReflectiveCritic()

memory.add("user", goal)
steps = planner.plan(goal)
print(f"Plan: {len(steps)} steps")

results = []
for step in steps:
    result = executor.execute(step, memory.to_context())
    memory.add("agent", result)
    results.append(result)
    print(f"  {step[:60]}: ✓")

reflection = critic.reflect(results)
print(f"\nQuality score: {reflection['quality_score']:.2f}")
print(f"Recommendation: {reflection['recommendation']}")

assert len(steps) == 5, "Planner should create 5 steps"
assert len(results) == 5, "Executor should complete all steps"
assert reflection['quality_score'] >= 0.8, f"Quality too low: {reflection['quality_score']}"
print("✅ Agentic Systems Capstone assertions passed")''',

    # Week 16, Days 113-117: Streaming, Next.js, LangSmith, RAGAS, RAG Deployment
    (16, 113): '''# Day 113: Streaming Responses & Real-Time AI Interface
import time
from typing import Generator, Iterator

def stream_tokens(text: str, delay_ms: float = 0) -> Generator[str, None, None]:
    """Simulate token-by-token streaming (OpenAI-style)."""
    tokens = text.split()
    for token in tokens:
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
        yield token + ' '
    yield '[DONE]'

def stream_response(prompt: str, max_tokens: int = 50) -> dict:
    """Process streaming response and collect metrics."""
    response_text = (
        f"Streaming response to: {prompt[:30]}... "
        "Token-by-token output enables real-time UI updates and better UX. "
        "Each token triggers a server-sent event (SSE) to the client."
    )
    tokens = response_text.split()[:max_tokens]

    collected = []
    first_token_time = None
    start = time.time()

    for i, chunk in enumerate(stream_tokens(' '.join(tokens))):
        if chunk != '[DONE]':
            if first_token_time is None:
                first_token_time = time.time() - start
            collected.append(chunk)

    ttft = first_token_time or 0.0  # Time to First Token
    total_tokens = len(collected)
    tps = total_tokens / max(time.time() - start, 0.001)  # tokens per second

    return {
        'text': ''.join(collected).strip(),
        'metrics': {
            'ttft_ms': round(ttft * 1000, 2),
            'total_tokens': total_tokens,
            'tokens_per_second': round(tps, 1),
        }
    }

# Test streaming
result = stream_response("Explain transformer architecture", max_tokens=30)
print(f"Response preview: {result['text'][:80]}...")
print(f"Metrics: {result['metrics']}")

assert result['text'] != '', "Response must not be empty"
assert result['metrics']['total_tokens'] > 5, "Must have >5 tokens"
assert result['metrics']['ttft_ms'] >= 0, "TTFT must be non-negative"
print("✅ Streaming Response assertions passed")''',

    (16, 114): '''# Day 114: Next.js & Vercel AI SDK — API route implementation
import json
from typing import Dict, Any
from dataclasses import dataclass

# Simulate a Next.js API Route handler (Python equivalent)
@dataclass
class Request:
    method: str
    body: Dict[str, Any]
    headers: Dict[str, str]

@dataclass
class Response:
    status_code: int
    body: Dict[str, Any]
    headers: Dict[str, str]

def handle_chat_api(req: Request) -> Response:
    """
    Simulates: pages/api/chat.ts
    POST /api/chat { messages: [...] }
    Returns streaming AI response
    """
    if req.method != 'POST':
        return Response(405, {'error': 'Method not allowed'}, {})

    messages = req.body.get('messages', [])
    if not messages or not isinstance(messages, list):
        return Response(400, {'error': 'messages array required'}, {})

    last_msg = messages[-1].get('content', '')
    if not last_msg:
        return Response(400, {'error': 'Last message must have content'}, {})

    # Simulate AI response generation
    response_text = f"AI response to: {last_msg[:50]}"
    usage = {'prompt_tokens': len(last_msg.split()), 'completion_tokens': len(response_text.split())}

    return Response(
        status_code=200,
        body={'id': 'chatcmpl-day114', 'choices': [{'message': {'role': 'assistant', 'content': response_text}}], 'usage': usage},
        headers={'Content-Type': 'application/json', 'X-Model': 'gpt-4-turbo'}
    )

# Test the API route
req_ok  = Request('POST', {'messages': [{'role': 'user', 'content': 'What is RAG?'}]}, {})
req_bad_method = Request('GET', {}, {})
req_no_msg = Request('POST', {'messages': []}, {})

resp_ok  = handle_chat_api(req_ok)
resp_bad = handle_chat_api(req_bad_method)
resp_nm  = handle_chat_api(req_no_msg)

print(f"OK: {resp_ok.status_code}, {json.dumps(resp_ok.body)[:80]}")
assert resp_ok.status_code == 200
assert 'choices' in resp_ok.body
assert resp_ok.body['choices'][0]['message']['role'] == 'assistant'
assert resp_bad.status_code == 405
assert resp_nm.status_code == 400
print("✅ Next.js API Route assertions passed")''',

    (16, 115): '''# Day 115: LLM Observability with LangSmith & Phoenix
import json, uuid, time, random
from datetime import datetime
from typing import List, Dict, Any

class ObservabilityTrace:
    """Simulates LangSmith/Phoenix trace structure."""

    def __init__(self, project: str):
        self.project = project
        self.traces: List[Dict] = []

    def trace(self, name: str, inputs: Dict, outputs: Dict,
               metadata: Dict = None, error: str = None):
        """Record a trace for a LLM call."""
        trace = {
            'trace_id':  str(uuid.uuid4())[:8],
            'name':      name,
            'project':   self.project,
            'timestamp': datetime.now().isoformat(),
            'inputs':    inputs,
            'outputs':   outputs,
            'latency_ms': random.randint(50, 500),
            'tokens':    {'prompt': len(str(inputs).split()), 'completion': len(str(outputs).split())},
            'error':     error,
            'metadata':  metadata or {},
        }
        self.traces.append(trace)
        return trace

    def get_stats(self) -> Dict:
        successful = [t for t in self.traces if not t['error']]
        return {
            'total_traces': len(self.traces),
            'success_rate': len(successful) / max(len(self.traces), 1),
            'avg_latency_ms': sum(t['latency_ms'] for t in self.traces) / max(len(self.traces), 1),
            'total_tokens': sum(t['tokens']['prompt'] + t['tokens']['completion'] for t in self.traces)
        }

# Run observability demo
tracer = ObservabilityTrace(project="day115-rag-pipeline")

for i in range(10):
    error = "TimeoutError" if random.random() < 0.1 else None
    tracer.trace(
        name=f"rag_query_{i}",
        inputs={'query': f"Question {i}: What is attention?"},
        outputs={'answer': f"Answer {i}: Attention is..." if not error else ''},
        metadata={'model': 'gpt-4', 'temperature': 0.7},
        error=error
    )

stats = tracer.get_stats()
print(f"Observability stats: {json.dumps(stats, indent=2)}")

assert stats['total_traces'] == 10
assert 0.0 <= stats['success_rate'] <= 1.0
assert stats['avg_latency_ms'] > 0
assert stats['total_tokens'] > 0
print("✅ LLM Observability assertions passed")''',

    (16, 116): '''# Day 116: LLM Evaluation — RAGAS & TruLens Metrics
from typing import List, Dict, Tuple
import numpy as np

def answer_relevancy(question: str, answer: str) -> float:
    """RAGAS: measure if answer addresses the question."""
    q_words = set(question.lower().split())
    a_words = set(answer.lower().split())
    overlap = len(q_words & a_words) / max(len(q_words), 1)
    return min(1.0, overlap * 3.0)  # scale overlap to [0,1]

def faithfulness(answer: str, contexts: List[str]) -> float:
    """RAGAS: measure if answer claims are supported by context."""
    if not contexts:
        return 0.0
    a_words = set(answer.lower().split())
    context_words = set(' '.join(contexts).lower().split())
    supported = len(a_words & context_words) / max(len(a_words), 1)
    return min(1.0, supported * 2.0)

def context_recall(answer: str, contexts: List[str], ground_truth: str) -> float:
    """RAGAS: fraction of ground truth claims found in context."""
    gt_words = set(ground_truth.lower().split())
    ctx_words = set(' '.join(contexts).lower().split())
    recall = len(gt_words & ctx_words) / max(len(gt_words), 1)
    return min(1.0, recall)

def ragas_score(question, answer, contexts, ground_truth) -> Dict[str, float]:
    """Composite RAGAS evaluation."""
    ar = answer_relevancy(question, answer)
    f  = faithfulness(answer, contexts)
    cr = context_recall(answer, contexts, ground_truth)
    return {
        'answer_relevancy': round(ar, 4),
        'faithfulness':     round(f, 4),
        'context_recall':   round(cr, 4),
        'ragas_score':      round((ar + f + cr) / 3, 4)
    }

# Test RAGAS evaluation
test_cases = [
    {
        'question':    "What is attention in transformers?",
        'answer':      "Attention is a mechanism that computes weighted sums of values based on query-key similarity in transformer models.",
        'contexts':    ["Attention mechanisms compute scaled dot-product scores between queries and keys, then use them to weight values.",
                        "Transformers use multi-head attention to capture different aspects of the input sequence."],
        'ground_truth': "Attention computes weighted combinations of values using query-key similarity scores in transformer architectures."
    }
]

for tc in test_cases:
    scores = ragas_score(**tc)
    print(f"RAGAS scores: {scores}")
    assert scores['ragas_score'] >= 0.0
    assert scores['faithfulness'] >= 0.0
    assert all(0 <= v <= 1.0 for v in scores.values())

print("✅ RAGAS LLM Evaluation assertions passed")''',

    (16, 117): '''# Day 117: Week 16 Capstone — Production RAG Deployment
from typing import List, Dict, Any, Optional
import numpy as np, json, hashlib

class EmbeddingModel:
    """Mock embedding model (replace with sentence-transformers in production)."""
    def embed(self, text: str) -> np.ndarray:
        hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
        np.random.seed(hash_val % (2**31))
        return np.random.randn(384)  # 384-dim embedding

class VectorStore:
    """In-memory vector store for RAG retrieval."""
    def __init__(self, embedder: EmbeddingModel):
        self.embedder = embedder
        self.docs: List[str] = []
        self.vectors: List[np.ndarray] = []

    def add(self, docs: List[str]):
        for doc in docs:
            self.docs.append(doc)
            self.vectors.append(self.embedder.embed(doc))

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.vectors:
            return []
        q_vec = self.embedder.embed(query)
        sims = [np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v) + 1e-9)
                for v in self.vectors]
        top_indices = np.argsort(sims)[::-1][:top_k]
        return [{'doc': self.docs[i], 'score': float(sims[i])} for i in top_indices]

class ProductionRAG:
    """Full RAG pipeline: retrieve + augment + generate."""
    def __init__(self, vector_store: VectorStore):
        self.vs = vector_store

    def answer(self, question: str) -> Dict[str, Any]:
        retrieved = self.vs.retrieve(question, top_k=3)
        context = '\n'.join(r['doc'] for r in retrieved)
        answer = f"Based on context: {context[:100]}... Answer: {question} is addressed by the retrieved documents."
        return {'answer': answer, 'sources': retrieved, 'context_docs': len(retrieved)}

# Build and test production RAG
corpus = [
    "Attention mechanisms compute scaled dot-product attention over queries, keys, and values.",
    "BERT uses bidirectional attention for masked language modeling pre-training.",
    "GPT uses autoregressive attention to generate text one token at a time.",
    "vLLM implements PagedAttention for efficient KV-cache management in serving.",
    "RAG combines retrieval with generation for knowledge-grounded responses.",
    "LangGraph enables stateful multi-step agent workflows with cycles and branching.",
]

embedder = EmbeddingModel()
store = VectorStore(embedder)
store.add(corpus)

rag = ProductionRAG(store)
result = rag.answer("How does attention work in transformers?")

print(f"Answer: {result['answer'][:100]}...")
print(f"Sources retrieved: {result['context_docs']}")

assert result['context_docs'] == 3, "Should retrieve top-3 docs"
assert len(result['answer']) > 20, "Answer must be non-trivial"
assert all(0.0 <= s['score'] for s in result['sources']), "Scores must be non-negative"
print("✅ Production RAG Capstone assertions passed")''',

    # Week 17, Days 119, 120, 123, 124
    (17, 119): '''# Day 119: REST API Design — JSON, Status Codes & Versioning
from flask import Flask, request, jsonify
from functools import wraps
import json

app = Flask(__name__)

# API versioning decorator
def versioned(version="v1"):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resp = f(*args, **kwargs)
            if isinstance(resp, dict):
                return jsonify({"api_version": version, "data": resp})
            return resp
        return wrapper
    return decorator

# RESTful user resource
users_db = {1: {"id": 1, "name": "Alice", "email": "alice@example.com"}}

@app.route("/api/v1/users", methods=["GET"])
@versioned("v1")
def list_users():
    return list(users_db.values())

@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users_db.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"api_version": "v1", "data": user})

@app.route("/api/v1/users", methods=["POST"])
def create_user():
    body = request.get_json()
    if not body or "name" not in body or "email" not in body:
        return jsonify({"error": "name and email required"}), 400
    new_id = max(users_db.keys()) + 1
    user = {"id": new_id, "name": body["name"], "email": body["email"]}
    users_db[new_id] = user
    return jsonify(user), 201

@app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users_db:
        return jsonify({"error": "Not found"}), 404
    del users_db[user_id]
    return "", 204

# Test
with app.test_client() as c:
    r_list = c.get("/api/v1/users")
    assert r_list.status_code == 200
    assert r_list.get_json()["api_version"] == "v1"

    r_get = c.get("/api/v1/users/1")
    assert r_get.status_code == 200
    assert r_get.get_json()["data"]["name"] == "Alice"

    r_create = c.post("/api/v1/users", json={"name": "Bob", "email": "bob@example.com"})
    assert r_create.status_code == 201
    new_id = r_create.get_json()["id"]

    r_del = c.delete(f"/api/v1/users/{new_id}")
    assert r_del.status_code == 204

    r_404 = c.get(f"/api/v1/users/9999")
    assert r_404.status_code == 404

    r_bad = c.post("/api/v1/users", json={"name": "NoEmail"})
    assert r_bad.status_code == 400

print("REST API: all 5 test scenarios passed")
print("✅ REST API Design assertions passed")''',

    (17, 120): '''# Day 120: Serving ML Models with Flask — Pickle, Joblib & Gunicorn
import pickle, io, os
import numpy as np
from flask import Flask, request, jsonify
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Train a model
np.random.seed(42)
X = np.random.randn(400, 4)
y = (X[:, 0] + X[:, 2] > 0).astype(int)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', LogisticRegression())
])
pipeline.fit(X, y)

# Serialize with pickle (in-memory for test)
buf = io.BytesIO()
pickle.dump(pipeline, buf)
buf.seek(0)
loaded_pipeline = pickle.load(buf)

# Flask serving
app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "model_type": type(loaded_pipeline).__name__})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = data.get("features")
    if not features or len(features) != 4:
        return jsonify({"error": "Provide exactly 4 features"}), 400
    X_in = np.array([features])
    pred = int(loaded_pipeline.predict(X_in)[0])
    proba = loaded_pipeline.predict_proba(X_in)[0].tolist()
    return jsonify({"prediction": pred, "probabilities": [round(p, 4) for p in proba]})

with app.test_client() as c:
    r = c.get("/health")
    assert r.status_code == 200 and "healthy" in r.data.decode()

    r2 = c.post("/predict", json={"features": [0.5, -0.3, 1.2, 0.8]})
    assert r2.status_code == 200
    body = r2.get_json()
    assert "prediction" in body and body["prediction"] in [0, 1]
    assert len(body["probabilities"]) == 2
    assert abs(sum(body["probabilities"]) - 1.0) < 1e-4

    r3 = c.post("/predict", json={"features": [1.0, 2.0]})
    assert r3.status_code == 400

print("Flask ML serving tests all passed")
print("✅ Model Serving with Flask assertions passed")''',

    (17, 123): '''# Day 123: Docker Compose — Multi-Container ML Stacks
# Validates Docker Compose YAML structure for a multi-service ML deployment
import yaml as yaml_lib
from typing import Dict, Any

COMPOSE_YAML = """
version: "3.9"
services:
  model_api:
    image: my-ml-api:latest
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/models/classifier.pkl
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/models
    depends_on:
      - redis
      - postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=mlops_db
      - POSTGRES_USER=mluser
      - POSTGRES_PASSWORD=mlpassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mluser"]
      interval: 10s
      timeout: 5s
      retries: 5

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

volumes:
  postgres_data:
"""

def validate_compose(compose_str: str) -> Dict[str, Any]:
    """Validate Docker Compose configuration."""
    config = yaml_lib.safe_load(compose_str)
    services = config.get("services", {})
    errors = []

    for svc_name, svc in services.items():
        if "image" not in svc and "build" not in svc:
            errors.append(f"{svc_name}: must have 'image' or 'build'")
        if svc.get("depends_on"):
            for dep in svc["depends_on"]:
                if dep not in services:
                    errors.append(f"{svc_name}: depends_on '{dep}' not defined")

    return {"services": list(services.keys()), "valid": len(errors) == 0, "errors": errors}

result = validate_compose(COMPOSE_YAML)
print(f"Services: {result['services']}")
print(f"Valid: {result['valid']}")
if result['errors']:
    print(f"Errors: {result['errors']}")

assert result['valid'], f"Compose invalid: {result['errors']}"
assert 'model_api' in result['services']
assert 'redis' in result['services']
assert 'postgres' in result['services']
assert len(result['services']) == 4
print("✅ Docker Compose multi-container assertions passed")''',

    (17, 124): '''# Day 124: Week 17 Capstone — Full ML System Deployment
from typing import Dict, Any, List
import json, time, random, hashlib

# Capstone: architect a complete ML system with all Week 17 components

class MLSystemConfig:
    """Configuration-driven ML deployment system."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._validate()

    def _validate(self):
        required = ["model_name", "api_version", "serving", "monitoring"]
        missing = [k for k in required if k not in self.config]
        if missing:
            raise ValueError(f"Missing config keys: {missing}")

class ModelRegistry:
    """Model versioning and artifact storage."""
    def __init__(self):
        self._registry: Dict[str, Dict] = {}

    def register(self, name: str, version: str, metrics: Dict) -> str:
        key = f"{name}:{version}"
        self._registry[key] = {
            "name": name, "version": version,
            "metrics": metrics,
            "artifact_hash": hashlib.md5(f"{name}{version}".encode()).hexdigest()[:8],
            "registered_at": time.time()
        }
        return key

    def get_champion(self, name: str) -> Dict:
        candidates = {k: v for k, v in self._registry.items() if v["name"] == name}
        if not candidates:
            raise KeyError(f"No models registered for '{name}'")
        return max(candidates.values(), key=lambda m: m["metrics"].get("accuracy", 0))

class APIGateway:
    """Route and rate-limit inference requests."""
    def __init__(self, rate_limit_rps: int = 100):
        self.rate_limit = rate_limit_rps
        self._request_log: List[float] = []

    def check_rate_limit(self) -> bool:
        now = time.time()
        self._request_log = [t for t in self._request_log if now - t < 1.0]
        if len(self._request_log) >= self.rate_limit:
            return False
        self._request_log.append(now)
        return True

    def route(self, endpoint: str, payload: Dict) -> Dict:
        if not self.check_rate_limit():
            return {"error": "Rate limit exceeded", "status": 429}
        return {"status": 200, "endpoint": endpoint, "routed": True, "payload_size": len(str(payload))}

# Wire everything together
config = MLSystemConfig({
    "model_name": "churn-classifier",
    "api_version": "v2",
    "serving": {"host": "0.0.0.0", "port": 8000, "workers": 4},
    "monitoring": {"metrics_port": 9090, "log_level": "INFO"}
})

registry = ModelRegistry()
registry.register("churn-classifier", "1.0.0", {"accuracy": 0.89, "f1": 0.84})
registry.register("churn-classifier", "1.1.0", {"accuracy": 0.92, "f1": 0.88})
champion = registry.get_champion("churn-classifier")
print(f"Champion model: {champion['name']} v{champion['version']} (accuracy={champion['metrics']['accuracy']})")

gateway = APIGateway(rate_limit_rps=50)
for i in range(5):
    result = gateway.route("/predict", {"features": [0.5]*8})
    print(f"Request {i+1}: status={result['status']}")

assert champion["version"] == "1.1.0", "Champion should be highest accuracy version"
assert champion["metrics"]["accuracy"] >= 0.90
assert all(gateway.route("/predict", {}) ["status"] == 200 for _ in range(3))
print("✅ Week 17 ML System Capstone assertions passed")''',

    # Week 19-26 misc remaining tasks
    (20, 147): '''# Day 147: Vector Memory & Coreference Resolution for Agents
import numpy as np
from typing import List, Dict, Optional, Tuple
import hashlib, re

class ConversationMemory:
    """Vector-based conversational memory with coreference resolution."""

    def __init__(self, dim: int = 64, max_turns: int = 20):
        self.dim = dim
        self.turns: List[Dict] = []
        self.embeddings: List[np.ndarray] = []
        self.max_turns = max_turns

    def _embed(self, text: str) -> np.ndarray:
        """Deterministic mock embedding."""
        h = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**31)
        np.random.seed(h)
        v = np.random.randn(self.dim)
        return v / (np.linalg.norm(v) + 1e-9)

    def add_turn(self, role: str, content: str):
        self.turns.append({'role': role, 'content': content})
        self.embeddings.append(self._embed(content))
        if len(self.turns) > self.max_turns:
            self.turns.pop(0)
            self.embeddings.pop(0)

    def retrieve_relevant(self, query: str, top_k: int = 3) -> List[Dict]:
        if not self.embeddings:
            return []
        q_vec = self._embed(query)
        sims = [np.dot(q_vec, e) for e in self.embeddings]
        top_idx = np.argsort(sims)[::-1][:top_k]
        return [{'turn': self.turns[i], 'score': float(sims[i])} for i in top_idx]

    def resolve_coreference(self, current_text: str) -> str:
        """Simple pronoun resolution using last entity mention."""
        pronouns = re.compile(r'\b(it|this|that|they|them|their)\b', re.IGNORECASE)
        if not pronouns.search(current_text):
            return current_text

        # Find last entity (NOUN or proper noun heuristic)
        entity = None
        for turn in reversed(self.turns):
            nouns = re.findall(r'\b[A-Z][a-z]+\b|\b(transformer|model|system|agent)\b',
                               turn['content'], re.IGNORECASE)
            if nouns:
                entity = next((n for n in nouns if n), None)
                break

        if entity:
            resolved = pronouns.sub(entity, current_text)
            return resolved
        return current_text

# Test conversational memory
memory = ConversationMemory(dim=64)
memory.add_turn("user", "Explain how the Transformer model works")
memory.add_turn("assistant", "The Transformer uses self-attention to process sequences in parallel")
memory.add_turn("user", "How does it handle long sequences?")
memory.add_turn("assistant", "The Transformer uses positional encoding to maintain order")
memory.add_turn("user", "What is its computational complexity?")

relevant = memory.retrieve_relevant("attention mechanism", top_k=2)
print(f"Retrieved {len(relevant)} relevant turns")
for r in relevant:
    print(f"  [{r['score']:.4f}] {r['turn']['role']}: {r['turn']['content'][:60]}")

resolved = memory.resolve_coreference("How does it scale to production?")
print(f"Resolved: '{resolved}'")

assert len(relevant) == 2, "Should retrieve 2 turns"
assert all(0 <= r['score'] for r in relevant)
assert len(memory.turns) == 5
print("✅ Vector Memory & Coreference assertions passed")''',

    (20, 148): '''# Day 148: Human-in-the-Loop (HITL) — Annotation & Feedback Pipeline
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time, json

class ReviewStatus(Enum):
    PENDING   = "pending"
    APPROVED  = "approved"
    REJECTED  = "rejected"
    REVISED   = "revised"

@dataclass
class ReviewItem:
    item_id: str
    content: str
    model_output: str
    confidence: float
    status: ReviewStatus = ReviewStatus.PENDING
    reviewer_feedback: Optional[str] = None
    corrected_output: Optional[str] = None
    reviewed_at: Optional[float] = None

class HITLPipeline:
    """Human-in-the-Loop pipeline for model output review."""

    def __init__(self, confidence_threshold: float = 0.85):
        self.threshold = confidence_threshold
        self.queue: List[ReviewItem] = []
        self.approved: List[ReviewItem] = []
        self.rejected: List[ReviewItem] = []
        self.metrics: Dict[str, int] = {
            "auto_approved": 0, "sent_to_human": 0,
            "human_approved": 0, "human_rejected": 0
        }

    def submit(self, item_id: str, content: str, model_output: str, confidence: float) -> str:
        """Submit model output for review (auto-approve if confidence high)."""
        item = ReviewItem(item_id=item_id, content=content,
                          model_output=model_output, confidence=confidence)

        if confidence >= self.threshold:
            # Auto-approve high-confidence outputs
            item.status = ReviewStatus.APPROVED
            item.reviewed_at = time.time()
            self.approved.append(item)
            self.metrics["auto_approved"] += 1
            return "auto_approved"
        else:
            # Send to human review queue
            self.queue.append(item)
            self.metrics["sent_to_human"] += 1
            return "queued_for_review"

    def human_review(self, item_id: str, decision: str,
                     feedback: str = None, correction: str = None):
        """Simulate human reviewer action."""
        item = next((i for i in self.queue if i.item_id == item_id), None)
        if not item:
            raise ValueError(f"Item {item_id} not in review queue")

        item.reviewer_feedback = feedback
        item.reviewed_at = time.time()

        if decision == "approve":
            item.status = ReviewStatus.APPROVED
            self.approved.append(item)
            self.metrics["human_approved"] += 1
        elif decision == "reject":
            item.status = ReviewStatus.REJECTED
            item.corrected_output = correction
            self.rejected.append(item)
            self.metrics["human_rejected"] += 1

        self.queue.remove(item)

    def get_stats(self) -> Dict:
        total = sum(self.metrics.values())
        return {**self.metrics, "total": total,
                "queue_size": len(self.queue),
                "approval_rate": (self.metrics["auto_approved"] + self.metrics["human_approved"]) / max(total, 1)}

# Test the HITL pipeline
pipeline = HITLPipeline(confidence_threshold=0.85)

# Submit batch of model outputs
test_cases = [
    ("item_001", "Classify this email", "spam",    0.95),  # auto-approved
    ("item_002", "Translate: Hello",    "Hola",    0.78),  # human review
    ("item_003", "Summarize article",   "Summary", 0.91),  # auto-approved
    ("item_004", "Tag sentiment",       "neutral", 0.62),  # human review
]

for item_id, content, output, conf in test_cases:
    result = pipeline.submit(item_id, content, output, conf)
    print(f"  {item_id} (conf={conf}): {result}")

# Human reviews pending items
pipeline.human_review("item_002", "approve", feedback="Translation correct")
pipeline.human_review("item_004", "reject", feedback="Should be negative", correction="negative")

stats = pipeline.get_stats()
print(f"\nStats: {json.dumps(stats, indent=2)}")

assert stats["auto_approved"] == 2
assert stats["human_approved"] == 1
assert stats["human_rejected"] == 1
assert stats["queue_size"] == 0
assert stats["approval_rate"] >= 0.5
print("✅ HITL Pipeline assertions passed")''',

    (23, 166): '''# Day 166: Serverless ML with AWS Lambda + API Gateway (local simulation)
import json, numpy as np, time, hashlib
from typing import Any, Dict, Optional

class ServerlessMLModel:
    """Serverless-optimized ML model (cold-start aware)."""
    _instance: Optional['ServerlessMLModel'] = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        """Cold start: load model weights (once)."""
        if not self._initialized:
            time.sleep(0.01)  # simulate cold start latency
            np.random.seed(42)
            self.weights = np.random.randn(8)
            self.bias = 0.5
            self._initialized = True
            return True
        return False

    def predict(self, features: list) -> dict:
        cold_start = self.initialize()
        x = np.array(features)
        score = float(np.dot(self.weights[:len(x)], x) + self.bias)
        prob = 1 / (1 + np.exp(-score))
        return {"prediction": int(prob > 0.5), "probability": round(float(prob), 4),
                "cold_start": cold_start}

def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """AWS Lambda entry point."""
    try:
        body = event if isinstance(event, dict) else json.loads(event.get('body', '{}'))
        features = body.get('features')

        if not features or not isinstance(features, list) or len(features) == 0:
            return {'statusCode': 400, 'body': json.dumps({'error': 'features list required'})}

        model = ServerlessMLModel()
        result = model.predict(features)

        response_body = {
            'prediction': result['prediction'],
            'probability': result['probability'],
            'cold_start': result['cold_start'],
            'request_id': hashlib.md5(str(features).encode()).hexdigest()[:8]
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'X-Lambda-Version': '1.0'},
            'body': json.dumps(response_body)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

# Test invocations
events = [
    {'features': [0.5, 1.2, -0.3, 0.8, 0.1, -0.5, 0.9, 0.2]},
    {'features': [-1.0, -0.5, 0.3]},
    {'features': []},  # error case
]

for i, event in enumerate(events):
    resp = lambda_handler(event)
    body = json.loads(resp['body'])
    print(f"Request {i+1}: status={resp['statusCode']}, {list(body.keys())}")

r1 = lambda_handler({'features': [0.5, 1.2, -0.3]})
r2 = lambda_handler({'features': []})
assert r1['statusCode'] == 200
assert r2['statusCode'] == 400
body1 = json.loads(r1['body'])
assert 'prediction' in body1 and body1['prediction'] in [0, 1]
assert 'request_id' in body1
print("✅ Serverless ML Lambda assertions passed")''',

    (23, 169): '''# Day 169: Secrets Management — production vault (see Pass 1 for full impl)
# Re-implementing with enhanced features: rotation policies + audit log
import os, hmac, hashlib, base64, time, json
from typing import Optional, Dict, List

class SecretRotationPolicy:
    def __init__(self, rotation_days: int):
        self.rotation_days = rotation_days
        self.rotation_seconds = rotation_days * 86400

    def is_expired(self, created_at: float) -> bool:
        return (time.time() - created_at) > self.rotation_seconds

class AuditLog:
    def __init__(self):
        self._log: List[Dict] = []

    def record(self, action: str, key: str, actor: str = "system"):
        self._log.append({"action": action, "key": key, "actor": actor, "timestamp": time.time()})

    def get_events(self, key: str = None) -> List[Dict]:
        if key:
            return [e for e in self._log if e["key"] == key]
        return self._log.copy()

class ProductionSecretsVault:
    def __init__(self, master_key: str, rotation_days: int = 90):
        self._key = master_key.encode()
        self._store: Dict[str, Dict] = {}
        self._policy = SecretRotationPolicy(rotation_days)
        self._audit = AuditLog()

    def _encrypt(self, plaintext: str) -> str:
        encoded = base64.b64encode(plaintext.encode()).decode()
        tag = hmac.new(self._key, encoded.encode(), hashlib.sha256).hexdigest()[:8]
        return f"{tag}:{encoded}"

    def _decrypt(self, ciphertext: str) -> Optional[str]:
        parts = ciphertext.split(":", 1)
        if len(parts) != 2: return None
        tag, encoded = parts
        expected = hmac.new(self._key, encoded.encode(), hashlib.sha256).hexdigest()[:8]
        if not hmac.compare_digest(tag, expected): return None
        return base64.b64decode(encoded.encode()).decode()

    def put(self, key: str, value: str, actor: str = "system"):
        self._store[key] = {"ciphertext": self._encrypt(value), "created_at": time.time()}
        self._audit.record("PUT", key, actor)

    def get(self, key: str, actor: str = "system") -> Optional[str]:
        if key not in self._store: return None
        self._audit.record("GET", key, actor)
        meta = self._store[key]
        if self._policy.is_expired(meta["created_at"]):
            self._audit.record("ROTATION_REQUIRED", key, "system")
        return self._decrypt(meta["ciphertext"])

    def rotate(self, key: str, new_value: str, actor: str = "system") -> bool:
        if key not in self._store: return False
        self.put(key, new_value, actor)
        self._audit.record("ROTATE", key, actor)
        return True

    def delete(self, key: str, actor: str = "system") -> bool:
        if key not in self._store: return False
        del self._store[key]
        self._audit.record("DELETE", key, actor)
        return True

    def audit_report(self, key: str = None) -> List[Dict]:
        return self._audit.get_events(key)

# Test
vault = ProductionSecretsVault(master_key="production-master-key-2024", rotation_days=90)
vault.put("DB_PASSWORD", "super-secure-pass-2024", actor="admin")
vault.put("API_KEY", "sk-prod-abc123", actor="devops")

assert vault.get("DB_PASSWORD") == "super-secure-pass-2024"
assert vault.get("API_KEY") == "sk-prod-abc123"
assert vault.get("MISSING") is None

vault.rotate("DB_PASSWORD", "new-secure-pass-2025", actor="admin")
assert vault.get("DB_PASSWORD") == "new-secure-pass-2025"

vault.delete("API_KEY", actor="admin")
assert vault.get("API_KEY") is None

audit = vault.audit_report("DB_PASSWORD")
actions = [e["action"] for e in audit]
assert "PUT" in actions and "ROTATE" in actions
print(f"Audit log for DB_PASSWORD: {actions}")
print("✅ Production Secrets Vault assertions passed")''',

    (24, 174): '''# Day 174: ML Workflow Orchestration with Apache Airflow (local simulation)
from datetime import datetime, timedelta
from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass, field
import json, time

@dataclass
class TaskInstance:
    task_id: str
    dag_id: str
    state: str = "pending"  # pending, running, success, failed
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    output: Any = None
    error: Optional[str] = None

    def duration_s(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return round(self.end_time - self.start_time, 3)
        return None

class AirflowDAG:
    """Simplified Airflow DAG simulation."""

    def __init__(self, dag_id: str, schedule: str = "@daily",
                 catchup: bool = False, max_active_runs: int = 1):
        self.dag_id = dag_id
        self.schedule = schedule
        self.tasks: Dict[str, Callable] = {}
        self.dependencies: Dict[str, List[str]] = {}  # task -> upstream tasks
        self.instances: List[TaskInstance] = []

    def task(self, task_id: str, upstream: List[str] = None):
        """Decorator to register a DAG task."""
        def decorator(fn: Callable):
            self.tasks[task_id] = fn
            self.dependencies[task_id] = upstream or []
            return fn
        return decorator

    def run(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute DAG tasks in dependency order (topological sort)."""
        context = context or {"execution_date": datetime.now().isoformat()}
        # Build execution order (simple topo sort)
        visited, order = set(), []
        def visit(task_id):
            if task_id in visited: return
            visited.add(task_id)
            for dep in self.dependencies.get(task_id, []):
                visit(dep)
            order.append(task_id)
        for t in self.tasks:
            visit(t)

        task_outputs = {}
        for task_id in order:
            instance = TaskInstance(task_id=task_id, dag_id=self.dag_id)
            instance.state = "running"
            instance.start_time = time.time()
            try:
                output = self.tasks[task_id](context=context, upstream_outputs=task_outputs)
                instance.output = output
                instance.state = "success"
                task_outputs[task_id] = output
            except Exception as e:
                instance.state = "failed"
                instance.error = str(e)
                task_outputs[task_id] = None
            instance.end_time = time.time()
            self.instances.append(instance)

        return task_outputs

# Build a data pipeline DAG
dag = AirflowDAG("ml_training_pipeline", schedule="@weekly")

@dag.task("extract_data")
def extract_data(context, upstream_outputs):
    return {"records": 10000, "source": "s3://ml-data/training/"}

@dag.task("preprocess", upstream=["extract_data"])
def preprocess(context, upstream_outputs):
    records = upstream_outputs["extract_data"]["records"]
    return {"processed": records, "features": 12, "split": "80/20"}

@dag.task("train_model", upstream=["preprocess"])
def train_model(context, upstream_outputs):
    info = upstream_outputs["preprocess"]
    return {"model_path": "s3://models/v1/clf.pkl", "accuracy": 0.924, "f1": 0.891}

@dag.task("evaluate", upstream=["train_model"])
def evaluate(context, upstream_outputs):
    metrics = upstream_outputs["train_model"]
    assert metrics["accuracy"] > 0.8, "Model quality gate: accuracy must > 80%"
    return {"status": "PASSED", "metrics": metrics}

@dag.task("register_model", upstream=["evaluate"])
def register_model(context, upstream_outputs):
    return {"registered": True, "version": "v1.0", "alias": "champion"}

outputs = dag.run()
print("DAG execution results:")
for task_id, output in outputs.items():
    print(f"  {task_id}: {output}")

assert outputs["extract_data"]["records"] == 10000
assert outputs["train_model"]["accuracy"] > 0.8
assert outputs["evaluate"]["status"] == "PASSED"
assert outputs["register_model"]["registered"] is True
failed = [i for i in dag.instances if i.state == "failed"]
assert len(failed) == 0, f"Tasks failed: {[i.task_id for i in failed]}"
print("✅ Airflow DAG Orchestration assertions passed")''',

    (24, 175): '''# Day 175: Model & Data Drift Monitoring with Evidently/Prometheus
import numpy as np
from typing import Dict, List, Any
from scipy import stats

class StatisticalDriftDetector:
    """Detects feature and prediction drift using statistical tests."""

    def __init__(self, reference_data: np.ndarray, feature_names: List[str] = None):
        self.reference = reference_data
        self.features = feature_names or [f"feat_{i}" for i in range(reference_data.shape[1])]

    def ks_drift(self, production_data: np.ndarray, threshold: float = 0.05) -> Dict[str, Dict]:
        """Kolmogorov-Smirnov test for distribution drift per feature."""
        results = {}
        for i, feat in enumerate(self.features):
            ref_col  = self.reference[:, i]
            prod_col = production_data[:, i]
            ks_stat, p_value = stats.ks_2samp(ref_col, prod_col)
            results[feat] = {
                "ks_statistic": round(ks_stat, 4),
                "p_value":      round(p_value, 4),
                "drift_detected": p_value < threshold,
                "severity": "HIGH" if p_value < 0.01 else ("MEDIUM" if p_value < threshold else "OK")
            }
        return results

    def psi_drift(self, production_data: np.ndarray, n_bins: int = 10) -> Dict[str, float]:
        """Population Stability Index (PSI) for categorical/discretized drift."""
        psi_scores = {}
        for i, feat in enumerate(self.features):
            ref_col  = self.reference[:, i]
            prod_col = production_data[:, i]
            bins = np.linspace(min(ref_col.min(), prod_col.min()),
                               max(ref_col.max(), prod_col.max()), n_bins + 1)
            ref_hist,  _ = np.histogram(ref_col, bins=bins, density=True)
            prod_hist, _ = np.histogram(prod_col, bins=bins, density=True)
            ref_hist  = np.clip(ref_hist, 1e-6, None)
            prod_hist = np.clip(prod_hist, 1e-6, None)
            psi = np.sum((prod_hist - ref_hist) * np.log(prod_hist / ref_hist)) * (bins[1] - bins[0])
            psi_scores[feat] = round(float(psi), 4)
        return psi_scores

# Generate reference (training) and drifted (production) data
np.random.seed(42)
n_ref, n_prod, n_feats = 1000, 500, 4
reference = np.random.randn(n_ref, n_feats)
feature_names = ["cpu_util", "request_rate", "latency_ms", "token_count"]

# Simulate drift: features 0 and 2 shift in production
production_ok     = np.random.randn(n_prod, n_feats)       # no drift
production_drifted = np.column_stack([
    np.random.randn(n_prod) + 1.5,   # DRIFTED (shift +1.5)
    np.random.randn(n_prod),          # OK
    np.random.randn(n_prod) * 2.0,   # DRIFTED (scale x2)
    np.random.randn(n_prod),          # OK
])

detector = StatisticalDriftDetector(reference, feature_names)

ks_ok = detector.ks_drift(production_ok)
ks_dr = detector.ks_drift(production_drifted)
psi   = detector.psi_drift(production_drifted)

print("KS Drift (no drift expected):")
for feat, result in ks_ok.items():
    print(f"  {feat}: p={result['p_value']}, drift={result['drift_detected']}")

print("\nKS Drift (drift expected):")
for feat, result in ks_dr.items():
    print(f"  {feat}: p={result['p_value']}, {result['severity']}")

print(f"\nPSI scores: {psi}")

# Assertions
drifted_feats = [f for f, r in ks_dr.items() if r["drift_detected"]]
assert "cpu_util" in drifted_feats, "cpu_util drift should be detected"
assert "latency_ms" in drifted_feats, "latency_ms drift should be detected"
no_drift = [f for f, r in ks_ok.items() if not r["drift_detected"]]
assert len(no_drift) >= 2, "Most features should not drift in clean data"
print("✅ Drift Detection assertions passed")''',

    (24, 176): '''# Day 176: Canary Deployments & Statistical A/B Testing
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple

class CanaryDeployment:
    """Manages gradual traffic shifting for canary deployments."""

    def __init__(self, current_version: str, canary_version: str,
                 initial_canary_pct: float = 5.0):
        self.current = current_version
        self.canary  = canary_version
        self.canary_pct = initial_canary_pct
        self.metrics: Dict[str, List[float]] = {current_version: [], canary_version: []}
        self.stage_log: List[Dict] = []

    def route_request(self) -> str:
        """Route request to canary or current based on traffic split."""
        return self.canary if np.random.random() < self.canary_pct / 100 else self.current

    def record_metric(self, version: str, value: float):
        """Record latency or success rate for a version."""
        self.metrics[version].append(value)

    def analyze(self) -> Dict:
        """Run Mann-Whitney U test to compare version performance."""
        curr_m = self.metrics[self.current]
        can_m  = self.metrics[self.canary]

        if len(curr_m) < 10 or len(can_m) < 10:
            return {"status": "insufficient_data", "sample_sizes": (len(curr_m), len(can_m))}

        stat, p_value = stats.mannwhitneyu(curr_m, can_m, alternative='two-sided')
        current_mean = np.mean(curr_m)
        canary_mean  = np.mean(can_m)
        improvement  = (current_mean - canary_mean) / current_mean * 100  # lower = better for latency

        return {
            "status": "analyzed",
            "sample_sizes": (len(curr_m), len(can_m)),
            "current_mean": round(current_mean, 4),
            "canary_mean":  round(canary_mean, 4),
            "improvement_pct": round(improvement, 2),
            "p_value":      round(p_value, 4),
            "significant":  p_value < 0.05,
            "canary_traffic_pct": self.canary_pct,
            "recommendation": "PROMOTE" if p_value < 0.05 and improvement > 0 else "HOLD"
        }

    def promote(self, new_pct: float):
        """Increase canary traffic percentage."""
        old = self.canary_pct
        self.canary_pct = min(100.0, new_pct)
        self.stage_log.append({"from": old, "to": self.canary_pct})
        return self.canary_pct

# Simulate canary deployment
np.random.seed(42)
deployment = CanaryDeployment("v1.0", "v1.1-canary", initial_canary_pct=10.0)

# Simulate traffic: v1.0 avg 150ms, v1.1 avg 120ms (20% improvement)
for _ in range(500):
    version = deployment.route_request()
    latency = np.random.normal(150, 20) if version == "v1.0" else np.random.normal(120, 18)
    deployment.record_metric(version, latency)

analysis = deployment.analyze()
print(f"Canary Analysis: {analysis}")

# Progressive rollout
for stage_pct in [25, 50, 75, 100]:
    deployment.promote(stage_pct)
    print(f"Traffic shifted to: {stage_pct}% canary")

assert analysis["status"] == "analyzed"
assert analysis["significant"], "Traffic improvement should be statistically significant"
assert analysis["improvement_pct"] > 0, "Canary should show improvement"
assert analysis["recommendation"] == "PROMOTE", "Canary should be promoted"
assert len(deployment.stage_log) == 4
print("✅ Canary Deployment & A/B Testing assertions passed")''',
}

# ─────────────────────────────────────────────────────────────────────────────
# Apply fixes
# ─────────────────────────────────────────────────────────────────────────────

def apply_pass2_fixes(week_n: int) -> bool:
    fpath = os.path.join(DATA_DIR, f"week{week_n:02d}.yaml")
    if not os.path.exists(fpath):
        return False

    data = load_yaml(fpath)
    changed = False

    # Backup
    shutil.copy2(fpath, os.path.join(BACKUP_DIR, f"week{week_n:02d}.yaml"))

    for day in data.get('days', []):
        day_id_raw = day.get('id')
        try:
            day_id_int = int(day_id_raw)
        except (TypeError, ValueError):
            day_id_int = None

        for ti, task in enumerate(day.get('tasks', []), 1):
            # K7: Fix week 3 tb-proj (missed in pass 1)
            if week_n == 3 and task.get('badge_class') == 'tb-proj':
                task['badge_class'] = 'tb-hard'
                print(f"  [K7] W3D{day_id_raw} task[{ti}]: tb-proj → tb-hard")
                changed = True

            # U9/K3: Replace skeleton solutions and RF boilerplate
            sol = task.get('solution_code', '') or ''
            has_todo_skeleton = ('# TODO: Replace this skeleton' in sol or
                                 '# TODO: Implement validation logic' in sol)
            has_rf_boilerplate = ('make_classification(n_samples=500, n_features=10, n_informative=8' in sol)

            if (has_todo_skeleton or has_rf_boilerplate) and day_id_int is not None:
                key = (week_n, day_id_int)
                if key in REAL_SOLUTIONS:
                    task['solution_code'] = REAL_SOLUTIONS[key]
                    why = 'skeleton' if has_todo_skeleton else 'RF boilerplate'
                    print(f"  [FIX] W{week_n}D{day_id_raw} task[{ti}]: replaced {why} with real solution")
                    changed = True

    if changed:
        save_yaml(fpath, data)
        print(f"  ✓ Saved week{week_n:02d}.yaml")
    return changed

# Run pass 2
print("🔧 Phase 3 Pass 2 — fixing K7(week3), skeleton solutions, RF boilerplate")
print("="*60)

for wn in range(1, 27):
    apply_pass2_fixes(wn)

print("\n✅ Pass 2 complete. Run phase1_audit.py to verify.")
