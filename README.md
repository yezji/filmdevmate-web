# web — GitHub Pages 정적 사이트

빌드 단계가 없다. 올라가는 건 HTML·CSS·이미지뿐이고, `gen.py` 는 배포에 끼지
않는다(ko/ja 문안이 한 곳에서 관리되도록 만든 생성기이고, 결과물도 커밋한다).

프레임워크를 안 쓴 건 취향이 아니라 목적이다. 답변 엔진 크롤러는 자바스크립트로
그린 내용을 못 보거나 늦게 본다. 본문은 전부 HTML 안에 있다. 유일한 JS 인 희석
계산기는 보조라, 꺼져 있어도 표와 본문으로 답이 읽힌다.

## 배포

1. GitHub 에 `filmdevmate` 레포를 새로 만든다(공개).
2. 이 폴더 내용을 루트에 넣고 푸시한다. `gen.py`·`content_*.py`·`build_i18n.py` 는
   올려도 서빙에 영향이 없다(원하면 빼도 된다).
3. Settings → Pages → Source 를 `main` 브랜치 `/ (root)` 로 둔다.
4. `https://yezji.github.io/filmdevmate-web/` 로 뜬다.

주소가 달라지면 고쳐야 하는 곳: 각 페이지의 `canonical`·`hreflang`,
`sitemap.xml`, `robots.txt` 의 Sitemap 줄, `llms.txt` 의 링크, `build_i18n.py` 의 `BASE`.

## 구조

    index.html          랜딩 (SoftwareApplication + FAQPage)
    dilution/           희석 계산 (HowTo + FAQPage, 계산기 포함)
    temperature/        온도가 어긋났을 때 (FAQPage)
    steps/              공정 순서 (HowTo + FAQPage)
    ko/ · ja/           같은 네 면. 번역이 아니라 그 언어로 묻는 방식에 맞춰 다시 씀
    style.css           공용. 다크 단일 테마, 앰버 한 색, 라운드 16px 한 단계
    img/                실제 앱 스크린샷 3장 (가짜 목업 아님)
    llms.txt · robots.txt · sitemap.xml

`ko/` `ja/` 를 고칠 때는 `content_ko.py` / `content_ja.py` 를 고치고
`python3 gen.py` 를 돌린다. 영어(루트)는 손으로 쓴 원본이라 생성기가 건드리지 않는다.

## 규칙

- **레시피 데이터를 싣지 않는다.** 이유는 `docs/aeo.md`.
- **숫자를 지어내지 않는다.** 희석 표는 계산해서 검산했고, 평점처럼 실제 값이 없는
  항목은 구조화 데이터에 넣지 않는다.
- **em dash 를 쓰지 않는다.** 전 언어 0개를 유지한다. 가운뎃점(·)은 한국어·일본어의
  정식 나열 부호라 그쪽에만 남긴다.
- 방법 글은 앱 없이도 답이 되게 쓴다. 광고문이면 인용되지 않는다.
- **스토어 버튼은 각 플랫폼의 공식 배지를 그대로 쓴다.** `img/badge-appstore.svg`(Apple),
  `img/badge-play.png`(Google). 색·모서리·문구를 바꾸면 양쪽 브랜드 가이드 위반이다.
  높이만 맞추고 폭은 비율대로 둔다.
- **모션은 CSS scroll-driven animation 뿐이다.** JS 가 없어서 정적 호스팅에서 그대로
  돌고, 크롤러는 본문을 그대로 읽는다. 미지원 브라우저에서는 아무 일도 안 일어나고
  그냥 보인다. prefers-reduced-motion 에서는 전부 꺼진다.
