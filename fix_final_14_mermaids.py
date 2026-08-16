from bs4 import BeautifulSoup

# Fix Week 4 #1, #2, #6
with open("pages/weeks/week4.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
nodes = soup.find_all(class_="mermaid")

# #1
nodes[1].string = """graph LR
  P["Probability P(A)"] --> Value["Range: 0 to 1"]
  P --> Cond["Conditional: P(A|B) = P(A ∩ B) / P(B)"]
  P --> Ind["Independent: P(A ∩ B) = P(A) × P(B)"]
  P --> Dep["Dependent: P(A ∩ B) = P(A) × P(B|A)"]"""

# #2
nodes[2].string = """graph TD
  Prior["Prior: P(A) - Initial belief"] --> Posterior["Posterior: P(A|B) - Updated belief"]
  Likelihood["Likelihood: P(B|A) - Evidence probability"] --> Posterior
  Normalizer["Normalizer: P(B) - Total probability"] --> Posterior"""

# #6
nodes[6].string = """graph TD
  Info["Information Metrics"] --> Ent["Entropy H(X): Average uncertainty/surprise"]
  Info --> CE["Cross-Entropy H(P, Q): Surprise using model distribution Q"]
  Info --> KL["KL Divergence D_KL(P||Q): Extra bits wasted"]
  Ent --> Formula1["Formula: -Σ P(x) log P(x)"]
  CE --> Formula2["Formula: -Σ P(x) log Q(x)"]
  KL --> Formula3["Formula: H(P, Q) - H(P)"]"""

with open("pages/weeks/week4.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Fixed week4.html diagrams")

# Fix Week 8 #2, #3, #4, #5, #6
with open("pages/weeks/week8.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
nodes = soup.find_all(class_="mermaid")

fixed_week8 = """graph LR
  X["Input X"] -->|Forward Pass: z = w*x + b| Linear["Linear Neuron: z"]
  Linear -->|Forward Pass: a = sigma(z)| Activation["Activation: sigma(z)"]
  Activation -->|Forward Pass: L = Loss(a,y)| Loss["Loss Node: L"]
  Loss -->|Backward Pass: dL/da| Activation
  Activation -->|Backward Pass: dL/dz = dL/da * sigma_prime(z)| Linear
  Linear -->|Backward Pass: dL/dw = dL/dz * x| Weights["Gradient dL/dw"]"""

for i in [2, 3, 4, 5, 6]:
    if i < len(nodes):
        nodes[i].string = fixed_week8

with open("pages/weeks/week8.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Fixed week8.html diagrams")

# Fix Week 10 #1, #2, #3, #4
with open("pages/weeks/week10.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
nodes = soup.find_all(class_="mermaid")

fixed_week10 = """graph LR
  CellPrev["Cell State C_{t-1}"] -->|x Forget Gate f_t| CellCurr["Cell State C_t"]
  Input["Input x_t & Hidden h_{t-1}"] --> ForgetGate["Forget Gate: sigma(W_f)"]
  Input --> InputGate["Input Gate: sigma(W_i) * tanh(W_c)"]
  InputGate -->|+ Add to Cell State| CellCurr
  CellCurr -->|tanh * Output Gate sigma(W_o)| HiddenCurr["Hidden State h_t"]"""

for i in [1, 2, 3, 4]:
    if i < len(nodes):
        nodes[i].string = fixed_week10

with open("pages/weeks/week10.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Fixed week10.html diagrams")

# Fix Week 23 #5
with open("pages/weeks/week23.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
nodes = soup.find_all(class_="mermaid")
if len(nodes) > 5:
    nodes[5].string = """graph LR
  User["User Request"] --> Bandit["Thompson Sampling Bandit Router"]
  Bandit -->|Sample theta ~ Beta(a,b)| ModelA["Model Candidate A: 85% Traffic"]
  Bandit -->|Sample theta ~ Beta(a,b)| ModelB["Model Candidate B: 15% Traffic"]
  ModelA -->|Reward Click/Conversion| Bandit"""
with open("pages/weeks/week23.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Fixed week23.html diagrams")

# Fix Week 24 #5
with open("pages/weeks/week24.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
nodes = soup.find_all(class_="mermaid")
if len(nodes) > 5:
    nodes[5].string = """graph LR
subgraph Canary_Traffic_Routing ["Canary Traffic Routing"]
  UserInference["User Inferences"] --> Ingress["Ingress Gateway Router"]
  Ingress -->|90% Traffic| V1["Model v1: champion (Stable)"]
  Ingress -->|10% Traffic| V2["Model v2: challenger (Canary)"]
  V1 --> Monitor["Prometheus Metric Collector"]
  V2 --> Monitor
  Monitor -->|Error Rate > 2%| Rollback["Instant Automated Rollback to 100% v1"]
end"""
with open("pages/weeks/week24.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
print("Fixed week24.html diagrams")
