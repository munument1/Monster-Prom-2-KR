# Monster Prom 2: Monster Camp 이미지 현지화 조사

> 조사일: 2026-10-24 / 대상: 로컬 Windows Steam 설치본 `C:\Games\Steam\steamapps\common\Monster Prom 2 - Monster Camp` / 게임 실행·인게임 렌더링 **미확인**

## 결론과 적용 우선순위

**이미지 자체에 영문 글자가 그려진 사례를 실제 추출 이미지에서 확인했다.** `background_spellpage`의 주문 내용, `background_knifebook`의 표지, `background_cactusmovie`의 영화 포스터, `background_lastwill`의 유언장, `icon_npc_shopkeeper`의 모자 글자는 문자 리소스 번역만으로 바뀌지 않는다. `drinks/thebest`의 작은 상품 라벨과 `drinks/fake_lastwill`에도 같은 종류의 픽셀 문구가 보인다.

반면 선택지·메뉴·크레딧에 쓰일 문자열은 `texts_assets_all.bundle`의 `english_camp_metatexts` 등에서 별도로 관리된다. 예컨대 `GLR_TTL_CRD = Credits`, `STT_CRE = View Full Credits`, `XTR_CRE_8` 및 `XTR_CRE_9`에는 크레딧 본문 텍스트가 있다. 조사한 `gallery/credits_02,08,16,32,38` 그림 샘플 자체에는 크레딧 글자가 보이지 않았다. **동적 UI/대사와 이미지 내부 문구는 서로 다른 교체 경로가 필요하다.** 이 판단은 파일 내용 기준이며 실제 게임의 합성 순서나 로딩 경로는 검증하지 않았다.

권장 작업 순서는 **(1) 배경 속 책·문서·포스터 → (2) 음료/소품에 인쇄된 글자 → (3) NPC 아이콘·갤러리의 장식 글자** 순이다. 의미 없는 기호나 로고는 반드시 한국어로 바꿀 필요가 없으며 작은 문자·패러디 작품명은 문맥 확인 후 결정한다.

## 조사 방법·범위

- `UnityPy 1.25.2`, `Pillow 12.2.0`에서 게임의 `MonsterCamp_Data/StreamingAssets/aa/StandaloneWindows/*_assets_all.bundle`을 **읽기 전용**으로 열었다. `Texture2D`/동일 이름의 `Sprite` 오브젝트를 인벤토리하고 텍스처 원본 크기·포맷을 기록했다.
- 6개 번들에서 **고유 이름의 Texture2D 635개 + Sprite 635개(총 1,270개)**를 찾았다. 각 번들에서 두 유형의 이름 집합은 완전히 일치하고 중복 이름은 없다. `Sprite.image`와 `Texture2D.image` 픽셀을 42개 샘플에서 비교하여 동일함을 확인했다. **전체 635쌍의 픽셀 동일성 검사는 수행하지 않았다.**
- 배경 12종, 갤러리 9종, 메타 상점 6종, 음료 9종, 플레이어 아이콘 3종, NPC 아이콘 3종의 **총 42종**을 디코딩하여 육안으로 확인했다. 화면 전체에서 찾은 결과가 아닌 **지정 샘플 조사**이므로 다른 그림의 문자 존재를 배제하지 못한다.
- 작은 JPEG 미리보기 6개 접촉 시트와 9개 개별 확대본을 `work/images_audit/`에 보관한다. `/work/`는 프로젝트 `.gitignore`로 제외되어 저장소 문서만 배포할 때 미리보기는 동봉되지 않는다. 아래 상대 경로는 해당 로컬 작업공간에서 확인할 수 있다.
- 별도의 `art_assets_all.bundle`은 설치된 번들 목록에서 발견되지 않았다. 관련 원화는 주로 `gallery`와 `backgrounds` 그룹에 포함되어 있어 이 두 번들을 ‘아트’ 범위로 함께 조사했다. AssetBundle 바깥의 게임 리소스와 모든 DLC·실제 노출 장면까지 망라하지는 않았다.

## 이미지 종류·수량·해상도

| 번들 파일 접두어 | Texture2D | Sprite | Texture2D 해상도별 수량 | 텍스처 포맷 |
|---|---:|---:|---|---|
| `gallery_assets_all.bundle` | 210 | 210 | 1024×1024 63개, 1276×1076 60개, 2048×1024 45개, 1920×1080 37개, 512×1024 2개, 760×1080 1개, 1024×512 1개, 4×4 1개 | BC7(25) 210 |
| `backgrounds_assets_all.bundle` | 109 | 109 | 1276×1076 109개 | BC7(25) 109 |
| `metashop_assets_all.bundle` | 16 | 16 | 256×256 15개, 600×600 1개 | BC7(25) 15, RGBA32(4) 1 |
| `drinks_assets_all.bundle` | 135 | 135 | 380×380 132개, 256×256 3개 | RGBA32(4) 132, BC7(25) 3 |
| `charactericons_assets_all.bundle` | 60 | 60 | 256×256 40개, 512×512 20개 | BC7(25) 60 |
| `npcicons_assets_all.bundle` | 105 | 105 | 256×256 102개, 16×16 3개 | BC7(25) 104, DXT5(12) 1 |
| **합계** | **635** | **635** | **고유 텍스처 635개** | BC7 501, RGBA32 133, DXT5 1 |

