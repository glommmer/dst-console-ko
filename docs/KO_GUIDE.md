# 한국어 설명 작성 가이드

`data/pending.json` 에 올라온 명령의 한국어 설명을 `data/ko.json` 의 `commands` 에 채울 때 따르는 규칙입니다. 사람이 고쳐도 되고, 매일 도는 예약 작업도 이 문서를 따릅니다.

## 읽는 사람

돈스타브 투게더 모바일을 하는 한국 사용자이고, 코딩이나 콘솔 명령은 처음입니다. 코드 용어(함수, 변수, 이벤트 등)는 쓰지 말고 게임 안에서 무엇이 보이고 무엇이 달라지는지로 설명합니다.

## 항목 형식

```json
"7.1": {
  "title": "짧은 이름 (20자 안팎)",
  "summary": "무엇을 하는지 1~2문장. 게임 화면에서 보이는 변화 위주.",
  "tips": ["실행 전 알아야 할 것, 주의할 점, 사용 요령. 없으면 빈 목록"],
  "mode": "LOCAL",
  "cat": "button",
  "group": "move",
  "step": 1,
  "optional": true,
  "hash": "commands.json 에 있는 같은 명령의 hash 값"
}
```

- `mode`: 원작자 제목의 (Local)/(Remote) 를 따르되, 코드를 보고 실제로 맞는 쪽을 씁니다. 서버 쪽 컴포넌트(`components.health` 등)를 바꾸거나 `c_announce` 를 쓰면 REMOTE, 화면 위젯(`HUD`, `widgets/…`)을 만들면 LOCAL. 명령이 아닌 글이면 빈 값.
- `cat`: `button`(화면 버튼·조작) / `info`(정보 표시·알림) / `macro`(저장·관리) / `misc`(편의·기타) / `server`(서버·테스트) / `ref`(참고)
- `group`: 원작자가 여러 개로 나눈 기능(예: 7.1~7.6)은 같은 group 으로 묶고, 새 묶음이면 `groups` 에 `title`, `summary`, `order`(실행 순서 한 줄)를 추가합니다. 단독 명령은 생략.
- `step`, `optional`: 묶음 안 순서, 선택 사항 여부. 해당 없으면 생략.
- `hash`: 반드시 `data/commands.json` 의 값을 그대로 복사합니다. 이 값이 맞아야 "설명 준비 중" 표시가 사라집니다.
- 명령이 아닌 글(AI에게 보낼 문장 등)은 `alt_title`, `alt_text` 로 한국어 버전을 함께 넣을 수 있습니다.

## 문체

- 존댓말 평서문(…합니다, …됩니다). 짧은 문장.
- 게임 용어는 한국어판 표기를 씁니다(예: 비팔로, 요리솥, 아이스박스, 정신력, 머름, 위노나).
- 확실하지 않은 동작은 추측해서 단정하지 말고, 코드에서 확인되는 것만 씁니다.
- 원작자가 기존 명령을 고친 경우(`reason: changed`)는 바뀐 코드를 보고 설명이 아직 맞는지 확인한 뒤, 고칠 부분만 고치고 `hash` 를 새 값으로 바꿉니다.

## 마무리 확인

```
python3 scripts/sync.py data/upstream.json <meta.json 의 upstream_sha>
python3 scripts/check.py
```

`check.py` 가 OK 를 출력하고 `data/pending.json` 이 `[]` 이면 끝입니다.
