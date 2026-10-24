# Monster Camp 한국어 번역 (작업 중)

대상: **Monster Prom 2: Monster Camp**, 설치본 `2.31.a` (PC / Unity 2019.4.16f1).

이 저장소는 1편 한국어 번역 저장소와 독립적으로 관리합니다. 현재 원본 게임 파일은 수정하지 않았습니다.

## 원문 구조

- 영문 이벤트/대사: `MonsterCamp_Data/StreamingAssets/aa/StandaloneWindows/texts_assets_all.bundle` 안의 `english_camp_events_*`, `english_camp_challenges`
- 메뉴/설정 등 UI: 같은 번들의 `english_camp_metatexts` (주석과 끝 쉼표가 있는 JSON 유사 형식)
- 게임 내 한국어 폰트와 `language_korean` 프로필이 이미 존재함
- 게임에 **Fan Translation Modtool**이 있으며, `Localization.txt`의 `ID<TAB>번역문` 형식과 한국어 폰트 프로필을 확인했습니다.

추출 기준 전체 **33,850개 위치**(이벤트/선택지 32,063, UI 1,787), 중복 영문 제거 시 **31,238개**. 이벤트는 약 1,077개. 전체 카탈로그에 포함된 원문을 무조건 게임에서 표시한다고 단정하지 않습니다. 대사의 일부는 결과 분기·이벤트 조건·DLC에 따라 노출됩니다.

## 초벌 번역 상태 · 2026-10-24

- 메인 메뉴·설정·일부 캐릭터/의상 선택 관련 UI: `translations/menu_ko.json` (92개)
- 오프닝 장면 전체: `translations/prologue_ko.json` (23개)
- 캠프 도전 과제 53개에 딸린 문구 106개: `translations/challenges_ko.json`
- 메타 상점·기본 이벤트·크레딧: `translations/small_events_ko.json` (36개)
- 캠프 일반 이벤트 전체: `translations/standard_ko.json` (302개)
- 캠프 음료 이벤트 전체: `translations/drinks_ko.json` (351개)
- 러브로그 전체: `translations/lovelog_ko.json` (250개)
- 소문 진술 전체: `translations/gossipstatements_ko.json` (178개)
- 선택형 소문 이벤트 첫 160개: `translations/gossips_001_160_ko.json`
- 아이스브레이커 첫 320개: `translations/icebreakers_001_160_ko.json`, `icebreakers_161_320_ko.json`
- 엔딩 첫 260개: `translations/endings_001_130_ko.json`, `endings_131_260_ko.json`
- 메인 게임 이벤트 `tasting`, `campfireflippers`, `robotsurvivalskills`: 109개
- 본편 곰 습격·마법 나무 이벤트 8개: `translations/maingame_bearattack*_ko.json`, `translations/maingame_magictree*_ko.json` (747개)
- 추가 본편 이벤트 9개: `pokerwolves`, `firstaid`, `lakeonfiredm`, `repurposedeer`, `joinhermitcrab`, `spoilerlynx`, `opinionatedsealion`, `slasherdm`, `weirdchallengemo` (704개)
- 추가 본편 이벤트 8개: `weirdchallengedh`, `slashercl`, `fishingcl`, `calmeetsfear`, `waterproofcl`, `holdingbreath`, `succulentnewhome`, `readingsafety` (673개)
- 추가 본편 이벤트 8개: `scottisatree`, `landscape`, `elevatethathedgehog`, `sirensoundcloud`, `ultimateknot`, `macaroniart`, `glamping`, `hungergamesaa` (666개)
- 추가 본편 이벤트 8개: `hungergamesj`, `slasherdh`, `slasheraa`, `prankmasterzcl`, `prankmasterzdh`, `prankmasterzaa`, `prankmasterzj`, `ismiloabear` (760개)
- 추가 본편 이벤트 8개: `chameleondm`, `deathtomosquitoes`, `tentsupplies`, `antterrarium1`, `chameleondh`, `chameleonaa`, `chameleonc`, `chameleonm` (688개)
- 추가 본편 이벤트 7개: `chameleonj`, `ceoc`, `ceom`, `antterrarium2`, `antterrarium3`, `ceoj`, `ceodm` (635개)
- 추가 본편 이벤트 6개: `ceodh`, `ceoaa`, `yogapoints`, `moralcompass`, `succulentcareer`, `slashercops` (547개)
- 추가 본편 이벤트 4개: `dewolf`, `piratechest`, `hermitcrabupgrade`, `fortuneteller` (377개)
- 추가 본편 이벤트 8개: `survivingyourself`, `ceodomef2p`, `ceodomemonetization`, `slasherlastsummer`, `slashercar`, `waterdungeonsupport`, `trolleyproblem`, `smalltopia` (763개)
- 추가 본편 이벤트 8개: `yasurvivalscenario`, `strandedinthelake`, `phonecharger`, `howtostartafire`, `helpinginjuredanimal`, `findingfood`, `noconflict`, `howtoswimscott` (698개)
- 추가 본편 이벤트 8개: `criteriaofidentification`, `animaltrapunicorn`, `sigils`, `scottthecheerleaderdmj`, `predictweather`, `lifeguardscpr`, `lifeguardswhogoes`, `lifeguardsflag` (771개)
- 추가 본편 이벤트 8개: `lifeguardslakepeople`, `Captured`, `alternativetoakiss`, `sexyupdate`, `lovedata`, `bp_dahliabestsummer1`, `bp_dahliabestsummer2`, `bp_dahliabestsummer3` (709개)
- 추가 연속 스토리 8개: `bp_caluprising1~3`, `dp_calfatherhood1~3`, `dp_hex1~2` (683개)
- 추가 본편 이벤트 9개: `dp_hex3`, `dp_appliancea1~2`, `dp_applianceb1~2`, `dp_appliancec1~2`, `dp_applianced1~2` (782개)
- 추가 연속 스토리 8개: `dp_batniss1~3`, `dp_calgrim1~3`, `dp_jerry1~2` (729개)
- 추가 연속 스토리 8개: `dp_jerry3`, `dp_aaraviamends1~3`, `dp_milocat1~3`, `AnimeWorkout3` (855개)
- 추가 본편 스토리 8개: `dp_DahliaRival1~3`, `dp_JoyCoven1~3`, `weirdchallengedm`, `slashermo` (1,269개)
- 추가 본편 이벤트 8개: `weirdchallengej`, `weirdchallengec`, `chickenfight`, `weirdchallengeaa`, `hungergamesdm`, `hungergamesdh`, `manorglowup`, `sexyoutofwater` (614개)
- 추가 본편 이벤트 8개: `threeleggedrace`, `pollination`, `truffles`, `slashernickname`, `slashercollection`, `babayaganewwitches`, `babayagacat`, `babayagaeatyou` (723개)
- 추가 본편 이벤트 8개: `interrogation`, `divideandconquer`, `coolweapons`, `cookiespranks`, `babayagaball`, `cookiesflavor`, `cookiesmascot`, `cookiesthousand` (696개)
- UI 추가 586개: `translations/ui_*_ko.json` 네 파일