> 위 수치는 `Texture2D`와 이름이 같은 `Sprite`를 **별도로** 센 것이다. ‘1,270개 독립 PNG’가 아니라 기본적으로 **635개의 이미지가 635개의 Sprite 오브젝트와 짝지어진 구조**다. 현재 샘플은 개별 스프라이트 전체 이미지가 텍스처 전체와 일치했다. 다중 스프라이트 아틀라스가 존재하는지 여부는 전체 Sprite 내부의 `rect`·텍스처 참조 분석까지 끝낸 결과가 아니다.

## 픽셀에 포함된 영문: 확인 사례

| 텍스처 이름(소속 번들) | 실제 이미지에서 확인된 부분 | 분류·제안 |
|---|---|---|
| `background_spellpage` (backgrounds) | 양피지 안에 `FORBIDDEN COOL JOSH HEART SPELL`, `I CAN'T BELIEVE U KILLED HIM U MONSTER`, `MIX IN A BOWL` 등 영문 손글씨 | **이미지 픽셀**. 작은 필기체를 재그림/합성 후 원본 배경과 색감 일치 필요 |
| `background_lastwill` (backgrounds) | 문서 표제 `Last Will & Test`, `Walter Wisconsin` | **이미지 픽셀**. 같은 소품이 `drinks/fake_lastwill`에 재등장하므로 두 이미지 함께 조정 |
| `background_knifebook` (backgrounds) | 책 표지 `Little Kenny Knows His Knife` | **이미지 픽셀**. 표지 일러스트에 곡선/광원 맞춰 한국어 제목 배치 |
| `background_cactusmovie` (backgrounds) | 영화 포스터의 `OW MY VAGINA!` 제목과 작은 영문 출연진·제작진 | **이미지 픽셀**. 제목뿐 아니라 작은 크레딧 문자열도 포함 |
| `background_heartbrokenpost` (backgrounds) | 폴라로이드 아래쪽에 손글씨 영문 문장 | **이미지 픽셀**. 축소 화면에서도 읽히는지 게임 내 확인 필요 |
| `background_horsebets` (backgrounds) | 메모 카드에 `CAN HORSES LOVE?`, `DO HORSES HAVE EARS?` 등 영문 | **이미지 픽셀**. 글씨가 작은 소품이므로 번역 길이 축약 필요 |
| `background_murderdiary` (backgrounds) | 책 표지에 영문 제목·장식 문자 | **이미지 픽셀**. 이름을 대사/이벤트 번역과 맞춰야 함 |
| `thebest` (drinks) | 트로피 `#1`, 옆 캔 `MOOSE MILK` 영문 | **이미지 픽셀**. `#1`은 그대로 둬도 되나 캔 라벨은 선택적으로 현지화 |
| `fake_lastwill` (drinks) | 작은 소품 스프라이트에 `Last Will & Test / Walter Wisconsin` | **이미지 픽셀**. 배경 `background_lastwill`과 병행 수정 |
| `icon_npc_shopkeeper` (npcicons) | 모자에 `NARRATOR`가 인쇄됨 | **이미지 픽셀**. 아이콘의 좁은 인쇄 공간 때문에 ‘해설자’ 같은 축약 후보 검토 |
| `sk_secretendings_damien_sketches` (gallery) | 스케치 4컷 구분자 `A/B/C/D` | **이미지 픽셀**이지만 알파벳 분류기호. 번역 우선순위 낮음 |

참조용 접촉 시트:

- 배경 12종: `work/images_audit/backgrounds_contact.jpg` / 주문서 상세: `work/images_audit/backgrounds__background_spellpage.jpg` / 유언장 상세: `work/images_audit/backgrounds__background_lastwill.jpg`
- 갤러리 9종: `work/images_audit/gallery_contact.jpg` / 크레딧 배경 샘플: `work/images_audit/gallery__credits_02.jpg`
- 메타 상점 6종: `work/images_audit/metashop_contact.jpg` / 음료 9종: `work/images_audit/drinks_contact.jpg`
- 캐릭터 아이콘 3종: `work/images_audit/charactericons_contact.jpg` / NPC 아이콘 3종: `work/images_audit/npcicons_contact.jpg`

