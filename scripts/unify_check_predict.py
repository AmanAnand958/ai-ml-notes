#!/usr/bin/env python3
"""
Step 1: Write unified, hardened checkPredict function in assets/js/course.js supporting:
1. checkPredict(id, answer)
2. checkPredict(btn, expected)
With full multi-line token normalization and XP awards.
"""

from pathlib import Path

fp_js = Path("assets/js/course.js")
js = fp_js.read_text(encoding='utf-8')

idx_start = js.find("function checkPredict(btn, expected) {")
idx_end = js.find("function triggerConfetti() {", idx_start)

if idx_start != -1 and idx_end != -1:
    new_func = """function checkPredict(arg1, arg2) {
  let input = null;
  let result = null;
  let answer = arg2;

  if (typeof arg1 === 'string') {
    input = document.getElementById(arg1 + '-input') || document.getElementById(arg1);
    result = document.getElementById(arg1 + '-result') || document.getElementById(arg1 + '-feedback') || document.getElementById(arg1);
  } else if (arg1 && arg1.nodeType) {
    const parent = arg1.closest('.predict-box') || arg1.closest('.predict-block') || arg1.closest('.task-block') || arg1.parentElement;
    input = parent ? parent.querySelector('input') : null;
    result = parent ? (parent.querySelector('.predict-result') || parent.querySelector('.predict-feedback') || parent.querySelector('.result')) : null;
  }

  if (!input || !result) return;
  if (result.dataset && result.dataset.solved === 'true') return;

  const normalize = (str) => {
    return String(str || '')
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
  const rawUser = input.value.trim().toLowerCase();
  const rawExp = String(answer || '').trim().toLowerCase();

  const isCorrect = (userVal === correctVal) || (rawUser === rawExp) || (correctVal.length > 0 && userVal.includes(correctVal));

  result.style.display = 'block';
  if (isCorrect) {
    if (result.dataset) result.dataset.solved = 'true';
    input.disabled = true;
    result.style.background = 'rgba(79,209,165,.1)';
    result.style.border = '1px solid rgba(79,209,165,.3)';
    result.style.color = 'var(--green, #4fd1a5)';
    result.style.borderRadius = '6px';
    result.style.padding = '.5rem .8rem';
    result.textContent = '✅ Correct! ' + String(answer).replace(/\\n/g, ' ');

    if (typeof courseState !== 'undefined') {
      courseState.awardXP(10, 'prediction');
    } else if (typeof state !== 'undefined') {
      state.xp = (state.xp || 0) + 10;
      if (typeof saveState === 'function') saveState();
      if (typeof syncUI === 'function') syncUI();
      if (typeof showXPToast === 'function') showXPToast(10, 'prediction');
    }
  } else {
    result.style.background = 'rgba(229,107,140,.08)';
    result.style.border = '1px solid rgba(229,107,140,.3)';
    result.style.color = 'var(--pink, #e56b8c)';
    result.style.borderRadius = '6px';
    result.style.padding = '.5rem .8rem';
    result.textContent = '❌ Expected: ' + String(answer).replace(/\\n/g, ' ') + ' — try again';
  }
}

"""
    js = js[:idx_start] + new_func + js[idx_end:]
    fp_js.write_text(js, encoding='utf-8')
    print("✅ Successfully unified checkPredict in assets/js/course.js!")
else:
    print(f"Indices: s={idx_start}, e={idx_end}")
