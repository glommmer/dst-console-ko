"""Lua 명령의 따옴표 문자열을 롱 브래킷([[...]])으로 바꾸고, 원본과 같은 코드인지 검증한다.

- "abc"            -> [[abc]]
- 내용이 ]] 와 겹치면 -> [=[...]=]
- 줄바꿈·특수 바이트 -> string.char(...)
검증: 원본과 변환본을 Lua 토큰으로 쪼개 문자열 값까지 비교한다.
"""
import re

from lualex import lex, unescape, long_bracket


def _lb(v):
    level = 0
    while True:
        close = "]" + "=" * level + "]"
        if (v + close).find(close) == len(v):
            return "[" + "=" * level + "[" + v + close
        level += 1


def _printable(ch):
    return 32 <= ord(ch) <= 126


def _literal(v):
    if all(_printable(c) for c in v):
        return _lb(v)
    parts, i = [], 0
    while i < len(v):
        j = i
        if _printable(v[i]):
            while j < len(v) and _printable(v[j]):
                j += 1
            parts.append(_lb(v[i:j]))
        else:
            while j < len(v) and not _printable(v[j]):
                j += 1
            parts.append("string.char(" + ",".join(str(ord(c)) for c in v[i:j]) + ")")
        i = j
    return "(" + "..".join(parts) + ")"


def convert(s):
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if s.startswith("--", i):
            r = long_bracket(s, i + 2) if s.startswith("[", i + 2) else None
            if r:
                j = r[1]
            else:
                j = s.find("\n", i)
                j = n if j < 0 else j
            out.append(s[i:j])
            i = j
            continue
        if c == "[" and re.match(r"\[=*\[", s[i:]):
            _, j = long_bracket(s, i)
            out.append(s[i:j])
            i = j
            continue
        if c in "\"'":
            j = i + 1
            while s[j] != c:
                j += 2 if s[j] == "\\" else 1
            rep = _literal(unescape(s[i + 1:j]))
            prev = "".join(out).rstrip()[-1:]
            nxt = s[j + 1:].lstrip()[:1]
            if rep.startswith("(") and prev in "(," and nxt in "),":
                rep = rep[1:-1]
            if prev in ("[", "-") and rep.startswith("["):
                rep = " " + rep
            out.append(rep)
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _norm(toks):
    t, changed = list(toks), True
    while changed:
        changed, r, k = False, [], 0
        while k < len(t):
            w = t[k:k + 4]
            if len(w) == 4 and w[0] == ("NAME", "string") and w[1] == ("SYM", ".") and w[2] == ("NAME", "char") and w[3] == ("SYM", "("):
                m, vals = k + 4, []
                while m < len(t) and t[m][0] == "NUM":
                    vals.append(int(t[m][1]))
                    m += 1
                    if m < len(t) and t[m] == ("SYM", ","):
                        m += 1
                if m < len(t) and t[m] == ("SYM", ")"):
                    r.append(("STR", "".join(map(chr, vals))))
                    k, changed = m + 1, True
                    continue
            if k + 2 < len(t) and t[k][0] == "STR" and t[k + 1] == ("SYM", "..") and t[k + 2][0] == "STR":
                r.append(("STR", t[k][1] + t[k + 2][1]))
                k, changed = k + 3, True
                continue
            if k + 2 < len(t) and t[k] == ("SYM", "(") and t[k + 1][0] == "STR" and t[k + 2] == ("SYM", ")"):
                r.append(t[k + 1])
                k, changed = k + 3, True
                continue
            r.append(t[k])
            k += 1
        t = r
    return t


def same_code(a, b):
    return _norm(lex(a)) == _norm(lex(b))


CODE_HINT = re.compile(r"\b(local|function|ThePlayer|TheSim|TheWorld|ConsoleScreenSettings|ChatHistory)\b")


def is_code(s):
    if not CODE_HINT.search(s):
        return False
    try:
        lex(s)
        return True
    except Exception:
        return False


def convert_checked(s):
    """(변환본, 상태) 를 돌려준다. 상태: ok / unchanged / failed"""
    if not is_code(s):
        return s, "text"
    try:
        t = convert(s)
        if not same_code(s, t):
            return s, "failed"
        return t, ("unchanged" if t == s else "ok")
    except Exception:
        return s, "failed"