## 표본에서 확인되지 않은 경우와 동적 UI

| 구분 | 관찰 | 판정 한계 |
|---|---|---|
| 메타 상점 | `metashop_manualbase`, `manualstats`, `manualros`, `sketch`, `op_hal`, `drinkschoice_fg` 샘플에는 영어 글자 미발견 | 아이템명·설명 등은 별도 `metatexts` 가능성이 높으나 실제 화면 UI 매핑 미확인 |
| 캐릭터 아이콘 | `icon_character_red`, `red_border`, `ksgreen` 샘플에 문자 미발견 | **전체 아이콘이 무문자**라는 결론 아님 |
| 갤러리 | 추출한 `credits_02`, `08`, `16`, `32`, `38`은 그림으로 구성되고 크레딧 이름 문구가 보이지 않음 | `XTR_CRE_8/9`의 글자가 언제 어디에 오버레이되는지 실게임 미확인 |
| 음료 | 일반 `whiskey`, `sacredblood`, `oldchumschampagne` 등 일부는 읽을 수 있는 영어 라벨이 보이지 않음 | `thebest`, `fake_lastwill`처럼 물체 안 글자가 있는 경우는 별도 작업 |
| 텍스트 자산 | `english_camp_metatexts/STT_CRE`, `GLR_TTL_CRD`, `XTR_CRE_8`, `XTR_CRE_9` 등 추출된 실제 문자열을 확인 | 이 값은 텍스트 자산이므로 기존 `Localization.txt` 번역 대상. 화면 출력 경로와 폰트 표시 여부는 미확인 |

## 이미지 교체 방법 및 재패킹 전략

1. **원본 Texture2D/Sprite 추출.** `UnityPy.load(bundle)`에서 해당 이름을 찾고 `Texture2D.image` 또는 `Sprite.image`를 PNG로 내보낸다. Sprite가 자르기·메시·피벗 정보를 가진 경우, 실제 편집 단위가 Texture2D의 전체 텍스처인지 하위 사각 영역인지 먼저 확인한다.
2. **글자가 있는 부분만 편집.** 텍스처를 원본 픽셀 해상도(예: 1276×1076, 380×380), RGBA 알파, 테두리·질감·색상·여백을 유지하며 편집한다. 글씨를 지우고 자연스럽게 바탕을 복원한 다음 한국어를 다시 그린다. 책·종이의 원근, 음료 라벨의 기울기, 낮은 해상도에서의 가독성을 따로 검토한다. 원본 애셋명·Sprite 메타데이터는 유지한다.
3. **텍스처 재인코딩·재직렬화.** 설치된 `UnityPy 1.25.2`의 `Texture2D.set_image(image, target_format=...)` → `Texture2D.save()` → `BundleFile.save()` 경로로 **메모리 내 검증을 실제로 수행**했다. `metashop_manualbase` 256×256 BC7(25)를 RGBA32(4)로 바꿔 재직렬화한 뒤, 반환된 번들 바이트를 `UnityPy.load(bytes)`로 다시 읽어 **256×256 / 포맷 4**를 확인했다. 게임 설치 디렉터리에는 쓰지 않았다.
4. **압축 포맷·아틀라스 주의.** 현재 자산은 BC7, RGBA32, 일부 DXT5이고 `m_StreamData`가 외부 `.resS` 경로를 가리키는 사례가 있다. RGBA32로 바꾸면 파일·VRAM 사용량이 늘 수 있다. 실제 in-memory 재직렬화 결과 `metashop` 번들 원본 483,092바이트 → 3,524,081바이트가 되었으므로 용량 증가와 스트리밍 데이터 처리 검증이 필수다. 기존 BC7로 **동일 포맷·동일 크기**를 유지한 재압축은 이번 조사에서 증명하지 않았다. 여러 Sprite가 한 아틀라스를 공유한다면 임의로 스프라이트 하나만 자르거나 전체 레이아웃·UV·피벗·보더·메시를 변경해서는 안 된다.
5. **실제 적용 경로 검증.** 현행 팬 번역 모드의 `Localization.txt`는 문자열 교체용이다. **PNG를 번역 모드 폴더에 넣는 것만으로 이미지가 덮어씌워진다는 증거는 없다.** 별도의 AssetBundle/Addressables 교체를 지원하는 로더가 있는지 먼저 조사해야 한다. 없으면 런타임 오버라이드/별도 이미지 패치 도입이 필요할 수 있다. 배포 전에 독립된 작업용 번들에서 참조 ID·Sprite 참조·스트리밍 데이터·카탈로그/해시/CRC·번들 의존성을 검증하고 수정본을 실게임에서 테스트해야 한다. 설치된 게임의 원본 번들을 직접 덮어쓰는 방식은 사용하지 않는다.