**누적 17,862 / 33,850개 위치(52.77%)**를 초벌 번역했습니다. 번역 완료 이벤트는 1,077개 중 611개이며, 게임 구동·표시 검증과 전체 한국어 번역은 아직 미완료입니다. 본편 주 스토리는 15,198 / 27,700개 위치(54.87%)가 번역되었습니다.

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
python .\report_progress.py
python .\next_translation_batch.py --limit 16
python .\inspect_images.py
python .\inspect_images.py --bundle drinks_assets_all.bundle --preview-count 2
python -m unittest discover -s tests -v
```

`work/catalog.jsonl`에는 키, 해당 에셋, 이벤트 ID, 원문 행 번호, 텍스트 열 번호, 영문 원문, 검증용 해시가 저장됩니다. `work/inventory.json`에는 구조 집계가 저장됩니다. 전체 원문 추출물과 미적용 텍스트 프리뷰는 `work/` 아래에 있으며 Git 추적에서 제외합니다.

초벌 번역 딕셔너리는 해당 카탈로그의 ID에 매핑되고, 검증기는 `%CURRENTPLAYERNAME%`, `%WEEKS%`, `[n]`, `[sub]` 등 게임의 변수·서식 토큰이 그대로 유지되었는지 검사합니다. 실제 탭·개행을 번역 값에 삽입하는 것도 차단합니다.

`build_preview.py`는 **텍스트 프리뷰만 생성**합니다. `build_mod.py`는 실제 게임의 `CustomLocalizationParser`가 읽는 2열 탭 구분 형식인 `build/MonsterCampKR/Localization.txt`를 생성합니다. 어떤 스크립트도 게임 원본 변경이나 창작마당 게시를 수행하지 않습니다.

현재 모드 파일 출력은 **17,844개 ID**입니다. 검토한 번역 17,862개 중 원문에 번역 ID가 없는 **18개 행**(음료 이벤트 14개, `antterrarium2` 본편 대사 3개, `strandedinthelake` 대사 1개)은 공식 텍스트 오버라이드에서 제외하고 `build/MonsterCampKR/manifest.json`의 `requires_asset_patch`에 기록합니다. 이 항목들은 추후 별도 에셋 적용 경로 확인이 필요합니다. 대사 번역용 원문 위치 전체에는 이런 ID 없는 행이 총 19개 존재하며, 그중 18개가 현재 번역되었습니다.

원본 ID·태그·변수 검사 외에도, PowerShell의 인코딩 오류로 한글이 `?`로 손상된 데이터를 사전 차단합니다. 번역·검수 기준은 [docs/TRANSLATION_GUIDE.md](docs/TRANSLATION_GUIDE.md)에 있습니다.

`next_translation_batch.py`는 완료 이벤트를 제외한 다음 미번역 이벤트와 권장 파일명을 카탈로그 순서대로 표시합니다. `--asset`, `--limit`, `--include-partial` 및 `--json` 옵션으로 범위를 바꿀 수 있습니다. 번역 파일 내 중복 JSON ID와 특수 대문자 꺾쇠 태그도 검증합니다.

### 이미지 안에 박힌 영어 번역

`Localization.txt`는 텍스트 ID를 덮어쓰는 형식이므로 그림의 픽셀 자체에 영어가 그려진 경우에는 영향을 주지 않습니다. 실제 `drinks_assets_all.bundle`의 `fake_spellpage` 텍스처(380×380)에는 영어 주문서 글씨가 직접 포함되어 있음을 확인했습니다. 별도의 이미지 편집 및 안전한 자산 교체 경로가 필요합니다.

`inspect_images.py`는 Unity 이미지 파일을 **읽기 전용**으로 조사해 `work/image_inventory.json`에 번들·경로 ID·스프라이트 참조·크기·포맷 등을 기록합니다. 현재 설치본 번들 28개에서 `Texture2D` 2,316개와 `Sprite` 2,300개를 찾았습니다. 이름만으로 영어 글씨가 있을 것으로 추정한 텍스처는 109개이며, 이미지 실제 글자 수가 검증된 것은 아닙니다. 미리보기는 명시한 `--preview-count` 만큼만 무시되는 `work/images_preview/`에 만듭니다. 이미지 원본은 GitHub에 올리지 않습니다.

[이미지 현지화 조사 보고서](docs/IMAGE_LOCALIZATION_AUDIT.md)는 배경·갤러리·상점·음료·아이콘 등 6개 주요 번들의 실제 그림 42종을 시각 검수하고, 영문이 그림에 인쇄된 구체적 사례와 텍스처 재직렬화의 기술적 한계를 정리했습니다. 임의 PNG 복사만으로 게임의 이미지가 바뀌는 것은 아니며, 게임 실행·번들 오버라이드 로더는 아직 검증하지 않았습니다.

확인된 텍스처 하나의 한국어 문구 초안은 `image_translations/candidates.json`에 보존했습니다. 이 JSON은 실제 이미지 파일이 아니며 아직 게임에 적용되지 않았습니다.

### 게임에 적용할 때

게임 내부의 **Fan Translation Modtool**에서 한국어를 선택하고 번역 모드를 생성하면 게임이 해당 모드의 `Descriptor.mcmtd`를 만듭니다. 출력한 `Localization.txt`를 공식 도구에서 번역 파일로 사용하세요. 모드 데이터는 일반적으로 Unity `Application.persistentDataPath/Mods/<모드 ID>/` 아래에 저장됩니다. 게임 실행 중 파일 교체나 기존 모드 덮어쓰기는 피하고, 실제 모드 활성화 및 한글 표시를 확인해야 합니다.

`Mods/<모드 ID>/`에 파일만 직접 배치해도 '번역 모드 불러오기' 목록에 자동 등록되지는 않습니다. 목록은 Steam 구독 및 `mods.mpd`에 의해 관리되므로, 직접 `mods.mpd`를 편집하는 방식은 사용하지 않습니다.

## 남은 작업

1. 공식 번역 모드 생성·활성화 후 인게임 렌더링 시험
2. 번역 데이터 확대, 변수/조사 자연화 및 UI 줄바꿈 검수
3. 게임 업데이트 후 원본 ID와 문구 대조·필요한 부분만 재번역

캐릭터 이름과 기본 능력치 번역은 1편과 최대한 통일했습니다(아라비, 캘큘레스터, 데미안; 지능/대담함/창의력/매력/재미).
