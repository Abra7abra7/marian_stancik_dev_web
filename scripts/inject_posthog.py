#!/usr/bin/env python3
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTHOG_TAG = '<script defer src="/js/posthog.js?v=consent1"></script>'
UMAMI_TAG = '<script defer src="https://api.marianstancik.dev/script.js" data-website-id="ec1c0df8-e51f-4236-9ad0-e3992f0b1637"></script>'

updated_files = 0

for root, dirs, files in os.walk(BASE_DIR):
    # Ignore node_modules, .git, scratch
    if any(p in root for p in ['.git', 'node_modules', 'scratch']):
        continue
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if POSTHOG_TAG in content:
                continue

            if '</head>' in content:
                # If umami is missing from head as well, add both
                if 'api.marianstancik.dev/script.js' not in content:
                    injection = f"{UMAMI_TAG}\n{POSTHOG_TAG}\n</head>"
                else:
                    injection = f"{POSTHOG_TAG}\n</head>"
                new_content = content.replace('</head>', injection, 1)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files += 1

print(f"PostHog snippet injected into {updated_files} HTML files successfully!")