## 미확인 사항과 검수 기준

- **실제 게임 실행 및 인게임 이미지 표시를 확인하지 않았다.** 어떤 그림이 어느 이벤트/해상도/분기에서 나오는지, UI가 상위에 겹쳐지는지, 축소 시 글자가 읽히는지는 미검증이다.
- 조사 대상 635개 전부에 대해 자동 글자 인식이나 전체 시각 검수는 하지 않았다. **양성 사례는 실제 샘플에서 육안 확인**, 음성 사례는 표본에 한정한다.
- UI는 실제 게임에서 번역 텍스트가 나오는 위치를 확인하고, 이미지 후보는 최소 하나씩 **원본/수정 PNG 픽셀 비교 → 재직렬화 후 재추출 비교 → 수정 번들 로딩 및 실제 화면 비교** 순서로 검증한다.
- 고유명사와 농담은 기존 `translations`의 용어집 및 해당 이벤트 문맥에 맞춘다. `Walter Wisconsin`, `Cool Josh`, `Little Kenny`처럼 이미지와 대사에 동시에 등장할 수 있는 이름은 텍스트 번역과 함께 검수한다.

## 부록: Texture2D 전체 이름 인벤토리

아래는 조사 대상 **635개 텍스처의 모든 이름**이다. 같은 이름의 Sprite가 각 1개씩 존재한다. 각 해상도 소제목 아래 이름을 나열했으므로 반복되는 해상도 표기는 생략한다. 식별자만 기록하며, 샘플 이외의 텍스처에서 글자를 확인했다는 뜻은 아니다.

### gallery_assets_all.bundle (210)

**2048 x 1024 (45)**

- `sk_aamonster_aaravi_birb`, `sk_aamonster_aaravi_dragon`, `sk_aamonster_aaravi_fairy`, `sk_aamonster_aaravi_nightmare`, `sk_aamonster_aaravi_reaper`
- `sk_aamonster_aaravi_spider`, `sk_altpcs_altpc1`, `sk_altpcs_altpc2`, `sk_appli_appliance2`, `sk_babayaga_babayaga000`
- `sk_babayaga_babayaga4`, `sk_babayaga_babayaga6`, `sk_bartender_bartender1`, `sk_batniss_batniss5`, `sk_bees_damien_bee2`
- `sk_ceo_ceo_1`, `sk_ceo_ceocolors_1`, `sk_cpu_cpulysses2`, `sk_cpu_cpulysses3`, `sk_director_weaving4`
- `sk_director_weaving5`, `sk_director_weaving6`, `sk_flodge_flodge15`, `sk_flodge_flodge3`, `sk_flodge_flodge5`
- `sk_hex_aaravicurse1`, `sk_hex_aaravicurse6`, `sk_hex_aaravicurse7`, `sk_lifeguards_lifeguard_sketches_1`, `sk_lifeguards_lifeguard_sketches_2`
- `sk_lifeguards_lifeguard_sketches_3`, `sk_lifeguards_lifeguard_sketches_4`, `sk_lifeguards_lifeguards1`, `sk_lifeguards_lifeguards5`, `sk_milo_newro1`
- `sk_morty_morty2`, `sk_morty_morty5`, `sk_morty_morty7`, `sk_morty_morty9`, `sk_prologue_bus_ro1`
- `sk_prologue_bus_ro2`, `sk_prologue_bus_ro3`, `sk_prologue_bus_ro4`, `sk_prologue_bus_ro5`, `sk_prologue_bus_ro6`

**1920 x 1080 (37)**

- `credits_02`, `credits_03`, `credits_04`, `credits_05`, `credits_06`
- `credits_07`, `credits_08`, `credits_09`, `credits_10`, `credits_11`
- `credits_12`, `credits_13`, `credits_14`, `credits_15`, `credits_16`
- `credits_17`, `credits_18`, `credits_19`, `credits_20`, `credits_21`
- `credits_22`, `credits_23`, `credits_24`, `credits_25`, `credits_26`
- `credits_27`, `credits_28`, `credits_29`, `credits_30`, `credits_31`
- `credits_32`, `credits_33`, `credits_34`, `credits_35`, `credits_36`
- `credits_37`, `credits_38`

**1276 x 1076 (60)**

