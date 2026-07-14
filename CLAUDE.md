# 자취생 연구소 운영 매뉴얼

이 저장소는 `laykim829` 계정이 운영하는 7개 콘텐츠/제휴마케팅 사이트 포트폴리오 중 하나입니다.
라이브 URL: https://laykim829.github.io/solo-living-lab/

## 포트폴리오 전체 목록 (자매 사이트)

| repo | 사이트명 | 주제 |
|---|---|---|
| ai-side-hustle-site | AI 부업 연구소 | AI 부업 정보 |
| pet-life-lab | 펫생활 연구소 | 반려동물 |
| home-fit-lab | 홈트 연구소 | 홈트레이닝 용품 |
| camping-life-lab | 캠핑라이프 연구소 | 캠핑용품 |
| baby-life-lab | 베이비 라이프 연구소 | 육아용품 |
| solo-living-lab | 자취생 연구소 | 원룸/자취 인테리어 |
| money-habit-lab | 재테크 습관 연구소 | 재테크/저축 습관 |

7개 사이트 모두 같은 템플릿 구조를 공유합니다. 한 사이트에서 구조적 변경(예: footer, 광고 스니펫)을 하면 나머지 6개에도 동일하게 적용해야 일관성이 유지됩니다.

## 배포

- GitHub Actions(`.github/workflows/*.yml`)가 `main` 브랜치 push 시 자동으로 GitHub Pages에 배포합니다. 빌드 스텝 없음 (정적 파일 그대로 배포).
- **push하는 순간 라이브 사이트가 바뀝니다.** 커밋 전 diff를 반드시 확인할 것.

## 파일 구조

```
index.html      홈페이지 (랭킹 섹션 + 블로그 카드 목록)
about.html      사이트 소개
privacy.html    개인정보처리방침
posts.json      전체 포스트 메타데이터 (홈페이지가 이 파일을 fetch해서 블로그 카드를 렌더링)
posts/*.html    개별 포스트 (정적 HTML, 완전한 SEO 메타 포함)
sitemap.xml     검색엔진 제출용 (scripts/regen_sitemap.py로 자동 생성)
robots.txt      Sitemap 경로 명시
scripts/regen_sitemap.py   posts.json 기준으로 sitemap.xml 재생성 (lastmod 포함)
```

## 신규 포스트 발행 체크리스트

1. `posts/<slug>.html` 생성 — 기존 포스트를 템플릿으로 복사해서 사용 (SEO 메타, canonical, OG/Twitter 태그, 히어로 이미지, 광고 블록 전부 포함되어 있음)
2. `posts.json`에 항목 추가: `{"title", "category", "summary", "date": "YYYY-MM-DD", "url": "posts/<slug>.html"}` — **이 파일에 추가 안 하면 홈페이지 블로그 목록에 안 뜨고, sitemap에도 안 잡힘**
3. `python3 scripts/regen_sitemap.py` 실행해서 sitemap.xml 재생성 (수동으로 sitemap.xml 편집하지 말 것 — 스크립트가 posts.json과 항상 동기화되도록 보장함)
4. 발행 직후 `posts/`, `posts.json` 파일 개수가 서로 일치하는지 확인 (2026-07-14 세션에서 pet-life-lab·ai-side-hustle-site가 여기서 어긋나 포스트가 검색엔진에서 누락된 적 있음)

## 수익화 스택

### Google AdSense
- Publisher ID: `ca-pub-6162930467504910` (7개 사이트 공통)
- **모든 페이지의 `<head>`에 로더 스크립트 + 자동광고(auto ads) 활성화 스니펫이 반드시 함께 있어야 함**:
  ```html
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6162930467504910" crossorigin="anonymous"></script>
  <script>
    (adsbygoogle = window.adsbygoogle || []).push({
      google_ad_client: "ca-pub-6162930467504910",
      enable_page_level_ads: true
    });
  </script>
  ```
  로더 스크립트만 있고 이 push 호출이 없으면 승인이 나도 광고가 절대 안 뜸 (2026-07-14 세션에서 7개 사이트 전체가 이 상태였던 걸 발견해서 일괄 수정함).

