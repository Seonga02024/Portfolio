# Robocare Portfolio · assets

이 폴더에 사진 파일을 넣으면 [`../index.html`](../index.html) 의 placeholder 가 자동으로 자리를 잡습니다.
파일을 추가한 뒤에는 해당 placeholder `<div>` 를 `<img src="assets/파일명">` 으로 교체해 주세요.

## 콘텐츠별 사진 (각 2장)

| 콘텐츠 | 파일명 | 비고 |
|---|---|---|
| Hero | `hero_kemi.jpg` | 케미프렌즈 앱 메인 / 재미 공간 진입 화면 (1080×1920 세로 권장) |
| 01 인지게임 | `cognitive_1.jpg`, `cognitive_2.jpg` | 10종 중 대표 2종 / 메인 화면 + 플레이 화면 |
| 02 오목게임 | `omok_1.jpg`, `omok_2.jpg` | 게임판 + 봄파고 아바타가 보이는 컷 |
| 03 리듬게임 | `rhythm_1.jpg`, `rhythm_2.jpg` | 손 인식 화면 + 음표 진행 화면 |
| 04 핀볼게임 | `pinball_1.jpg`, `pinball_2.jpg` | 보스 화면 + 일반 플레이 화면 |
| 05 맞고게임 | `matgo_1.jpg`, `matgo_2.jpg` | 대국 화면 + 프로필/랭킹 화면 |
| 06 신체활동게임 | `carebrainfit_1.jpg`, `carebrainfit_2.jpg` | 체조 모드 + 아케이드 모드 |
| 07 실벗 | `silbot_1.jpg`, `silbot_2.jpg` | 학생 태블릿 화면 + 교사 PC/로봇 |

## 권장 사항

- **비율**: 카드 안 이미지 슬롯이 `aspect-ratio: 4/5` 이므로 **세로형(4:5) 사진**이 가장 잘 맞습니다.
  가로형 사진을 넣어도 `object-fit: cover` 로 잘려서 표시됩니다.
- **해상도**: 800×1000 이상이면 충분합니다. 1200×1500 권장.
- **포맷**: `.jpg` (사진), `.png` (UI 캡처/로고).
- **용량**: 한 장 200KB ~ 500KB 정도로 압축하면 페이지 로딩이 쾌적합니다.
- **선택 기준**:
  - 1장은 **타이틀/대표 비주얼** (콘텐츠가 한눈에 식별되는 컷)
  - 1장은 **인게임/플레이 중 컷** (실제 상호작용이 드러나는 컷)

## 교체 예시

placeholder:
```html
<div class="img-slot">
  <div><strong>대표 화면 ①</strong>assets/omok_1.jpg</div>
</div>
```

이미지 추가 후:
```html
<div class="img-slot">
  <img src="assets/omok_1.jpg" alt="봄파고와 오목대결 메인 화면" />
</div>
```

## 링크되는 기존 포트폴리오

| 콘텐츠 | 링크된 페이지 |
|---|---|
| 05 맞고게임 (로보맞고) | [`../gostop/index.html`](../../gostop/index.html) |
| 06 신체활동게임 (케어 브레인 핏) | [`../carebrainfit/index.html`](../../carebrainfit/index.html) |
| 07 실벗 | [`../silbot/index.html`](../../silbot/index.html) |

나머지 4종(인지·오목·리듬·핀볼)은 현재 "상세 페이지 준비 중" 상태입니다. 추후 페이지가 생기면
`open-link disabled` 클래스를 `open-link` 로 바꾸고 `href` 를 채워 주세요.