- `campfire_genericfailure`, `campfire_genericsuccess`, `galleryspecial_spst_dahlia`, `galleryspecial_spst_gregorian_chant`, `galleryspecial_spst_lofi`
- `galleryspecial_spst_mall_client`, `galleryspecial_spst_npc_antigambling`, `galleryspecial_spst_npc_bear`, `galleryspecial_spst_npc_bowl_of_salad`, `galleryspecial_spst_npc_chiyo`
- `galleryspecial_spst_npc_cigarette_spirit`, `galleryspecial_spst_npc_deep`, `galleryspecial_spst_npc_dominique`, `galleryspecial_spst_npc_future_damien`, `galleryspecial_spst_npc_gerd`
- `galleryspecial_spst_npc_invisible_entrepreneurs`, `galleryspecial_spst_npc_multidamien`, `galleryspecial_spst_npc_norah`, `galleryspecial_spst_npc_pizzaboyz`, `galleryspecial_spst_npc_sarth`
- `galleryspecial_spst_o_aaravi_armor`, `galleryspecial_spst_o_aaravi_yogaarmor`, `galleryspecial_spst_o_assmade`, `galleryspecial_spst_o_bear_book`, `galleryspecial_spst_o_bear_dmitri`
- `galleryspecial_spst_o_bear_flodge`, `galleryspecial_spst_o_bear_hex`, `galleryspecial_spst_o_bees`, `galleryspecial_spst_o_calcularry`, `galleryspecial_spst_o_chaz`
- `galleryspecial_spst_o_dahlia_bucket`, `galleryspecial_spst_o_dahlius`, `galleryspecial_spst_o_damien_noface`, `galleryspecial_spst_o_damien_paintedface`, `galleryspecial_spst_o_damien_pancake`
- `galleryspecial_spst_o_damien_swappedface`, `galleryspecial_spst_o_damien_upsidedown`, `galleryspecial_spst_o_evilscott`, `galleryspecial_spst_o_fancyhats`, `galleryspecial_spst_o_flodge_box`
- `galleryspecial_spst_o_flodge_bush`, `galleryspecial_spst_o_flodge_coach`, `galleryspecial_spst_o_flodge_dahlia`, `galleryspecial_spst_o_flodge_fan`, `galleryspecial_spst_o_flodge_hex`
- `galleryspecial_spst_o_flodge_lamp`, `galleryspecial_spst_o_lawyers`, `galleryspecial_spst_o_milo_banana`, `galleryspecial_spst_o_milo_catshirt`, `galleryspecial_spst_o_milo_nophone`
- `galleryspecial_spst_o_mustaches`, `galleryspecial_spst_o_pjs`, `galleryspecial_spst_o_prankmasterzghosts`, `galleryspecial_spst_o_scott_jello`, `galleryspecial_spst_o_scott_tree`
- `galleryspecial_spst_o_the_cat`, `galleryspecial_spst_o_turquoise`, `galleryspecial_spst_tavern`, `galleryspecial_spst_turnintoabear`, `galleryspecial_spst_wrong_baby`

**1024 x 1024 (63)**

- `sk_altpcs_altpc3green`, `sk_altpcs_altpc4green`, `sk_appli_appliance1`, `sk_appli_appliance3`, `sk_appli_appliance5`
- `sk_babayaga_babayaga1`, `sk_babayaga_babayaga2`, `sk_babayaga_babayaga3`, `sk_babayaga_babayaga5`, `sk_babayaga_babayaga7`
- `sk_bartender_bartender2`, `sk_batniss_batniss1`, `sk_batniss_batniss3`, `sk_batniss_batniss4`, `sk_bees_damien_bee1`
- `sk_ceo_ceo2`, `sk_chancellor_chancellor1`, `sk_chancellor_chancellor2`, `sk_chancellor_chancellor3`, `sk_coven_faith_summer_sketches`
- `sk_coven_faith_summer_sketches_1`, `sk_coven_hope_summer_sketches`, `sk_coven_hope_summer_sketches_1`, `sk_cpu_cpulysses`, `sk_director_weaving1`
- `sk_director_weaving2`, `sk_director_weaving3`, `sk_director_weaving7`, `sk_endings_success_caljoy`, `sk_endings_success_dok`
- `sk_endings_success_dok2`, `sk_endings_success_joy`, `sk_evilexes_ex1`, `sk_evilexes_ex2`, `sk_evilexes_ex3`
- `sk_flodge_flodge14`, `sk_flodge_flodge6`, `sk_flodge_flodge7`, `sk_flodge_flodge8`, `sk_hex_aaravicurse2`
- `sk_hex_aaravicurse3`, `sk_jerry_jerry1`, `sk_jerry_jerry2`, `sk_jerry_jerry3`, `sk_lifeguards_lifeguards`
- `sk_lifeguards_lifeguards0`, `sk_lifeguards_lifeguards2`, `sk_lifeguards_lifeguards4`, `sk_lifeguards_lifeguards6`, `sk_milo_newro2`
- `sk_milo_newro3`, `sk_morty_morty1`, `sk_morty_morty3`, `sk_morty_morty4`, `sk_morty_morty8`
- `sk_othechars_deer2`, `sk_othechars_goddess`, `sk_pizzagirl_npc_pizza_girl2`, `sk_pizzagirl_pizza1`, `sk_pizzagirl_pizza3`
- `sk_pizzagirl_pizza4`, `sk_secretendings_dahliaanime12`, `sk_secretendings_damien_sketches`

