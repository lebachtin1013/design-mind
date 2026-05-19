import re
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []
        self.in_ignore = False
        self.ignore_tags = ['style', 'script', 'xml', 'head', 'meta', 'link']

    def handle_starttag(self, t, a):
        d = dict(a)
        if t in self.ignore_tags:
            self.in_ignore = True
        elif t == 'img' or t == 'v:imagedata':
            src = d.get('src', '')
            if src:
                self.data.append(f'\n[IMAGE: {src}]')

    def handle_endtag(self, t):
        if t in self.ignore_tags:
            self.in_ignore = False

    def handle_data(self, d):
        if not self.in_ignore:
            txt = d.strip()
            # ignore MS Word XML fragments like <!--[if gte mso 9]>
            if txt and not txt.startswith('<!--'):
                self.data.append(txt)

p = P()
with open('index.html', encoding='windows-1252') as f:
    content = f.read()

# remove comments
content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
p.feed(content)

for i, line in enumerate(p.data[:100]):
    print(f"{i}: {line}")
