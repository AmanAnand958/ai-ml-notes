#!/usr/bin/env python3
"""
Step 1: Fix Predict Normalization in course.js & HTML:
Handles multi-line outputs seamlessly so that newlines and spaces match without friction.
"""

from pathlib import Path

fp_js = Path("assets/js/course.js")
js = fp_js.read_text(encoding='utf-8')

start_marker = "function checkPredict(id, answer) {"
end_marker = "function openRepl() {"

idx_start = js.find(start_marker)
idx_end = js.find(end_marker)

if idx_start != -1 and idx_end != -1:
    new_func = """function checkPredict(id, answer) {
  const input = document.getElementById(id + '-input');
  const result = document.getElementById(id + '-result');
  if (!input || !result) return;
  if (result.dataset.solved === 'true') return;
  
  const normalize = (str) => {
    return String(str)
      .replace(/\\\\n/g, ' ')
      .replace(/\\n/g, ' ')
      .replace(/['"()\\[\\]]/g, '')
      .replace(/[,;]/g, ' ')
      .replace(/\\s+/g, ' ')
      .trim()
      .toLowerCase();
  };
  
  const userVal = normalize(input.value);
  const correctVal = normalize(answer);

  // Exact comparison after token normalization or raw trimmed match
  let isCorrect = (userVal === correctVal) || (input.value.trim().toLowerCase() === String(answer).trim().toLowerCase());
  
  result.style.display = 'block';
  if (isCorrect) {
    result.dataset.solved = 'true';
    input.disabled = true;
    result.style.background = 'rgba(79,209,165,.1)';
    result.style.border = '1px solid rgba(79,209,165,.3)';
    result.style.color = 'var(--green)';
    result.style.borderRadius = '6px';
    result.style.padding = '.5rem .8rem';
    result.textContent = '✅ Correct! ' + answer.replace(/\\n/g, ' ');
    if (typeof state !== 'undefined') {
      state.xp = (state.xp || 0) + 10;
      if (typeof saveState === 'function') saveState();
      if (typeof syncUI === 'function') syncUI();
    }
    if (typeof showXPToast === 'function') showXPToast(10, 'prediction');
  } else {
    result.style.background = 'rgba(229,107,140,.08)';
    result.style.border = '1px solid rgba(229,107,140,.3)';
    result.style.color = 'var(--pink)';
    result.style.borderRadius = '6px';
    result.style.padding = '.5rem .8rem';
    result.textContent = '❌ Expected: ' + answer.replace(/\\n/g, ' ') + ' — try again';
  }
}

"""
    js = js[:idx_start] + new_func + js[idx_end:]
    fp_js.write_text(js, encoding='utf-8')
    print("✅ 1. Successfully upgraded checkPredict in assets/js/course.js!")
else:
    print("⚠️ Could not locate marker in course.js")