**760 x 1080 (1)**

- `galleryspecial_npc_tree`

**512 x 1024 (2)**

- `sk_babayaga_babayaga00`, `sk_jerry_jerry4`

**1024 x 512 (1)**

- `sk_appli_appliance4`

**4 x 4 (1)**

- `TransparentPixel`

### backgrounds_assets_all.bundle (109)

**1276 x 1076 (109)**

- `background_antmiami1`, `background_antmiami2`, `background_antmiami3`, `background_antmiami4`, `background_antmiami5`
- `background_antmiami6`, `background_antmiami7`, `background_antmiami8`, `background_antmiami9`, `background_antreligion1`
- `background_antreligion2`, `background_antreligion3`, `background_antreligion4`, `background_antreligion5`, `background_antreligion6`
- `background_antreligion7`, `background_antreligion8`, `background_antspace1`, `background_antspace2`, `background_antspace3`
- `background_antspace4`, `background_antspace5`, `background_antspace6`, `background_bear`, `background_buffducks`
- `background_cactusmovie`, `background_campfire`, `background_campfire_classical`, `background_dahlia_farmer`, `background_dahlia_taxes`
- `background_dahlia_water`, `background_dahliacosplay`, `background_dahliarival_coolending`, `background_dahliarival_defeat`, `background_dahliarival_finalpunch`
- `background_dahliarival_handinshoulder`, `background_dahliarival_milocat`, `background_dahliarival_offeringhand`, `background_dahliarival_setokaiba`, `background_dahliarival_vikingshake`
- `background_damiensigil`, `background_dmitrimorty_alpaca`, `background_dmitrimorty_jelly`, `background_dmitrimorty_paper`, `background_dmitrimorty_scott`
- `background_dome`, `background_dome_classical`, `background_encryptedcode`, `background_failure`, `background_fishteeth`
- `background_genericbright`, `background_genericdark`, `background_goddess`, `background_heartbrokenpost`, `background_helltaverninnkeeper`
- `background_helltavernwanderer`, `background_horsebets`, `background_interdimensional`, `background_knifebook`, `background_lake`
- `background_lake_classical`, `background_lakeaaravi`, `background_lakescott`, `background_lakesiren`, `background_lakesiren2`
- `background_lastwill`, `background_manor`, `background_manor_classical`, `background_milo_friend`, `background_murderdiary`
- `background_normal`, `background_pigclouds`, `background_plantprom`, `background_scouthq`, `background_scouthq_classical`
- `background_secretending_aaraviamends`, `background_secretending_aaraviorhex_a`, `background_secretending_aaraviorhex_ah`, `background_secretending_aaraviorhex_h`, `background_secretending_appliances`
- `background_secretending_calfatherhood_extra_s1s1s1`, `background_secretending_calfatherhood_extra_s1s1s2`, `background_secretending_calfatherhood_extra_s1s2s1`, `background_secretending_calfatherhood_extra_s1s2s2`, `background_secretending_calfatherhood_extra_s2s1s1`
- `background_secretending_calfatherhood_extra_s2s1s2`, `background_secretending_calfatherhood_extra_s2s2s1`, `background_secretending_calfatherhood_extra_s2s2s2`, `background_secretending_calgrim`, `background_secretending_caluprising`
- `background_secretending_dahliarival`, `background_secretending_dahliasummer`, `background_secretending_damiendads`, `background_secretending_damienfire`, `background_secretending_dmitri`
- `background_secretending_joycoven`, `background_secretending_joyex`, `background_secretending_milocat`, `background_secretending_miloyolo`, `background_spellpage`
- `background_success`, `background_turnip`, `background_woods`, `background_woods_classical`, `background_zgordstory0`
- `background_zgordstory1`, `background_zgordstory2`, `background_zgordstory3`, `background_zgordstory4`

### metashop_assets_all.bundle (16)

**600 x 600 (1)**

- `metashop_op_hal`

**256 x 256 (15)**

- `metashop_drinkschoice_fg`, `metashop_drinksmode_choice`, `metashop_manualbase`, `metashop_manualros`, `metashop_manualstats`
- `metashop_op_cat`, `metashop_op_cir`, `metashop_op_eig`, `metashop_op_fai`, `metashop_op_maz`
- `metashop_op_nau`, `metashop_op_wil`, `metashop_pcp_fri`, `metashop_pcp_mod`, `metashop_sketch`

### drinks_assets_all.bundle (135)

**380 x 380 (132)**

