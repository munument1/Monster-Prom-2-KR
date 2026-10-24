# Monster Camp 한국어 번역 (작업 중)

대상: **Monster Prom 2: Monster Camp**, 설치본 `2.31.a` (PC / Unity 2019.4.16f1).

이 저장소는 1편 한국어 번역 저장소와 독립적으로 관리합니다. 현재 원본 게임 파일은 수정하지 않았습니다.

## 원문 구조

- 영문 이벤트/대사: `MonsterCamp_Data/StreamingAssets/aa/StandaloneWindows/texts_assets_all.bundle` 안의 `english_camp_events_*`, `english_camp_challenges`
- 메뉴/설정 등 UI: 같은 번들의 `english_camp_metatexts` (주석과 끝 쉼표가 있는 JSON 유사 형식)
- 게임 내 한국어 폰트와 `language_korean` 프로필이 이미 존재함
- 게임에 **Fan Translation Modtool**이 있으며, `Localization.txt`의 `ID<TAB>번역문` 형식과 한국어 폰트 프로필을 확인했습니다.

추출 기준 전체 **33,850개 위치**(이벤트/선택지 32,063, UI 1,787), 중복 영문 제거 시 **31,238개**. 이벤트는 약 1,077개. 전체 카탈로그에 포함된 원문을 무조건 게임에서 표시한다고 단정하지 않습니다. 대사의 일부는 결과 분기·이벤트 조건·DLC에 따라 노출됩니다.

## 초벌 번역 상태

- 메인 메뉴·설정·일부 캐릭터/의상 선택 관련 UI: `translations/menu_ko.json` (92개)
- 오프닝 장면 전체: `translations/prologue_ko.json` (23개)
- 캠프 도전 과제 53개에 딸린 문구 106개: `translations/challenges_ko.json`
- 메타 상점·기본 이벤트·크레딧: `translations/small_events_ko.json` (36개)
- 합계 257개. 게임 구동·표시 검증 전이며 전체 번역은 미완료.

## 로컬 재현

Python 3.14 및 `requirements.txt` 설치가 필요합니다. 설치 위치는 환경 변수로 바꿀 수 있습니다.

```powershell
cd 'D:\Codex_Trans\Monster-Prom-2-KR'
python -m pip install -r requirements.txt
$env:MCKR_GAME_DIR = 'C:\Games\Steam\steamapps\common\Monster Prom 2 - Monster Camp'
python .\inspect_sources.py
python .\extract_catalog.py
python .\build_preview.py
python .\build_mod.py
```

`work/catalog.jsonl`에는 키, 해당 에셋, 이벤트 ID, 원문 행 번호, 텍스트 열 번호, 영문 원문, 검증용 해시가 저장됩니다. `work/inventory.json`에는 구조 집계가 저장됩니다. 전체 원문 추출물과 미적용 텍스트 프리뷰는 `work/` 아래에 있으며 Git 추적에서 제외합니다.

초벌 번역 딕셔너리는 해당 카탈로그의 ID에 매핑되고, 검증기는 `%CURRENTPLAYERNAME%`, `%WEEKS%`, `[n]`, `[sub]` 등 게임의 변수·서식 토큰이 그대로 유지되었는지 검사합니다. 실제 탭·개행을 번역 값에 삽입하는 것도 차단합니다.

`build_preview.py`는 **텍스트 프리뷰만 생성**합니다. `build_mod.py`는 실제 게임의 `CustomLocalizationParser`가 읽는 2열 탭 구분 형식인 `build/MonsterCampKR/Localization.txt`를 생성합니다. 어떤 스크립트도 게임 원본 변경이나 창작마당 게시를 수행하지 않습니다.

### 게임에 적용할 때

게임 내부의 **Fan Translation Modtool**에서 한국어를 선택하고 번역 모드를 생성하면 게임이 해당 모드의 `Descriptor.mcmtd`를 만듭니다. 출력한 `Localization.txt`를 공식 도구에서 번역 파일로 사용하세요. 모드 데이터는 일반적으로 Unity `Application.persistentDataPath/Mods/<모드 ID>/` 아래에 저장됩니다. 게임 실행 중 파일 교체나 기존 모드 덮어쓰기는 피하고, 실제 모드 활성화 및 한글 표시를 확인해야 합니다.

`Mods/<모드 ID>/`에 파일만 직접 배치해도 '번역 모드 불러오기' 목록에 자동 등록되지는 않습니다. 목록은 Steam 구독 및 `mods.mpd`에 의해 관리되므로, 직접 `mods.mpd`를 편집하는 방식은 사용하지 않습니다.

## 남은 작업

1. 공식 번역 모드 생성·활성화 후 인게임 렌더링 시험
2. 번역 데이터 확대, 변수/조사 자연화 및 UI 줄바꿈 검수
3. 게임 업데이트 후 원본 ID와 문구 대조·필요한 부분만 재번역

캐릭터 이름과 기본 능력치 번역은 1편과 최대한 통일했습니다(아라비, 캘큘레스터, 데미안; 지능/대담함/창의력/매력/재미).
