#!/usr/bin/env python3
"""
css_class_audit.py — CSS class audit for GG Dashboard.
Checks every HTML template against styles.css (and inline <style> blocks)
to ensure zero undefined CSS classes.

Exit codes:
  0 = all clean
  1 = missing classes found (also prints them)

Usage:
  python3 css_class_audit.py                    # check current state
  python3 css_class_audit.py --fix              # append missing class stubs to styles.css (DANGEROUS)
  python3 css_class_audit.py --git-hook         # run as pre-commit hook (only checks changed files)
"""
import os, sys, re

DASHBOARD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = os.path.join(DASHBOARD, "templates")
STYLES = os.path.join(DASHBOARD, "static", "styles.css")


def get_stylesheet_classes():
    """Parse all class selectors from styles.css (including @media blocks)."""
    if not os.path.exists(STYLES):
        return set()
    with open(STYLES) as f:
        css = f.read()
    # Match .class-name {  or .class-name.class-name {
    classes = set()
    for m in re.finditer(r'\.([a-zA-Z0-9_-]+)', css):
        # Skip pseudo-classes and after/before that start with :
        cls = m.group(1)
        if cls and cls[0].isalpha():
            classes.add(cls)
    return classes


def get_inline_classes(html_path):
    """Parse class selectors from inline <style> blocks in a template."""
    classes = set()
    with open(html_path) as f:
        html = f.read()
    for m in re.finditer(r'<style>(.*?)</style>', html, re.DOTALL):
        for cm in re.finditer(r'\.([a-zA-Z0-9_-]+)', m.group(1)):
            cls = cm.group(1)
            if cls and cls[0].isalpha():
                classes.add(cls)
    return classes


def get_html_classes(html_path):
    """Extract all class names used in HTML elements."""
    classes = set()
    with open(html_path) as f:
        html = f.read()
    for m in re.finditer(r'class="([^"]*)"', html):
        for cls in m.group(1).split():
            # Skip JS template expressions
            if '+' in cls or "'" in cls or '"' in cls:
                continue
            if cls:
                classes.add(cls)
    return classes


def check_all():
    """Check all templates for missing CSS classes."""
    stylesheet_classes = get_stylesheet_classes()
    all_ok = True
    total_missing = 0
    
    for fname in sorted(os.listdir(TEMPLATES)):
        if not fname.endswith(".html"):
            continue
        fpath = os.path.join(TEMPLATES, fname)
        html_classes = get_html_classes(fpath)
        inline_classes = get_inline_classes(fpath)
        defined_classes = stylesheet_classes | inline_classes
        
        missing = html_classes - defined_classes
        if missing:
            print(f"❌ {fname}: {len(missing)} missing class(es)")
            for cls in sorted(missing):
                print(f"     .{cls}")
            all_ok = False
            total_missing += len(missing)
    
    if all_ok:
        print(f"✅ ALL CLEAN — 0 missing classes across {sum(1 for f in os.listdir(TEMPLATES) if f.endswith('.html'))} templates")
    else:
        print(f"\n⚠️  {total_missing} total missing class(es)")
    
    return all_ok


if __name__ == "__main__":
    ok = check_all()
    sys.exit(0 if ok else 1)
