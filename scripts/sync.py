"""원작자 저장소의 contents.json 을 읽어 한국어 페이지용 데이터를 만든다.

사용: python3 scripts/sync.py <원작자 contents.json 경로> <원작자 커밋 SHA>

만드는 파일 (data/)
- commands.json : 대괄호로 변환한 명령 목록 (원작자 순서 그대로)
- pending.json  : 한국어 설명이 없거나, 원본 명령이 바뀌어 설명을 다시 봐야 하는 항목
- seen.json     : 항목별 처음 발견한 날짜 / 마지막으로 바뀐 날짜 (NEW·업데이트 표시용)
- meta.json     : 원작자 커밋, 동기화 시각
"""
import datetime
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert import convert_checked  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
LIMIT = 999  # DST 모바일 콘솔이 한 줄에 받는 최대 글자 수(실측)


def load(name, default):
    p = os.path.join(DATA, name)
    if not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(name, obj):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def make_id(label, used):
    m = re.match(r"^\s*(\d+(?:\.\d+)*)", label)
    if m:
        base = m.group(1)
    else:
        words = re.findall(r"[a-z0-9]+", re.sub(r"\([^)]*\)", " ", label.lower()))
        base = "-".join(words[:4]) or "item"
    cid, k = base, 2
    while cid in used:
        cid, k = f"{base}-{k}", k + 1
    used.add(cid)
    return cid


def mode_of(label):
    low = label.lower()
    if "(remote" in low:
        return "REMOTE"
    if "(local" in low:
        return "LOCAL"
    return ""


def main(src, sha):
    with open(src, encoding="utf-8") as f:
        upstream = json.load(f)
    ko = load("ko.json", {"groups": {}, "commands": {}})
    seen = load("seen.json", None)
    baseline = seen is None
    seen = seen or {}
    today = datetime.date.today().isoformat()

    used, commands, pending = set(), [], []
    for order, entry in enumerate(upstream):
        label, original = entry.get("label", ""), entry.get("text", "")
        cid = make_id(label, used)
        text, status = convert_checked(original)
        h = hashlib.sha1(original.encode("utf-8")).hexdigest()[:12]

        s = seen.get(cid)
        if s is None:
            seen[cid] = {"first_seen": None if baseline else today, "changed": None, "hash": h}
        elif s.get("hash") != h:
            s["changed"], s["hash"] = today, h

        flags = []
        if status == "failed":
            flags.append("convert_failed")
        if status in ("ok", "unchanged", "failed") and len(text) > LIMIT:
            flags.append("too_long")
        commands.append({
            "id": cid,
            "order": order,
            "label": label,
            "mode": mode_of(label),
            "kind": "text" if status == "text" else "code",
            "text": text,
            "length": len(text),
            "original_length": len(original),
            "hash": h,
            "flags": flags,
        })

        k = ko["commands"].get(cid)
        if k is None:
            pending.append({"id": cid, "label": label, "reason": "new"})
        elif k.get("hash") != h:
            pending.append({"id": cid, "label": label, "reason": "changed"})

    current = {c["id"] for c in commands}
    for cid in list(seen):
        if cid not in current:
            del seen[cid]

    dump("upstream.json", upstream)
    dump("commands.json", commands)
    dump("pending.json", pending)
    dump("seen.json", seen)
    old_meta = load("meta.json", {})
    synced_at = old_meta.get("synced_at") if old_meta.get("upstream_sha") == sha else None
    dump("meta.json", {
        "upstream_repo": "jarlini69420-bit/Read-only-Public-Clipboard-",
        "upstream_sha": sha,
        "synced_at": synced_at or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(commands),
    })
    bad = [c["id"] for c in commands if c["flags"]]
    print(f"{len(commands)} commands, {len(pending)} pending, flagged: {bad or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
