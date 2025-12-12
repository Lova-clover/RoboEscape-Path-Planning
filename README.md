<div align="center">

# 🤖 RoboEscape: Algorithm Hunters

### *7가지 경로 계획 알고리즘이 당신을 추격한다*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5.0-green?logo=pygame)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success)]()

**로봇공학의 Path-Planning 알고리즘들이 적 AI로 살아 움직이는 교육용 액션 게임**

[🎮 빠른 시작](#-빠른-시작) • [📚 알고리즘 소개](#-구현된-알고리즘) • [🎯 게임플레이](#-게임플레이) • [📖 문서](#-문서)

---

![Main Menu](images/main.png)

</div>

## 🌟 프로젝트 하이라이트

<div align="center">

### *단순한 게임을 넘어 살아있는 알고리즘 교과서*

</div>

| 특징 | 설명 |
|------|------|
| 🎓 **학습 가치** | Bug/APF/PRM/RRT/Belief 등 7가지 실전 알고리즘 체험 |
| 🧩 **전략성** | 각 알고리즘의 약점(Local Minimum, Noise Sensitivity)을 활용한 플레이 |
| 🎨 **가시성** | PRM 로드맵, RRT 트리, Belief 확률 분포를 실시간 시각화 |
| 🎪 **완성도** | 사이버펑크 메인 메뉴, 6개 스테이지 + 보스전, 파티클 효과, 사운드 |
| ⚡ **난이도** | 점진적 학습 곡선: 튜토리얼 → 보스전 → 무한 모드 |

<div align="center">

> 💡 **왜 특별한가?**  
> 대부분의 교육용 게임은 알고리즘을 "보여주기만" 합니다.  
> 이 게임은 알고리즘과 **상호작용**하고, 그들의 **강점과 약점을 체감**하게 만듭니다.

</div>

## 🧠 구현된 알고리즘

<div align="center">

### *7가지 Path-Planning 알고리즘이 살아 움직입니다*

</div>

### 🐛 Bug Algorithms (기초 반응형 추적)
<sup>실제 로봇이 센서만으로 장애물을 피하는 방식</sup>

<table>
<tr>
<th width="20%">알고리즘</th>
<th width="35%">동작 원리</th>
<th width="25%">시각적 특징</th>
<th width="20%">약점</th>
</tr>
<tr>
<td align="center"><b>Bug1</b></td>
<td>장애물을 완전히 한 바퀴 돌며<br/>최단 이탈점 찾기</td>
<td align="center">🔴 빨간색<br/>벽 따라 회전</td>
<td>복잡한 장애물에서<br/>비효율적</td>
</tr>
<tr>
<td align="center"><b>Bug2</b></td>
<td>M-line 기반<br/>직선 복귀 전략</td>
<td align="center">🟠 주황색<br/>직진 시도</td>
<td>좁은 통로에서<br/>헤맴</td>
</tr>
<tr>
<td align="center"><b>Tangent Bug</b></td>
<td>시야 기반<br/>접선 방향 선택</td>
<td align="center">🟡 노란색<br/>스마트한 회피</td>
<td>시야 제한<br/>지형에 약함</td>
</tr>
</table>

### ⚡ Artificial Potential Field (물리 기반 추적)
<sup>가상의 인력/척력을 이용한 빠르고 부드러운 경로 생성</sup>

<table>
<tr>
<td width="30%"><b>동작 원리</b></td>
<td>목표에는 인력, 장애물에는 척력 발생 → 벡터 합으로 이동</td>
</tr>
<tr>
<td><b>시각화</b></td>
<td>🟢 초록색, 유체처럼 흐르는 움직임</td>
</tr>
<tr>
<td><b>치명적 약점</b></td>
<td>⚠️ <b>Local Minimum</b> (U자/O자 구조에서 영구 정지)</td>
</tr>
<tr>
<td><b>대응 전략</b></td>
<td>🎯 <kbd>E</kbd>키로 벽 설치 → 함정 생성!</td>
</tr>
</table>

### 🗺️ Sampling-Based Planning (그래프/트리 탐색)
<sup>현대 자율주행의 핵심 기술 - 공간을 샘플링하여 경로 탐색</sup>

<table>
<tr>
<th width="15%">알고리즘</th>
<th width="35%">동작 원리</th>
<th width="30%">실시간 시각화</th>
<th width="20%">대응법</th>
</tr>
<tr>
<td align="center"><b>PRM</b></td>
<td>맵 전체에 랜덤 노드 뿌려<br/>로드맵 구축 → A* 탐색</td>
<td align="center">🔵 파란색<br/>그래프 네트워크</td>
<td>벽 설치로<br/>그래프 단절</td>
</tr>
<tr>
<td align="center"><b>RRT</b></td>
<td>시작점에서 트리를<br/>목표까지 성장시킴</td>
<td align="center">🟣 보라색<br/>트리 가지들</td>
<td>복잡한 지형에서<br/>재계획 유도</td>
</tr>
</table>

<div align="center">

> 🎨 **시각화의 백미**  
> 적들이 어떻게 "생각"하는지 눈으로 볼 수 있습니다!

</div>

### 🎯 Belief Localization (확률적 추적)
<sup>센서 노이즈 속에서 베이지안 추론으로 위치 추정</sup>

<table>
<tr>
<td width="30%"><b>원리</b></td>
<td>Prediction (모션 모델) + Update (센서 관측) 반복</td>
</tr>
<tr>
<td><b>시각화</b></td>
<td>🟪 청보라색 히트맵 (확률 분포 표시)</td>
</tr>
<tr>
<td><b>약점</b></td>
<td>센서 노이즈에 취약 - 추정 위치가 왜곡됨</td>
</tr>
<tr>
<td><b>대응 전략</b></td>
<td>🎯 <kbd>Q</kbd>키 노이즈 폭탄으로 센서 교란 → 엉뚱한 곳으로 유도!</td>
</tr>
</table>

## 🎮 게임플레이

<div align="center">

### 🎯 목표: 3개의 열쇠를 모아 출구로 탈출!

</div>

### 🕹️ 조작법

<table>
<tr>
<th width="15%">키</th>
<th width="20%">기능</th>
<th width="15%">쿨타임</th>
<th width="50%">전략적 활용</th>
</tr>
<tr>
<td align="center"><kbd>WASD</kbd></td>
<td><b>이동</b></td>
<td align="center">-</td>
<td>적과 거리 유지, 미로 탐색</td>
</tr>
<tr>
<td align="center"><kbd>Shift</kbd></td>
<td><b>대시</b> ⚡</td>
<td align="center">2.5초</td>
<td>위급 상황 탈출, 빠른 회피</td>
</tr>
<tr>
<td align="center"><kbd>E</kbd></td>
<td><b>임시 벽 설치</b> 🧱</td>
<td align="center">6초</td>
<td><b>APF 적을 함정에 가두기</b> (핵심 전략!)</td>
</tr>
<tr>
<td align="center"><kbd>Q</kbd></td>
<td><b>노이즈 폭탄</b> 💥</td>
<td align="center">12초</td>
<td><b>Belief 적의 센서 교란</b> (확률 분포 왜곡)</td>
</tr>
<tr>
<td align="center"><kbd>Space</kbd></td>
<td><b>슬로우모션</b> ⏱️</td>
<td align="center">18초</td>
<td>보스전 생존, 정밀 조작</td>
</tr>
<tr>
<td align="center"><kbd>ESC</kbd></td>
<td><b>일시정지</b></td>
<td align="center">-</td>
<td>전략 재정비, 휴식</td>
</tr>
</table>

### 🏆 스테이지 구성

<table>
<tr>
<td width="50%" align="center">
<img src="images/Stage1-1.png" width="100%"/><br/>
<b>Stage 1: 튜토리얼</b><br/>
Bug1 × 3<br/>
⭐ 기본 조작 익히기
</td>
<td width="50%" align="center">
<img src="images/Stage2.png" width="100%"/><br/>
<b>Stage 2: 패턴 학습</b><br/>
Bug1, Bug2, Tangent<br/>
⭐⭐ 세 가지 Bug 알고리즘 비교
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="images/Stage3.png" width="100%"/><br/>
<b>Stage 3: APF 트랩</b><br/>
Bug2 × 2, APF × 2, Tangent<br/>
⭐⭐⭐ U자 구조로 APF 무력화
</td>
<td width="50%" align="center">
<img src="images/Stage4.png" width="100%"/><br/>
<b>Stage 4: 그래프 차단</b><br/>
Bug2, Tangent, PRM, RRT, APF × 2<br/>
⭐⭐⭐⭐ 샘플링 알고리즘 대응
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="images/Stage5.png" width="100%"/><br/>
<b>Stage 5: 확률 전쟁</b><br/>
Bug2, Tangent, APF, Belief × 2, RRT, PRM<br/>
⭐⭐⭐⭐⭐ 노이즈로 추적 방해
</td>
<td width="50%" align="center">
<img src="images/Stage6.png" width="100%"/><br/>
<b>Stage 6: 보스전</b><br/>
Bug1, Bug2, Tangent, APF, PRM, RRT, Belief × 2<br/>
⭐⭐⭐⭐⭐⭐ 모든 알고리즘 총동원
</td>
</tr>
</table>

| Stage | 테마 | 등장 알고리즘 | 핵심 전략 | 난이도 |
|-------|------|-------------|----------|--------|
| **7+** | 무한 모드 | 점점 증가 (최대 12마리) | 생존 한계 도전 | ∞ |

### 💡 알고리즘별 대응 치트시트

<table>
<tr>
<th width="25%">적 유형</th>
<th width="75%">대응 전략</th>
</tr>
<tr>
<td align="center"><b>🐛 Bug 계열</b></td>
<td>복잡한 장애물 주변으로 유도 → 벽 따라 돌게 만들기</td>
</tr>
<tr>
<td align="center"><b>⚡ APF</b></td>
<td>🌟 <kbd>E</kbd>키로 <b>U자/O자 함정 만들기</b> → Local Minimum 유발 ★★★</td>
</tr>
<tr>
<td align="center"><b>🗺️ PRM/RRT</b></td>
<td><kbd>E</kbd>키로 벽 설치 → 그래프 갱신 강제 (경로 재계산 시간 벌기)</td>
</tr>
<tr>
<td align="center"><b>🎯 Belief</b></td>
<td>🌟 <kbd>Q</kbd>키로 <b>센서 교란</b>, 벽 뒤에 숨기 → 엉뚱한 곳으로 유도 ★★★</td>
</tr>
</table>

## 🚀 빠른 시작

<div align="center">

### 🎮 3분만에 시작하기

</div>

### 설치 요구사항
```
✅ Python 3.8 이상
✅ Windows / macOS / Linux
```

### 1️⃣ 의존성 설치
```bash
pip install -r requirements.txt
```

### 2️⃣ 게임 실행
```bash
# Python으로 직접 실행
python main.py

# 또는 스크립트 사용
# Windows
run_game.bat

# Mac/Linux
./run_game.sh
```

### 3️⃣ 첫 플레이 팁
<table>
<tr>
<td width="25%" align="center">
<b>1️⃣ 패턴 관찰</b><br/>
Stage 1에서 Bug1 적의<br/>움직임 패턴 관찰
</td>
<td width="25%" align="center">
<b>2️⃣ 벽 연습</b><br/>
E키로 벽을 세워<br/>적 가두기 연습
</td>
<td width="25%" align="center">
<b>3️⃣ 대시 절약</b><br/>
대시는 아껴두었다가<br/>위급할 때만 사용
</td>
<td width="25%" align="center">
<b>4️⃣ 미니맵 활용</b><br/>
미니맵을 보고<br/>열쇠 위치 파악
</td>
</tr>
</table>

> 📖 자세한 공략은 [QUICKSTART.md](QUICKSTART.md) 참고

## 📁 프로젝트 구조

<details>
<summary><b>📂 클릭하여 전체 구조 보기</b></summary>

```
roboescape-path-planning/
│
├── main.py                      # 🎮 게임 엔트리 포인트
├── config.py                    # ⚙️ 모든 게임 설정 (속도, 색상, 파라미터)
├── requirements.txt             # 📦 의존성 목록
│
├── game/                        # 🎪 게임 엔진 및 로직
│   ├── engine.py                # 🔄 메인 게임 루프, 상태 관리
│   ├── level.py                 # 🗺️ 6개 스테이지 맵 생성 로직
│   ├── player.py                # 🏃 플레이어 캐릭터 (이동, 스킬)
│   ├── grid.py                  # 📐 그리드 좌표 변환, 충돌 검사
│   ├── ui.py                    # 🖼️ HUD, 미니맵, 게임오버 화면
│   ├── particles.py             # ✨ 파티클 효과 시스템
│   ├── sound.py                 # 🎵 사운드 시스템 (optional)
│   │
│   └── enemies/                 # 🤖 적 AI 구현
│       ├── __init__.py          # 👾 EnemyBase 공통 클래스
│       ├── bug.py               # 🐛 Bug1, Bug2, TangentBug 적
│       ├── apf.py               # ⚡ APF 적 (Local Minimum 감지)
│       ├── prm_rrt.py           # 🗺️ PRM, RRT 적 (그래프/트리 시각화)
│       └── belief.py            # 🎯 Belief 적 (확률 분포 히트맵)
│
├── algos/                       # 🧠 Path-Planning 알고리즘 구현
│   ├── bug.py                   # 🐛 Bug1/2/Tangent Planner
│   ├── apf.py                   # ⚡ APF Planner (인력/척력)
│   ├── prm.py                   # 🔵 PRM Planner (로드맵 + A*)
│   ├── rrt.py                   # 🟣 RRT Planner (트리 확장)
│   └── belief.py                # 🎯 Belief Planner (Bayesian Filter)
│
└── docs/                        # 📚 문서
    ├── README.md                # 📖 프로젝트 소개 (이 파일)
    ├── QUICKSTART.md            # 🚀 빠른 시작 가이드
    ├── GAME_GUIDE.md            # 🎮 상세 게임 매뉴얼
    ├── STAGE_GUIDE.md           # 🗺️ 스테이지별 공략법
    └── DEVELOPMENT.md           # 💻 개발자 문서
```

</details>

### 🏗️ 아키텍처 특징

- **Entity-Component 패턴**: 모든 적은 `EnemyBase` 상속
- **전략 패턴**: 각 알고리즘은 독립된 Planner 클래스
- **이중 좌표계**: Grid(정수) ↔ World(실수) 변환 유틸리티
- **상태 머신**: MENU → PLAYING → STAGE_CLEAR → GAME_OVER
- **옵저버 패턴**: 파티클 시스템이 게임 이벤트에 반응

## 📚 문서

| 문서 | 대상 | 내용 |
|------|------|------|
| [📖 README.md](README.md) | 모두 | 프로젝트 개요 및 소개 (현재 문서) |
| [🚀 QUICKSTART.md](QUICKSTART.md) | 플레이어 | 5분 안에 시작하는 방법 |
| [🎮 GAME_GUIDE.md](GAME_GUIDE.md) | 플레이어 | 조작법, 스킬, 적 대처법 상세 매뉴얼 |
| [🗺️ STAGE_GUIDE.md](STAGE_GUIDE.md) | 플레이어 | 스테이지 1-6 완벽 공략 (스포일러 주의!) |
| [💻 DEVELOPMENT.md](DEVELOPMENT.md) | 개발자 | 코드 구조, 확장 방법, 기술 상세 |

## 🎓 교육적 가치

이 프로젝트는 다음을 학습하는 데 최적화되어 있습니다:

### 🤖 로봇공학 분야
- ✅ 반응형 알고리즘 (Bug Algorithms)의 한계
- ✅ Potential Field의 Local Minimum 문제 체험
- ✅ Sampling-based Planning의 확률적 완전성
- ✅ Probabilistic Localization의 센서 융합

### 💻 게임 개발 분야
- ✅ Pygame을 활용한 실시간 2D 게임 엔진
- ✅ Entity-Component 아키텍처 설계
- ✅ 파티클 시스템 및 시각 효과
- ✅ 게임 UI/UX 설계

### 🧠 알고리즘 분야
- ✅ A* 경로 탐색 (PRM 내부)
- ✅ 트리 자료구조 (RRT)
- ✅ 베이지안 추론 (Belief Filter)
- ✅ 그래프 이론 응용

## 🛠️ 기술 스택

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/-Pygame-green?style=flat-square)
![NumPy](https://img.shields.io/badge/-NumPy-013243?style=flat-square&logo=numpy)
![SciPy](https://img.shields.io/badge/-SciPy-8CAAE6?style=flat-square&logo=scipy)

- **게임 엔진**: Pygame 2.5.0 (렌더링, 이벤트 처리)
- **수치 연산**: NumPy 1.24.0 (그리드 연산, 확률 분포)
- **과학 계산**: SciPy 1.10.0 (최적화, 거리 계산)
- **아키텍처**: Entity-Component, Strategy Pattern

## ✅ 개발 완료 상태

- [x] 🧠 **7가지 알고리즘** 완전 구현 (Bug1/2/Tangent, APF, PRM, RRT, Belief)
- [x] 🗺️ **6개 스테이지** + 보스전 + 무한 모드
- [x] 🎨 **실시간 시각화** (PRM 그래프, RRT 트리, Belief 히트맵)
- [x] ✨ **파티클 효과** (대시, 충돌, 열쇠 획득)
- [x] 🎵 **사운드 시스템** (효과음, 옵션)
- [x] 🖼️ **완전한 UI** (HUD, 미니맵, 게임오버, 통계)
- [x] 📚 **5종 문서화** (README, QUICKSTART, GAME, STAGE, DEVELOPMENT)
- [x] 🎯 **난이도 조정** (점진적 학습 곡선)
- [x] 🔧 **맵 생성 개선** (스폰/아이템 접근성 보장)
- [x] 👁️ **시각화 최적화** (눈 피로 감소)

## 🤝 기여 및 확장 아이디어

### 🎮 게임플레이 확장
- [ ] 새로운 스킬 추가 (텔레포트, 투명화)
- [ ] 멀티플레이어 협동 모드
- [ ] 리더보드 및 순위 시스템

### 🧠 알고리즘 추가
- [ ] `D* Lite` (동적 재계획)
- [ ] `Hybrid A*` (자동차 경로)
- [ ] 강화학습 기반 적 AI

### 🎨 비주얼 개선
- [ ] 스프라이트 아트 교체
- [ ] 애니메이션 추가
- [ ] 더 화려한 이펙트

기여는 언제나 환영합니다! 이슈나 PR을 자유롭게 올려주세요.

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

<div align="center">

## 🎮 지금 바로 플레이하세요!

```bash
python main.py
```

### 📸 게임 스크린샷

<table>
<tr>
<td width="50%" align="center">
<img src="images/Stage1-1.png" width="100%"/><br/>
<b>Stage 1: 튜토리얼 시작</b>
</td>
<td width="50%" align="center">
<img src="images/Stage3.png" width="100%"/><br/>
<b>Stage 3: APF 적 활용</b>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="images/Stage4.png" width="100%"/><br/>
<b>Stage 4: 복잡한 경로 탐색</b>
</td>
<td width="50%" align="center">
<img src="images/Stage5.png" width="100%"/><br/>
<b>Stage 5: 다수 알고리즘 대응</b>
</td>
</tr>
</table>

---

**즐거운 학습과 게임이 되시길 바랍니다!** ⭐

Made with 💜 for Robotics & Game Development Education

[![Star this repo](https://img.shields.io/badge/⭐-Star_this_repo-yellow?style=for-the-badge)](https://github.com/Lova-clover/roboescape-path-planning)

</div>
