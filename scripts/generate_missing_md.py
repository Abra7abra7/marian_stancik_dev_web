import os
import json
import re
from html.parser import HTMLParser

class HTMLToMD(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.in_article = False
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag == 'article':
            self.in_article = True
        if not self.in_article:
            return
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.skip = True
        elif tag == 'h1':
            self.text.append('\n\n# ')
        elif tag == 'h2':
            self.text.append('\n\n## ')
        elif tag == 'h3':
            self.text.append('\n\n### ')
        elif tag == 'p':
            self.text.append('\n\n')
        elif tag == 'li':
            self.text.append('\n- ')
        elif tag in ['strong', 'b']:
            self.text.append('**')
        elif tag in ['em', 'i']:
            self.text.append('*')
        elif tag == 'code':
            self.text.append('`')

    def handle_endtag(self, tag):
        if tag == 'article':
            self.in_article = False
        if not self.in_article:
            return
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.skip = False
        elif tag in ['strong', 'b']:
            self.text.append('**')
        elif tag in ['em', 'i']:
            self.text.append('*')
        elif tag == 'code':
            self.text.append('`')

    def handle_data(self, data):
        if self.in_article and not self.skip:
            self.text.append(data)

    def get_md(self):
        raw = ''.join(self.text)
        raw = re.sub(r'\n{3,}', '\n\n', raw)
        return raw.strip()

with open('blog/posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

created = 0
for p in posts:
    slug = p['slug']
    for l_dir in ['', 'sk/', 'de/', 'pl/']:
        md_path = f'blog/posts/{l_dir}{slug}.md'
        html_path = f'blog/posts/{l_dir}{slug}.html'
        if not os.path.exists(md_path):
            if os.path.exists(html_path):
                with open(html_path, 'r', encoding='utf-8') as hf:
                    hcontent = hf.read()
                parser = HTMLToMD()
                parser.feed(hcontent)
                body_md = parser.get_md()
                
                title = p.get('title')
                date = p.get('displayDate', '2026')
                if l_dir == 'sk/':
                    title = p.get('titleSk', title)
                    date = p.get('displayDateSk', date)
                elif l_dir == 'de/':
                    title = p.get('titleDe', title)
                    date = p.get('displayDateDe', date)
                elif l_dir == 'pl/':
                    title = p.get('titlePl', title)
                    date = p.get('displayDatePl', date)
                
                final_md = f"# {title}\n\n**Published:** {date} | **Author:** Marian Stancik\n\n---\n\n{body_md}\n\n---\n\n*⚠️ AI-generated | Info only | marianstancik.dev/disclaimer*\n"
                with open(md_path, 'w', encoding='utf-8') as mf:
                    mf.write(final_md)
                created += 1
                print(f"[+] Created: {md_path}")
            else:
                print(f"[!] Missing HTML for {html_path}")

print(f"Total .md files created: {created}")