- `abblood`, `abblood_grounded`, `aglassofcurse`, `aglassofcurse_grounded`, `allbrians`
- `allbrians_grounded`, `aveverage`, `aveverage_grounded`, `blendersmoothie`, `blendersmoothie_grounded`
- `bloodymary`, `bloodymary_grounded`, `bonehurtingjuice`, `bonehurtingjuice_grounded`, `casketwine`
- `casketwine_grounded`, `cofibeatstorelaxstudyto`, `cofibeatstorelaxstudyto_grounded`, `communitypunch`, `communitypunch_grounded`
- `cosmopolitan`, `cosmopolitan_grounded`, `cursedbearew`, `cursedbearew_grounded`, `darknstormy`
- `darknstormy_grounded`, `doomperignon`, `doomperignon_grounded`, `dumpsterfire`, `dumpsterfire_grounded`
- `ectoplasm`, `ectoplasm_grounded`, `fake_encryptedcode`, `fake_heartbrokenpost`, `fake_horsebets`
- `fake_lastwill`, `fake_murderdiary`, `fake_spellpage`, `fantasyale`, `fantasyale_grounded`
- `flaskgenie`, `flaskgenie_grounded`, `gamergirlbathwater`, `gamergirlbathwater_grounded`, `hexoland`
- `hexoland_grounded`, `holywater`, `holywater_grounded`, `hotshot`, `hotshot_grounded`
- `imaginationshots`, `imaginationshots_grounded`, `joecrow`, `joecrow_grounded`, `lovepotionno9`
- `lovepotionno9_grounded`, `lowcostenergydrink`, `lowcostenergydrink_grounded`, `loyaltylemonade`, `loyaltylemonade_grounded`
- `maaargherita`, `maaargherita_grounded`, `manhattan`, `manhattan_grounded`, `molotovcocktail`
- `molotovcocktail_grounded`, `moskito`, `moskito_grounded`, `notthebees`, `notthebees_grounded`
- `oldchumschampagne`, `oldchumschampagne_grounded`, `pairofbeerboots`, `pairofbeerboots_grounded`, `phobiashots`
- `phobiashots_grounded`, `pinaskullada`, `pinaskullada_grounded`, `pizza`, `pizza_grounded`
- `poison`, `poison_grounded`, `proteinshake`, `proteinshake_grounded`, `sacredblood`
- `sacredblood_grounded`, `sakebomb`, `sakebomb_grounded`, `sangria`, `sangria_grounded`
- `screwdriver`, `screwdriver_grounded`, `sexonthebeach`, `sexonthebeach_grounded`, `skimask`
- `skimask_grounded`, `spellshake`, `spellshake_grounded`, `spirits`, `spirits_grounded`
- `statsmoothie`, `statsmoothie_grounded`, `tequilamoonrise`, `tequilamoonrise_grounded`, `thebargain`
- `thebargain_grounded`, `thebest`, `thebest_grounded`, `theclassicalpalette`, `theclassicalpalette_grounded`
- `thecooldude`, `thecooldude_grounded`, `thedarkesttimeline`, `thedarkesttimeline_grounded`, `thedoublegift`
- `thedoublegift_grounded`, `theequalizer`, `theequalizer_grounded`, `thefoulmouth`, `thefoulmouth_grounded`
- `thefullmoon`, `thefullmoon_grounded`, `theredacted`, `theredacted_grounded`, `theroyale`
- `theroyale_grounded`, `thespook`, `thespook_grounded`, `toiletwine`, `toiletwine_grounded`
- `whiskey`, `whiskey_grounded`

**256 x 256 (3)**

- `average_icon`, `nothinghappened_icon`, `plotline_icon`

### charactericons_assets_all.bundle (60)

**512 x 512 (20)**

- `icon_character_altblue_border`, `icon_character_altgreen_border`, `icon_character_altred_border`, `icon_character_altyellow_border`, `icon_character_bear_border`
- `icon_character_blue_border`, `icon_character_doug_border`, `icon_character_fridge_border`, `icon_character_green_border`, `icon_character_jacqueline_border`
- `icon_character_ksblue_border`, `icon_character_ksgreen_border`, `icon_character_ksred_border`, `icon_character_ksyellow_border`, `icon_character_mamimi_border`
- `icon_character_modeus_border`, `icon_character_red_border`, `icon_character_whiskey_border`, `icon_character_yellow_border`, `icon_character_zoe_border`

**256 x 256 (40)**

