# Silbot Portfolio · assets

이 폴더에 사진·영상 파일을 넣으면 [`../index.html`](../index.html) 의 placeholder 가 자동으로 자리를 잡습니다.
파일을 추가한 뒤에는 해당 placeholder `<div>` 를 `<img>` / `<video>` 로 교체해 주세요.

## 권장 파일 목록

### 필수 (placeholder 가 페이지에 보임)
| 파일명 | 용도 | 권장 해상도 |
|---|---|---|
| `hero_classroom.jpg` | Hero 섹션 (실벗 + 학생 태블릿 + 교사 PC) | 1920×1200 가로 |
| `game_match3.jpg` | 3-11 Match3 인게임 캡처 | 1280×720 |
| `game_match5_06.jpg` | 5-06 Match 인게임 캡처 | 1280×720 |
| `game_star.jpg` | 5-07 Star 인게임 캡처 | 1280×720 |
| `feature_speech_window.jpg` | 행사용 발화 창 UI 캡처 (Highlights #07) | 1280×800 |

### 선택 (있으면 좋음)
| 파일명 | 용도 | 권장 |
|---|---|---|
| `play_match3.mp4` | Match3 플레이 영상 | 30s, 음소거 |
| `play_match5_06.mp4` | Match 플레이 영상 | 30s, 음소거 |
| `play_star.mp4` | Star 플레이 영상 | 30s, 음소거 |
| `clip_match3_chain.mp4` | 연쇄 매치 클립 | 8~15s |
| `clip_match_combo.mp4` | 콤보 공격 클립 | 8~15s |
| `clip_star_hint.mp4` | 힌트 시스템 클립 | 8~15s |
| `robot_silbot.jpg` | 실벗 본체 사진 | 1:1 또는 4:5 |
| `robot_hibomi.jpg` | HiBomi2 보조 로봇 | 1:1 또는 4:5 |
| `face_joy.png` 등 | 실벗 표정 갤러리 | 600×600 |
| `architecture.png` | 시스템 다이어그램 | 자유 |
| `logo.png` / `logo.svg` | 좌상단 로고 (현재 "실" 텍스트) | 정사각형 |

## 임베드 예시

```html
<!-- 이미지 -->
<img src="assets/game_match3.jpg" alt="3-11 Match3 게임 화면" />

<!-- 영상 (자동재생/음소거/루프) -->
<video src="assets/play_match3.mp4" autoplay muted loop playsinline></video>
```

## 영상 가이드라인

- **자동재생 정책**: 브라우저가 자동재생을 허용하려면 `muted` 필수.
  소리 있는 데모는 별도 컨트롤(`controls`) 붙여서 사용자가 클릭해서 재생.
- **길이**: 30초 안팎이 가장 보기 좋음. 너무 길면 페이지 로드가 느려짐.
- **포맷**: `.mp4` (H.264) 권장. 가능하면 720p, 1Mbps 이하로 압축.
- **크기**: 가능한 한 5MB 이하로 유지. 큰 영상은 YouTube 임베드 추천.

## 사진 가이드라인

- 게임 캡처는 **UI 가 잘 보이는 한 순간**을 고르기 — 인트로/결과 화면 좋음.
- 교실 장면은 **사람 얼굴이 식별되지 않게** 크롭 또는 후면 컷.
- 표정 캡처는 같은 배경/같은 크기로 통일하면 갤러리가 정돈됨.
