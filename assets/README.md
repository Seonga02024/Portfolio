# Portfolio root · assets

메인 랜딩 페이지([`../index.html`](../index.html))의 이미지 자원입니다.

## 권장 파일 목록

| 파일명 | 용도 | 권장 해상도 |
|---|---|---|
| `profile.jpg` | Hero 프로필 사진 (4:5 권장) | 800×1000 이상 |
| `feat_silbot.jpg` | 실벗 대표 이미지 | 1280×720 |
| `feat_cbf.jpg` | 케어 브레인 핏 대표 이미지 | 1280×720 |
| `feat_gostop.jpg` | 로보맞고 대표 이미지 | 1280×720 |
| `feat_robocare.jpg` | 로보케어 통합 페이지 대표 이미지 | 1280×720 |

## 교체 예시

placeholder:
```html
<div class="profile-photo">
  <div class="placeholder">
    <strong>PROFILE PHOTO</strong>
    assets/profile.jpg<br/>
    (4:5 권장, 정면 컷)
  </div>
  <div class="badge">...</div>
</div>
```

이미지 추가 후:
```html
<div class="profile-photo">
  <img src="assets/profile.jpg" alt="박성아 프로필 사진" />
  <div class="badge">...</div>
</div>
```

## 폴더 구조

```
Portfolio/
├── index.html              ← 메인 랜딩 (지금 이 페이지)
├── assets/                 ← 이 폴더
│   ├── profile.jpg
│   ├── feat_silbot.jpg
│   ├── feat_cbf.jpg
│   ├── feat_gostop.jpg
│   └── feat_robocare.jpg
├── silbot/                 ← 실벗 상세 페이지
├── carebrainfit/           ← 케어 브레인 핏 상세 페이지
├── gostop/                 ← 로보맞고 상세 페이지
└── robocare/               ← 로보케어 통합 정리
```

## 보안 / 개인정보

메인 페이지의 Contact 섹션에는 다음 개인정보가 포함되어 있습니다:
- 📱 전화번호: +82 10-7525-5014
- ✉️ 이메일: psa20708@naver.com
- 🏠 거주지: 경기도 기흥구

해당 정보는 Notion 원본 페이지에서 그대로 가져온 것입니다. 공개 웹에 노출하지 않으려면
[`../index.html`](../index.html) 의 `<!-- =================== CONTACT ===================  -->`
섹션에서 해당 카드를 제거해 주세요.