- `icon_character_altblue`, `icon_character_altblue_outline`, `icon_character_altgreen`, `icon_character_altgreen_outline`, `icon_character_altred`
- `icon_character_altred_outline`, `icon_character_altyellow`, `icon_character_altyellow_outline`, `icon_character_bear`, `icon_character_bear_outline`
- `icon_character_blue`, `icon_character_blue_outline`, `icon_character_doug`, `icon_character_doug_outline`, `icon_character_fridge`
- `icon_character_fridge_outline`, `icon_character_green`, `icon_character_green_outline`, `icon_character_jacqueline`, `icon_character_jacqueline_outline`
- `icon_character_ksblue`, `icon_character_ksblue_outline`, `icon_character_ksgreen`, `icon_character_ksgreen_outline`, `icon_character_ksred`
- `icon_character_ksred_outline`, `icon_character_ksyellow`, `icon_character_ksyellow_outline`, `icon_character_mamimi`, `icon_character_mamimi_outline`
- `icon_character_modeus`, `icon_character_modeus_outline`, `icon_character_red`, `icon_character_red_outline`, `icon_character_whiskey`
- `icon_character_whiskey_outline`, `icon_character_yellow`, `icon_character_yellow_outline`, `icon_character_zoe`, `icon_character_zoe_outline`

### npcicons_assets_all.bundle (105)

**256 x 256 (102)**

- `icon_npc_aaravi`, `icon_npc_aaravi_opmosterporm`, `icon_npc_aaravi_outline`, `icon_npc_aaraviappliance`, `icon_npc_aaravihex`
- `icon_npc_aaravihex_outline`, `icon_npc_aaravihexappliance`, `icon_npc_antigambling`, `icon_npc_axarax`, `icon_npc_babayaga`
- `icon_npc_bartender`, `icon_npc_batniss`, `icon_npc_bear`, `icon_npc_calculester`, `icon_npc_calculester_opmosterporm`
- `icon_npc_calculester_outline`, `icon_npc_calculesterappliance`, `icon_npc_calculesterjr`, `icon_npc_chancellor`, `icon_npc_chiyo`
- `icon_npc_cigarettespirit`, `icon_npc_coach`, `icon_npc_cooljosh`, `icon_npc_dahlia`, `icon_npc_dahlia_opmosterporm`
- `icon_npc_dahlia_outline`, `icon_npc_dahliaappliance`, `icon_npc_damien`, `icon_npc_damien_opmosterporm`, `icon_npc_damien_outline`
- `icon_npc_damienappliance`, `icon_npc_deep`, `icon_npc_director`, `icon_npc_dmitri`, `icon_npc_dominique`
- `icon_npc_evilceo`, `icon_npc_evilfaith`, `icon_npc_eviljoy`, `icon_npc_evilscott`, `icon_npc_faith`
- `icon_npc_fellowstudent`, `icon_npc_fellowstudentcop`, `icon_npc_flodge`, `icon_npc_flodge_bush`, `icon_npc_flodge_coach`
- `icon_npc_flodge_dahlia`, `icon_npc_flodge_fankid`, `icon_npc_flodge_hex`, `icon_npc_flodge_lamp`, `icon_npc_futuredamien`
- `icon_npc_gchupacabra`, `icon_npc_gdeer`, `icon_npc_gerard`, `icon_npc_geyes`, `icon_npc_glich`
- `icon_npc_goddess`, `icon_npc_gplant`, `icon_npc_hex`, `icon_npc_hex_opmosterporm`, `icon_npc_hex_outline`
- `icon_npc_hexagon`, `icon_npc_hexappliance`, `icon_npc_hope`, `icon_npc_innkeeper`, `icon_npc_jerry`
- `icon_npc_joy`, `icon_npc_joy_opmosterporm`, `icon_npc_joy_outline`, `icon_npc_joyappliance`, `icon_npc_juan`
- `icon_npc_liam`, `icon_npc_lifeguards`, `icon_npc_lucien`, `icon_npc_milo`, `icon_npc_milo_opmosterporm`
- `icon_npc_milo_outline`, `icon_npc_miloappliance`, `icon_npc_morty`, `icon_npc_mothman`, `icon_npc_mothman_outline`
- `icon_npc_multidamien`, `icon_npc_narrator`, `icon_npc_narratorbody`, `icon_npc_norah`, `icon_npc_notscott`
- `icon_npc_pizzagirl`, `icon_npc_pizzajoy`, `icon_npc_pizzamilo`, `icon_npc_polly`, `icon_npc_prince`
- `icon_npc_robotcommander`, `icon_npc_salad`, `icon_npc_salil`, `icon_npc_salome`, `icon_npc_sarth`
- `icon_npc_scott`, `icon_npc_shopkeeper`, `icon_npc_stan`, `icon_npc_stu`, `icon_npc_tree`
- `icon_npc_wanda`, `icon_npc_wanderer`

**16 x 16 (3)**

- `icon_npc_invisible1`, `icon_npc_invisible2`, `icon_npc_invisible3`
