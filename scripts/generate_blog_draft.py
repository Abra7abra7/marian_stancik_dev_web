#!/usr/bin/env python3
"""
Autonomous Blog Draft Generator (Hermes Agent replacement via GitHub Actions + OpenRouter)

Reads AGENTS.md and .agents/product-marketing.md as the single source of truth for brand voice,
picks the next pending topic from blog/topics.json (or a custom --topic), generates a structured
EN + SK article via OpenRouter (default: deepseek/deepseek-chat), and delegates multilingual
publishing + PR creation to scripts/publish_post.py --langs sk,en,cs,de,pl --pr.

Environment:
  OPENROUTER_API_KEY   Required. API key for OpenRouter.
  BLOG_GEN_MODEL       Optional. Default: deepseek/deepseek-chat
  GH_TOKEN             Used by publish_post.py to open the Pull Request.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS_PATH = os.path.join(BASE_DIR, 'blog', 'topics.json')
AGENTS_MD = os.path.join(BASE_DIR, 'AGENTS.md')
BRAND_MD = os.path.join(BASE_DIR, '.agents', 'product-marketing.md')
DEFAULT_MODEL = os.environ.get('BLOG_GEN_MODEL', 'deepseek/deepseek-chat')


def read_text(path, max_chars=5000):
    if not os.path.exists(path):
        return ''
    with open(path, encoding='utf-8') as f:
        return f.read()[:max_chars]


def pick_topic(custom_topic=None):
    with open(TOPICS_PATH, encoding='utf-8') as f:
        topics = json.load(f)

    if custom_topic:
        return topics, None, {
            'id': 'custom',
            'topic': custom_topic.strip(),
            'angle': 'Practical, plain-language breakdown aligned with Marian Stancik brand voice.',
            'tags': 'AI Agents, Open Source, Practical AI',
        }

    for idx, item in enumerate(topics):
        if item.get('status') == 'pending':
            return topics, idx, item

    return topics, None, None


def call_openrouter(system_prompt, user_prompt, api_key, model):
    payload = json.dumps({
        'model': model,
        'temperature': 0.5,
        'response_format': {'type': 'json_object'},
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt},
        ],
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=payload,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://www.marianstancik.dev',
            'X-Title': 'marianstancik.dev Auto-Blog Generator',
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    content = data['choices'][0]['message']['content'].strip()
    if content.startswith('```'):
        content = content.split('\n', 1)[1].rsplit('```', 1)[0].strip()
    return json.loads(content)


def main():
    parser = argparse.ArgumentParser(description='Generate a bilingual blog draft and open a PR.')
    parser.add_argument('--topic', default='', help='Optional custom topic (overrides blog/topics.json)')
    parser.add_argument('--langs', default='sk,en,cs,de,pl', help='Target languages for publish_post.py')
    parser.add_argument('--dry-run', action='store_true', help='Generate and print summary without creating a PR')
    args = parser.parse_args()

    api_key = os.environ.get('OPENROUTER_API_KEY', '').strip()
    if not api_key:
        raise SystemExit('ERROR: OPENROUTER_API_KEY is not set.')

    topics, idx, item = pick_topic(args.topic or None)
    if not item:
        print('No pending topics left in blog/topics.json. Add more topics or pass --topic.')
        return

    agents_ctx = read_text(AGENTS_MD, 4000)
    brand_ctx = read_text(BRAND_MD, 3500)

    system_prompt = f"""You write practical, honest blog posts for Marian Stancik (marianstancik.dev).
Follow these exact brand rules and legal boundaries:

=== AGENTS.md ===
{agents_ctx}

=== BRAND VOICE ===
{brand_ctx}

MANDATORY RULES:
1. Slovak version MUST use informal "tykanie", plain everyday Slovak, short sentences, zero corporate/IT jargon.
2. English version MUST be plain, direct, honest English.
3. Critical view of AI: treat AI as a tool, not magic. Never promise overnight miracles or guaranteed compliance.
4. Legal boundary: Marian is a 3rd-year law student and does NOT provide legal advice. If mentioning GDPR or EU AI Act, explicitly state it is a subjective note, not legal advice.
5. Do NOT invent fake clients, fake testimonials, or Stripe/product pricing.
6. Return ONLY valid JSON with these exact keys:
   - title_en (string, concise, max 85 chars)
   - excerpt_en (string, 1-2 sentences, max 180 chars)
   - html_en (string, semantic HTML using <h2>, <p>, <ul>, <li>, <strong>, <code>; NO <h1>, NO <html>/<body> wrappers; 600-900 words)
   - title_sk (string, concise Slovak, max 85 chars)
   - excerpt_sk (string, 1-2 sentences in Slovak tykanie, max 180 chars)
   - html_sk (string, semantic HTML in Slovak tykanie matching html_en structure; 600-900 words)
   - tags (string, comma-separated 3-5 tags)
   - read_time (string, e.g. "5 min read")
"""

    user_prompt = (
        f"Topic: {item['topic']}\n"
        f"Angle: {item.get('angle', '')}\n"
        f"Suggested tags: {item.get('tags', 'AI Agents, Practical AI')}\n\n"
        "Write both the English and Slovak versions now as a single JSON object."
    )

    print(f"[*] Generating article via OpenRouter ({DEFAULT_MODEL}) for topic: {item['topic']}")
    draft = call_openrouter(system_prompt, user_prompt, api_key, DEFAULT_MODEL)

    required = ['title_en', 'excerpt_en', 'html_en', 'title_sk', 'excerpt_sk', 'html_sk']
    missing = [k for k in required if not draft.get(k)]
    if missing:
        raise SystemExit(f'ERROR: Model response missing keys: {missing}')

    print(f"[+] EN Title: {draft['title_en']}")
    print(f"[+] SK Title: {draft['title_sk']}")

    if args.dry_run:
        print('[*] Dry run enabled — skipping publish_post.py and PR creation.')
        return

    # Mark topic as done before publish_post commits on the PR branch
    if idx is not None:
        topics[idx]['status'] = 'done'
        with open(TOPICS_PATH, 'w', encoding='utf-8') as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
            f.write('\n')

    with tempfile.TemporaryDirectory() as tmp:
        en_file = os.path.join(tmp, 'en.html')
        sk_file = os.path.join(tmp, 'sk.html')
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(draft['html_en'])
        with open(sk_file, 'w', encoding='utf-8') as f:
            f.write(draft['html_sk'])

        cmd = [
            sys.executable,
            os.path.join(BASE_DIR, 'scripts', 'publish_post.py'),
            '--title', draft['title_en'],
            '--excerpt', draft['excerpt_en'],
            '--title-sk', draft['title_sk'],
            '--excerpt-sk', draft['excerpt_sk'],
            '--content-file', en_file,
            '--content-file-sk', sk_file,
            '--tags', draft.get('tags', item.get('tags', 'AI Agents')),
            '--read-time', draft.get('read_time', '5 min read'),
            '--langs', args.langs,
            '--pr',
        ]
        print('[*] Invoking publish_post.py to translate, sync, verify, and open PR...')
        subprocess.run(cmd, cwd=BASE_DIR, check=True)


if __name__ == '__main__':
    main()
