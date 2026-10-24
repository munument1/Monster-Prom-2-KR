# Monster Camp 한국어 번역 v0.2.1

**상태: 공개 패치 릴리즈.** `v0.2.0`의 주인공 이름 조사 오류를 추가로 교정합니다.

## 이번 업데이트

- `%CURRENTPLAYERNAME%` 뒤에 바로 붙는 `잖아`를 `이잖아`로 수정했습니다. 빨강·노랑·초록·파랑 주인공 이름이 모두 받침으로 끝나는 점을 반영했습니다.
- 본편 대사 6곳을 수정하고 같은 실수가 재발하지 않도록 회귀 테스트를 추가했습니다.

## 포함 범위

- 번역 가능한 원문: 33,837 / 33,837개
- `Localization.txt`의 공식 번역 ID: 33,818개
- 자동 테스트 17개 통과, 전체 번역 카탈로그·토큰 검사 통과, 프리뷰/모드 빌드 통과.
- 원본에 native 번역 ID가 없는 19개 문장은 표준 텍스트 오버라이드에서 제외됩니다. 원본 숫자 6개와 내부 플레이스홀더 7개는 보존됩니다.

## Steam Workshop 업데이트

아래 ZIP을 풀어 `Localization.txt`를 사용하세요. 게임 내 **Fan Translation Modtool**에서 기존 한국어 모드에 번역 파일을 교체한 뒤 공식 도구로 다시 게시하면 됩니다. ZIP 자체를 게임 원본 폴더에 덮어쓰지 마세요.

검증 가이드: https://github.com/munument1/Monster-Prom-2-KR/blob/main/docs/INGAME_VALIDATION.md
