import re
KW=set('and break do else elseif end false for function goto if in local nil not or repeat return then true until while'.split())
SYM=['...','..','==','~=','<=','>=','::','//','<<','>>']
def long_bracket(s,i):
    m=re.match(r'\[(=*)\[',s[i:])
    if not m: return None
    lv=m.group(1); close=']'+lv+']'
    j=s.find(close,i+len(m.group(0)))
    if j<0: raise ValueError('unclosed long bracket at %d'%i)
    body=s[i+len(m.group(0)):j]
    if body.startswith('\r\n') or body.startswith('\n'): body=body[1:]
    return body, j+len(close)
def unescape(b):
    out=[];i=0
    E={'n':'\n','t':'\t','r':'\r','a':'\a','b':'\b','f':'\f','v':'\v','\\':'\\','"':'"',"'":"'",'\n':'\n'}
    while i<len(b):
        c=b[i]
        if c!='\\': out.append(c); i+=1; continue
        n=b[i+1]
        if n in E: out.append(E[n]); i+=2
        elif n.isdigit():
            m=re.match(r'\d{1,3}',b[i+1:]); out.append(chr(int(m.group(0)))); i+=1+len(m.group(0))
        elif n=='x': out.append(chr(int(b[i+2:i+4],16))); i+=4
        else: raise ValueError('bad escape \\'+n)
    return ''.join(out)
def lex(s):
    toks=[];i=0;n=len(s)
    while i<n:
        c=s[i]
        if c.isspace(): i+=1; continue
        if s.startswith('--',i):
            lb=long_bracket(s,i+2) if s.startswith('[',i+2) else None
            if lb: i=lb[1]
            else:
                j=s.find('\n',i); i=n if j<0 else j
            continue
        if c=='[' and re.match(r'\[=*\[',s[i:]):
            body,i=long_bracket(s,i); toks.append(('STR',body)); continue
        if c in '"\'':
            j=i+1
            while s[j]!=c:
                if s[j]=='\\': j+=2
                elif s[j]=='\n': raise ValueError('newline in string')
                else: j+=1
            toks.append(('STR',unescape(s[i+1:j]))); i=j+1; continue
        m=re.match(r'0[xX][0-9a-fA-F]+|(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?',s[i:])
        if m and m.group(0): toks.append(('NUM',m.group(0))); i+=len(m.group(0)); continue
        m=re.match(r'[A-Za-z_]\w*',s[i:])
        if m: w=m.group(0); toks.append(('KW' if w in KW else 'NAME',w)); i+=len(w); continue
        for sy in SYM:
            if s.startswith(sy,i): toks.append(('SYM',sy)); i+=len(sy); break
        else: toks.append(('SYM',c)); i+=1
    return toks
