import re, sys, hashlib, base64, subprocess, json, os

def assemble():
    p1 = open('build/p1.html').read()
    p1 = p1.replace('<style>', '<style>\n' + open('build/fonts.css').read(), 1)
    p1 = p1.replace('@media print{', open('build/extra.css').read() + '\n' +
                    open('build/extra2.css').read() + '\n' +
                    open('build/extra3.css').read() + '\n' +
                    open('build/extra4.css').read() + '\n@media print{', 1)
    p1 = p1.replace('</head>\n<body>\n', '</head>\n<body>\n' + open('build/sprite.html').read() + open('build/art.html').read())
    parts = [p1] + [open('build/' + f).read() for f in
                    ['p2.html', 'p3.html', 'p4.html', 'p4b.html', 'p5.html']]
    parts[-1] = parts[-1].replace('</body>', '').replace('</html>', '')
    return ''.join(parts) + open('build/p6.html').read() + open('build/p7.html').read() + open('build/p8.html').read() + '\n</body>\n</html>\n'

def sha(txt):
    return "'sha256-" + base64.b64encode(hashlib.sha256(txt.encode('utf-8')).digest()).decode() + "'"

def add_csp(html):
    scripts = re.findall(r'<script>(.*?)</script>', html, re.S)
    hashes = ' '.join(dict.fromkeys(sha(s) for s in scripts))
    csp = ("default-src 'none'; "
           "script-src " + hashes + "; "
           "style-src 'unsafe-inline'; "
           "img-src 'self' data:; "
           "font-src 'self' data:; "
           "connect-src 'none'; "
           "media-src 'none'; "
           "object-src 'none'; "
           "frame-src 'none'; "
           "worker-src 'none'; "
           "manifest-src 'none'; "
           "base-uri 'none'; "
           "form-action 'none'")
    head = ('<meta http-equiv="Content-Security-Policy" content="' + csp + '">\n'
            '<meta name="referrer" content="no-referrer">\n'
            '<meta name="format-detection" content="telephone=no">\n')
    return html.replace('<meta name="theme-color"', head + '<meta name="theme-color"', 1)

def minify(html):
    # JS: terser per script block (locals mangled, top level kept so blocks still see each other)
    def js(m):
        src = m.group(1)
        p = subprocess.run(['npx','--no-install','terser','--compress','--mangle','--format','comments=false'],
                           input=src, capture_output=True, text=True)
        return '<script>' + (p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else src) + '</script>'
    html = re.sub(r'<script>(.*?)</script>', js, html, flags=re.S)
    # CSS
    def css(m):
        s = re.sub(r'/\*.*?\*/', '', m.group(1), flags=re.S)
        s = re.sub(r'\s*([{}:;,>])\s*', r'\1', s)
        s = re.sub(r';}', '}', s)
        s = re.sub(r'\s+', ' ', s)
        return '<style>' + s.strip() + '</style>'
    html = re.sub(r'<style>(.*?)</style>', css, html, flags=re.S)
    # HTML: comments + whitespace between tags on their own lines
    html = re.sub(r'<!--(?!\[if).*?-->', '', html, flags=re.S)
    html = re.sub(r'>\n\s+<', '><', html)
    return html

src = assemble()
open('babywegweiser.html', 'w').write(add_csp(src))
print('readable build:', len(add_csp(src)), 'bytes')

if '--min' in sys.argv:
    m = add_csp(minify(src))
    open('babywegweiser.min.html', 'w').write(m)
    print('minified build:', len(m), 'bytes')
