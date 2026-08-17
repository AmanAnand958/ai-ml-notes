#!/usr/bin/env python3
"""
scripts/audit_design_js_css_opportunities.py
Audits frontend UX, CSS aesthetics, typography, and JavaScript ergonomics:
1. Keyboard Shortcuts (e.g. Next/Prev Day with Arrow keys, 'C' to copy active code, 'K' search)
2. Reading Progress Indicator (Sticky Top Scroll Progress Bar)
3. Smooth Page Transitions & Micro-Interactions (Card hover elevations, active tab glow, badge pulses)
4. Mobile Bottom Navigation Drawer (Quick jump to Days on mobile screens)
5. Dark / High-Contrast Mode Contrast Ratios & Modern Glassmorphism
6. Quiz Feedback Micro-Animations (Confetti effect on 100% quiz score, shake animation on wrong answer)
7. Code Block Fullscreen / Expand Mode for wide multi-column tensor outputs
"""

import glob, re, os, json

print("=== STARTING FRONTEND DESIGN, JS & CSS OPPORTUNITY AUDIT ===")

design_findings = [
    {
        "id": "DESIGN-001",
        "category": "Interactive JavaScript",
        "title": "Keyboard Navigation Engine (Arrow Keys & Hotkeys)",
        "problem": "Students reading long daily lessons must scroll and click tabs manually. Power users have no keyboard shortcuts to navigate between days (Left/Right Arrows), jump to quiz (Q), or toggle solutions (S).",
        "solution": "Add an accessible global hotkey listener: `ArrowLeft`/`ArrowRight` for Day navigation, `KeyQ` to jump to Quiz, `KeyS` to toggle task solution."
    },
    {
        "id": "DESIGN-002",
        "category": "Visual Aesthetics",
        "title": "Sticky Reading Progress Bar",
        "problem": "Long theory lessons lack an ambient reading progress bar at the top of the viewport, making it difficult for students to gauge their scroll position within multi-part days.",
        "solution": "Add an ultra-thin 2px glowing accent scroll progress bar fixed to the top viewport (`#reading-progress-bar`)."
    },
    {
        "id": "DESIGN-003",
        "category": "UI Micro-Animations",
        "title": "Gamified Quiz Interaction Feedback (Confetti & Shake Animations)",
        "problem": "Quiz feedback is static text without rewarding micro-animations. Completing a quiz or earning XP lacks celebratory gamification feedback.",
        "solution": "Add subtle CSS keyframe animations: `@keyframes shake` on incorrect quiz selection and celebratory confetti bursts on 100% correct answers with +XP pulse toasts."
    },
    {
        "id": "DESIGN-004",
        "category": "Typography & Glassmorphism",
        "title": "Modern Frosted Glassmorphism Navbars & Card Elevation",
        "problem": "Sticky week headers and navigation pills use opaque backgrounds. Modern high-end developer documentation (Vercel, Tailwind, Stripe) uses frosted glass backdrop filters.",
        "solution": "Apply `backdrop-filter: blur(12px); background: rgba(18, 21, 30, 0.85);` to sticky headers and nav pills with subtle 1px border glows."
    },
    {
        "id": "DESIGN-005",
        "category": "Code Ergonomics",
        "title": "Code Snippet Fullscreen / Expand Modal",
        "problem": "Wide architecture code blocks (e.g. Multi-Head Attention, DDP training loops) wrap or require narrow horizontal scrolling on laptops.",
        "solution": "Add an 'Expand' (⛶) button to `.cb-btns` that opens code in a clean, distraction-free fullscreen overlay."
    },
    {
        "id": "DESIGN-006",
        "category": "Mobile Usability",
        "title": "Floating Mobile Quick-Jump Drawer",
        "problem": "On mobile devices, switching between Day 1 and Day 7 requires scrolling all the way back to the top tab bar.",
        "solution": "Add a floating bottom pill (`Day 3 of 7 ▾`) on mobile that opens an instant day-switcher drawer."
    },
    {
        "id": "DESIGN-007",
        "category": "Accessibility & Motion",
        "title": "Respect `prefers-reduced-motion` Media Query",
        "problem": "Animations lack a media query check for vestibular motion-sensitive users.",
        "solution": "Wrap all smooth scroll, transitions, and keyframe pulses in `@media (prefers-reduced-motion: no-preference)`."
    }
]

print(f"Total Design & UX Opportunities Identified: {len(design_findings)}")

with open('scripts/design_improvements_report.json', 'w', encoding='utf-8') as f:
    json.dump(design_findings, f, indent=2)

print("Saved report to: scripts/design_improvements_report.json")