### Kakao AdFit
- 이 사이트의 광고 유닛 ID: 데스크톱 `DAN-jqqgWFwVCw9IiAFW` / 모바일 `DAN-2bGjgB9usH9vjlPM`
- 홈페이지 + 모든 포스트에 데스크톱/모바일 반응형으로 삽입되어 있음 (`kas/static/ba.min.js`)

### 쿠팡파트너스
- 트래킹 코드: `AF3401189` (공통)
- 방식 두 가지 혼용 중:
  1. **상품별 딥링크** (`link.coupang.com/a/...`): 랭킹 카드나 포스트 "추천 상품" 박스에서 특정 상품을 가리킬 때. 딥링크는 쿠팡파트너스 대시보드(로그인 필요)에서 개별 생성해야 함 — 코드만으로는 만들 수 없음.
  2. **범용 캐러셀 위젯** (`ads-partners.coupang.com/g.js`, `id:1003711`(데스크톱)/`1003715`(모바일)): 특정 상품 딥링크가 없을 때 쓰는 대체재. 홈페이지에 이미 쓰이고 있는 걸 그대로 재사용하면 됨.
  - **주의**: "추천 상품" 박스(`ad-box`)에 고지 문구만 있고 실제 링크/위젯이 비어있는 경우가 있었음(2026-07-14, pet-life-lab 2개 포스트) — 새 포스트 발행 시 반드시 실제 링크가 채워졌는지 확인할 것.

### 애드픽 (Adpick)
- 랭킹 섹션(`TOP 8`, `.tool-card`)의 `bitl.bz/...` 단축링크. 애드픽은 여러 제휴사(쿠팡, 알리익스프레스 등)를 중개하는 CPA 네트워크라 리다이렉트 최종 목적지가 쿠팡이 아닐 수 있음 — **정상 동작**이며 버그 아님.
- 신규 랭킹 상품 소싱은 애드픽 로그인 세션(브라우저)이 필요해서 코드 작업만으론 불가.

### 고지 문구 표준
```html
<div class="disclosure">
※ 본 사이트의 일부 링크는 제휴 마케팅 링크이며, 이를 통해 발생한 구매에 대해 사이트 운영자가 소정의 수수료를 받을 수 있습니다.
또한 본 사이트는 광고 게재를 통해 수익을 창출할 수 있습니다. 실제 구매 전 각 제품의 최신 정보를 공식 판매처에서 확인하시기 바랍니다.
</div>
```

## Footer 자매사이트 크로스링크

모든 사이트 footer에 나머지 6개 사이트로 가는 링크가 있어야 함 (SEO 내부링크 신호 + 트래픽 교차 유입). 누락되면 내부링크 점검 시 바로 티가 남 — 새 사이트를 포트폴리오에 추가하면 **7개 전체** footer를 갱신해야 함.

## 알려진 이슈 / 주의사항 (2026-07-14 세션 기록)

- `money-habit-lab`의 "추천 금융앱 TOP8"은 제휴 트래킹이 없는 순수 정보성 링크임 (토스/뱅크샐러드 등 공식 사이트 직결). 금융앱은 쿠팡파트너스식 이커머스 제휴가 안 통하고 각 앱 자체 제휴 프로그램이나 CPA 네트워크 가입이 필요 — 미해결 상태.
- 뉴스레터 구독 폼은 데모用이며 실제 발송 연동이 안 되어 있음 (JS 메시지에 "데모용" 명시).
- 홈페이지 블로그 카드 목록은 `posts.json`을 클라이언트사이드 JS fetch로 그리는 구조라, JS 미실행 크롤러에는 안 보일 수 있음. 개별 포스트 페이지 자체는 완전한 정적 HTML이라 검색엔진 색인에는 문제없음.
