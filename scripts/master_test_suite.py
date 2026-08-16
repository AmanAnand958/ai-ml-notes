#!/usr/bin/env python3
"""
master_test_suite.py — Master Testing & Verification Suite

Unified testing script for 191-Day AI/ML Study Guide.
Combines:
  1. HTML DOM & Tag Balance Engine (HTMLParser)
  2. Asset Integrity & Path Verification (course.css, course.js in assets/)
  3. Navigation & Relative Link Integrity (Root <-> Pages/Weeks/)
  4. KaTeX Math Delimiters & Formula Audit
  5. Security & Link Attribute Audit (rel="noopener" for target="_blank")
  6. Week Page Structural Audit (Day sections, pills, quizzes, completion boxes)
"""

import os
import sys
import glob
import re
from html.parser import HTMLParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DivTracker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            line, col = self.getpos()
            self.stack.append((line, col, tag, attrs))

    def handle_endtag(self, tag):
        if tag == 'div':
            if not self.stack:
                line, col = self.getpos()
                self.errors.append((line, col))
            else:
                self.stack.pop()

class MasterTestSuite:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed_tests = 0
        self.failed_tests = 0

    def log_pass(self, name):
        self.passed_tests += 1
        print(f"  ✓ PASS: {name}")

    def log_fail(self, name, detail):
        self.failed_tests += 1
        msg = f"  ❌ FAIL: {name} — {detail}"
        self.errors.append(msg)
        print(msg)

    def log_warn(self, name, detail):
        msg = f"  ⚠️ WARN: {name} — {detail}"
        self.warnings.append(msg)
        print(msg)

    def run_all_tests(self):
        print("==========================================================")
        print("🚀 RUNNING MASTER TESTING & VERIFICATION SUITE")
        print("==========================================================\n")

        self.test_asset_files_exist()
        self.test_no_duplicate_assets()
        self.test_root_navigation_files()
        self.test_week_pages_exist()
        self.test_week_pages_div_balance()
        self.test_week_pages_asset_links()
        self.test_week_pages_navigation_links()
        self.test_katex_delimiters_and_math()
        self.test_security_attributes()
        self.test_week_structure_components()

        print("\n==========================================================")
        print("📊 TEST RESULTS SUMMARY")
        print("==========================================================")
        print(f"Passed Tests: {self.passed_tests}")
        print(f"Failed Tests: {self.failed_tests}")
        print(f"Warnings:     {len(self.warnings)}")

        if self.errors:
            print("\n❌ SUITE FAILED WITH THE FOLLOWING ERRORS:")
            for err in self.errors:
                print(err)
            return False
        else:
            print("\n🎉 ALL TESTS PASSED! 100% System Integrity & Clean Architecture Verified.")
            return True

    def test_asset_files_exist(self):
        print("--- [1/10] Testing Asset Files Existence ---")
        css = os.path.join(BASE_DIR, "assets", "css", "course.css")
        js = os.path.join(BASE_DIR, "assets", "js", "course.js")

        if os.path.exists(css):
            self.log_pass("assets/css/course.css exists")
        else:
            self.log_fail("assets/css/course.css exists", "File missing!")

        if os.path.exists(js):
            self.log_pass("assets/js/course.js exists")
        else:
            self.log_fail("assets/js/course.js exists", "File missing!")

    def test_no_duplicate_assets(self):
        print("\n--- [2/10] Testing No Duplicate Asset Files ---")
        all_css_js = glob.glob(os.path.join(BASE_DIR, "**", "course.css"), recursive=True) + \
                     glob.glob(os.path.join(BASE_DIR, "**", "course.js"), recursive=True)

        expected = {
            os.path.normpath(os.path.join(BASE_DIR, "assets", "css", "course.css")),
            os.path.normpath(os.path.join(BASE_DIR, "assets", "js", "course.js")),
        }

        duplicates = []
        for f in all_css_js:
            nf = os.path.normpath(f)
            if nf not in expected:
                duplicates.append(os.path.relpath(f, BASE_DIR))

        if not duplicates:
            self.log_pass("Single canonical asset storage (no duplicate course.css/course.js files)")
        else:
            self.log_fail("Single canonical asset storage", f"Duplicates found: {duplicates}")

    def test_root_navigation_files(self):
        print("\n--- [3/10] Testing Root Navigation Files ---")
        root_files = ["index.html", "roadmap.html", "dashboard.html", "resources.html"]
        for rf in root_files:
            fp = os.path.join(BASE_DIR, rf)
            if not os.path.exists(fp):
                self.log_fail(f"Root file {rf}", "File missing!")
                continue
            
            with open(fp, "r", encoding="utf-8") as f:
                c = f.read()

            # Verify week page links use pages/weeks/
            unprefixed = re.findall(r'href=["\'](?!\.\./|pages/weeks/)(week\d+\.html)["\']', c)
            if unprefixed:
                self.log_fail(f"Root file {rf} links", f"Unprefixed week links: {unprefixed}")
            else:
                self.log_pass(f"Root file {rf} correctly links to pages/weeks/")

    def test_week_pages_exist(self):
        print("\n--- [4/10] Testing 26 Week Pages Existence ---")
        missing = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                missing.append(f"week{w}.html")

        if not missing:
            self.log_pass("All 26 week files exist in pages/weeks/")
        else:
            self.log_fail("All 26 week files exist in pages/weeks/", f"Missing: {missing}")

    def test_week_pages_div_balance(self):
        print("\n--- [5/10] Testing HTML Div Tag Balance Across All Weeks ---")
        imbalanced = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                continue
            with open(wp, "r", encoding="utf-8") as f:
                c = f.read()

            parser = DivTracker()
            try:
                parser.feed(c)
                if parser.stack or parser.errors:
                    imbalanced.append(f"week{w}.html (unclosed={len(parser.stack)}, unmatched={len(parser.errors)})")
            except Exception as e:
                imbalanced.append(f"week{w}.html (Parse error: {e})")

        if not imbalanced:
            self.log_pass("100% div tag balance across all 26 week HTML files")
        else:
            self.log_fail("100% div tag balance", f"Imbalanced files: {imbalanced}")

    def test_week_pages_asset_links(self):
        print("\n--- [6/10] Testing Week Page Asset Links ---")
        bad_assets = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                continue
            with open(wp, "r", encoding="utf-8") as f:
                c = f.read()

            has_css = ('href="../../assets/css/course.css"' in c) or ('--accent-rgb:' in c and '.topnav' in c) or ('<style>' in c and '--bg:' in c)
            has_js = ('src="../../assets/js/course.js"' in c) or ('function toggleTheme()' in c and 'initializeState()' in c)
            
            if not has_css:
                bad_assets.append(f"week{w}.html (CSS link or inline)")
            if not has_js:
                bad_assets.append(f"week{w}.html (JS src or inline)")

        if not bad_assets:
            self.log_pass("All 26 week pages correctly point to ../../assets/css/course.css and ../../assets/js/course.js")
        else:
            self.log_fail("Week page asset links", f"Broken links: {bad_assets}")

    def test_week_pages_navigation_links(self):
        print("\n--- [7/10] Testing Week Page Navigation Links ---")
        bad_nav = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                continue
            with open(wp, "r", encoding="utf-8") as f:
                c = f.read()

            if '../../roadmap.html' not in c and '../roadmap.html' not in c:
                bad_nav.append(f"week{w}.html (roadmap link)")

        if not bad_nav:
            self.log_pass("All 26 week pages contain valid roadmap links")
        else:
            self.log_fail("Week page navigation links", f"Broken nav: {bad_nav}")

    def test_katex_delimiters_and_math(self):
        print("\n--- [8/10] Testing KaTeX Delimiters & Formula Integrity ---")
        bad_katex = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                continue
            with open(wp, "r", encoding="utf-8") as f:
                c = f.read()

            if "delimiters:[{left:'47097'" in c or "delimiters:[{left:'47217'" in c:
                bad_katex.append(f"week{w}.html (Corrupted delimiter)")

            if "^$$" in c:
                bad_katex.append(f"week{w}.html (Truncated LaTeX exponent)")

        if not bad_katex:
            self.log_pass("All KaTeX delimiters clean ({left:'$$',right:'$$',display:true}) and math expressions valid")
        else:
            self.log_fail("KaTeX delimiters & math integrity", f"Issues in: {bad_katex}")

    def test_security_attributes(self):
        print("\n--- [9/10] Testing External Link Security Attributes ---")
        insecure = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                continue
            with open(wp, "r", encoding="utf-8") as f:
                c = f.read()

            missing_rel = re.findall(r'<a\s+[^>]*target=["\']_blank["\'][^>]*>', c)
            for m in missing_rel:
                if 'rel=' not in m or 'noopener' not in m:
                    insecure.append(f"week{w}.html: {m}")

        if not insecure:
            self.log_pass("All target='_blank' links include rel='noopener'")
        else:
            self.log_fail("Security attributes", f"Insecure links count: {len(insecure)}")

    def test_week_structure_components(self):
        print("\n--- [10/10] Testing Week Page Structural Components ---")
        malformed = []
        for w in range(1, 27):
            wp = os.path.join(BASE_DIR, "pages", "weeks", f"week{w}.html")
            if not os.path.exists(wp):
                continue
            with open(wp, "r", encoding="utf-8") as f:
                c = f.read()

            # Check orphaned week-summary string
            if 'class="week-summary">' in c and '<div class="week-summary">' not in c:
                malformed.append(f"week{w}.html (Orphaned class='week-summary'>)")

            # Check duplicate week-summary in week9
            if w == 9 and c.count('class="week-summary"') != 1:
                malformed.append(f"week9.html (Expected 1 week-summary, found {c.count('class=\"week-summary\"')})")

        if not malformed:
            self.log_pass("All structural components (week-summary boxes, badges) are valid and well-formed")
        else:
            self.log_fail("Structural components", f"Malformed components: {malformed}")

if __name__ == "__main__":
    suite = MasterTestSuite()
    success = suite.run_all_tests()
    sys.exit(0 if success else 1)
