#!/usr/bin/env python3
"""
Fix the final 5 brief flashcards.
"""

import glob
import yaml

def fix_5():
    files = sorted(glob.glob('src/data/week*.yaml'))
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as fp:
            data = yaml.safe_load(fp)
            
        for d in data.get('days', []):
            did = str(d.get('id', ''))
            
            for fc in d.get('flashcards', []):
                front = str(fc.get('front', ''))
                back = str(fc.get('back', ''))
                
                if did == '66' and 'tanh' in back:
                    fc['back'] = 'h_t = \\tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_{h}), preserving historical temporal sequence state.'
                elif did == '136' and 'formula for rrf' in front.lower():
                    fc['back'] = 'RRF Score = \\sum_{m \\in M} \\frac{1}{k + r_m(d)}, with standard constant k=60 to balance dense and sparse rank distributions.'
                elif did == '141' and 'hyde' in front.lower():
                    fc['back'] = 'Hypothetical Document Embeddings: Generates a synthetic pseudo-answer first, then embeds it to retrieve real documents in semantic space.'
                elif did == '162' and 'fp16 size' in front.lower():
                    fc['back'] = '16-bit Floating Point: Exactly 2 bytes per parameter (e.g. 70B parameter model requires 140GB VRAM strictly for weights).'
                elif did == '191' and 'title' in front.lower():
                    fc['back'] = 'Senior Full-Stack AI & Machine Learning Systems Engineer capable of designing, fine-tuning, and serving production GenAI architectures.'

        with open(fpath, 'w', encoding='utf-8') as fp:
            yaml.dump(data, fp, allow_unicode=True, sort_keys=False)

    print("✅ Successfully updated the final 5 flashcards!")

if __name__ == '__main__':
    fix_5()
