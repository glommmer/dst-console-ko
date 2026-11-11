"""data/ko.json 이 올바른지 검사한다. 문제가 있으면 내용을 출력하고 종료 코드 1.

python3 scripts/check.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = {"button", "info", "macro", "misc", "server", "ref"}
MODES = {"LOCAL", "REMOTE", ""}


def main():
    cmds = json.load(open(os.path.join(ROOT, "data", "commands.json"), encoding="utf-8"))
    ko = json.load(open(os.path.join(ROOT, "data", "ko.json"), encoding="utf-8"))
    groups, kc = ko.get("groups", {}), ko.get("commands", {})
    errs = []
    for gid, g in groups.items():
        for f in ("title", "summary"):
            if not str(g.get(f, "")).strip():
                errs.append(f"group {gid}: '{f}' 비어 있음")
    ids = {c["id"]: c for c in cmds}
    for cid, c in ids.items():
        e = kc.get(cid)
        if e is None:
            errs.append(f"{cid}: 한국어 설명 없음")
            continue
        for f in ("title", "summary"):
            if not str(e.get(f, "")).strip():
                errs.append(f"{cid}: '{f}' 비어 있음")
        if e.get("hash") != c["hash"]:
            errs.append(f"{cid}: hash 불일치 (설명 {e.get('hash')} / 명령 {c['hash']})")
        if e.get("mode", "") not in MODES:
            errs.append(f"{cid}: mode 는 LOCAL / REMOTE / 빈 값 중 하나")
        if e.get("cat") not in CATS:
            errs.append(f"{cid}: cat 은 {sorted(CATS)} 중 하나")
        if e.get("group") and e["group"] not in groups:
            errs.append(f"{cid}: group '{e['group']}' 이 groups 에 없음")
        if not isinstance(e.get("tips", []), list):
            errs.append(f"{cid}: tips 는 목록이어야 함")
        if c["flags"]:
            print(f"참고: {cid} flags={c['flags']}")
    for cid in kc:
        if cid not in ids:
            print(f"참고: {cid} 는 원작자 목록에서 사라졌습니다(설명은 남아 있어도 표시되지 않음)")
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    print(f"OK: 명령 {len(ids)}개 모두 한국어 설명 있음")


if __name__ == "__main__":
    main()
