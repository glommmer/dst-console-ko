# DST 모바일 콘솔 명령 모음 (한국어)

돈스타브 투게더 모바일에서 쓰는 콘솔 명령을 처음 보는 사람도 쓸 수 있게 한국어로 정리한 페이지입니다.

- 페이지: https://glommmer.github.io/dst-console-ko/
- 명령 원작자: [StarvedSteve — Read-only Public Clipboard](https://github.com/jarlini69420-bit/Read-only-Public-Clipboard-) (MIT License)

이 저장소는 원작자와 관련 없는 비공식 정리본입니다.

> **운영 종료 (2026-11-23)**
> 원작자 페이지가 따옴표 대신 `[[ ]]` 를 쓰도록 바뀌어 운영을 마쳤습니다. 매시간 동기화(GitHub Actions 정기 실행)와 매일 한국어 설명을 채우던 Claude 예약 작업은 모두 멈췄고, 이후 원작자 저장소의 변경은 이 페이지에 반영되지 않습니다. 최신 명령은 [원작자 페이지](https://jarlini69420-bit.github.io/Read-only-Public-Clipboard-/)를 보세요. 페이지와 저장소는 참고용으로 남겨 둡니다.

## 무엇이 다른가요

- 명령마다 한국어 설명, LOCAL/REMOTE 표시, 실행 순서를 붙였습니다.
- 아이폰 등의 스마트 구두점이 따옴표를 바꿔 명령이 깨지는 문제를 막기 위해, 모든 문자열을 의미가 같은 `[[...]]` 형태로 바꿨습니다. 바꾼 명령은 Lua 토큰 단위로 원본과 같은지 자동 검사합니다.
- 콘솔 한도(999자)를 넘는 명령은 페이지에 경고가 표시됩니다.

## 자동 반영 구조 (운영 당시, 지금은 멈춤)

1. **매시간** (지금은 꺼짐) GitHub Actions(`.github/workflows/sync.yml`)가 원작자 저장소를 확인합니다. 새 커밋이 있으면 `scripts/sync.py` 가 명령을 변환해 `data/` 를 갱신하고 페이지를 다시 배포합니다. 새 명령은 이때 바로 페이지에 올라갑니다(영어 제목 + "설명 준비 중").
2. **매일** (지금은 꺼짐) Claude 예약 작업이 `data/pending.json` 에 남은 명령의 한국어 설명을 `docs/KO_GUIDE.md` 에 따라 `data/ko.json` 에 채워 올립니다.

## 파일

| 경로 | 내용 | 누가 바꾸나 |
|---|---|---|
| `data/upstream.json` | 원작자 contents.json 사본 | 자동(sync) |
| `data/commands.json` | 대괄호로 바꾼 명령 | 자동(sync) |
| `data/seen.json` | NEW·업데이트 표시용 날짜 | 자동(sync) |
| `data/pending.json` | 한국어 설명이 필요한 명령 | 자동(sync) |
| `data/meta.json` | 원작자 커밋, 반영 시각 | 자동(sync) |
| `data/ko.json` | 한국어 설명 | 사람 / 예약 작업 |

다시 운영하려면 `sync.yml` 의 `schedule` 주석을 풀면 됩니다. 직접 설명을 고칠 때는 `data/ko.json` 을 수정한 뒤 `python3 scripts/check.py` 로 확인하세요.

## 라이선스

MIT. 명령 원문의 저작권은 원작자(starvedsteve)에게 있으며 원작자의 MIT License 를 따릅니다. 자세한 내용은 `LICENSE` 를 보세요.
