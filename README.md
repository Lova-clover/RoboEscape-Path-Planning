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

</div>

## 🌟 프로젝트 하이라이트

이 게임은 **단순한 게임을 넘어 살아있는 알고리즘 교과서**입니다.

| 특징 | 설명 |
|------|------|
| 🎓 **학습 가치** | Bug/APF/PRM/RRT/Belief 등 7가지 실전 알고리즘 체험 |
| 🧩 **전략성** | 각 알고리즘의 약점(Local Minimum, Noise Sensitivity)을 활용한 플레이 |
| 🎨 **가시성** | PRM 로드맵, RRT 트리, Belief 확률 분포를 실시간 시각화 |
| 🎪 **완성도** | 6개 스테이지 + 보스전, 파티클 효과, 사운드, 완전한 UI |
| ⚡ **난이도** | 점진적 학습 곡선: 튜토리얼 → 보스전 → 무한 모드 |

> 💡 **왜 특별한가?** 대부분의 교육용 게임은 알고리즘을 "보여주기만" 합니다. 
> 이 게임은 알고리즘과 **상호작용**하고, 그들의 **강점과 약점을 체감**하게 만듭니다.

## 🧠 구현된 알고리즘

### 🐛 Bug Algorithms (기초 반응형 추적)
실제 로봇이 센서만으로 장애물을 피하는 방식을 시뮬레이션

| 알고리즘 | 동작 원리 | 시각적 특징 | 약점 |
|---------|----------|------------|------|
| **Bug1** | 장애물을 완전히 한 바퀴 돌며 최단 이탈점 찾기 | 🔴 빨간색, 벽 따라 회전 | 복잡한 장애물에서 비효율적 |
| **Bug2** | M-line 기반 직선 복귀 전략 | 🟠 주황색, 직진 시도 | 좁은 통로에서 헤맴 |
| **Tangent Bug** | 시야 기반 접선 방향 선택 | 🟡 노란색, 스마트한 회피 | 시야 제한 지형에 약함 |

### ⚡ Artificial Potential Field (물리 기반 추적)
가상의 인력/척력을 이용한 빠르고 부드러운 경로 생성

- **동작**: 목표에는 인력, 장애물에는 척력 발생 → 벡터 합으로 이동
- **시각화**: 🟢 초록색, 유체처럼 흐르는 움직임
- **치명적 약점**: **Local Minimum** (U자/O자 구조에서 영구 정지)
- **대응 전략**: E키로 벽 설치 → 함정 생성!

### 🗺️ Sampling-Based Planning (그래프/트리 탐색)
공간을 샘플링하여 경로 탐색 - 현대 자율주행의 핵심 기술

| 알고리즘 | 동작 원리 | 실시간 시각화 | 대응법 |
|---------|----------|--------------|--------|
| **PRM** | 맵 전체에 랜덤 노드 뿌려 로드맵 구축 → A* 탐색 | 🔵 파란색 그래프 네트워크 | 벽 설치로 그래프 단절 |
| **RRT** | 시작점에서 트리를 목표까지 성장시킴 | 🟣 보라색 트리 가지들 | 복잡한 지형에서 재계획 유도 |

> 🎨 **시각화의 백미**: 적들이 어떻게 "생각"하는지 눈으로 볼 수 있습니다!

### 🎯 Belief Localization (확률적 추적)
센서 노이즈 속에서 베이지안 추론으로 위치 추정

- **원리**: Prediction (모션 모델) + Update (센서 관측) 반복
- **시각화**: 🟪 청보라색 히트맵 (확률 분포)
- **약점**: Q키 노이즈 폭탄으로 센서 교란 → 엉뚱한 곳으로 유도!

## � 게임플레이

### 🎯 목표
각 스테이지에서 **3개의 열쇠**를 모아 **출구**로 탈출하세요!

### 🕹️ 조작법

| 키 | 기능 | 쿨타임 | 전략적 활용 |
|----|------|--------|-----------|
| **WASD** | 이동 | - | 적과 거리 유지 |
| **Shift** | 대시 | 2.5초 | 위급 상황 탈출 |
| **E** | 임시 벽 설치 | 6초 | APF 적을 함정에 가두기 |
| **Q** | 노이즈 폭탄 | 12초 | Belief 적의 센서 교란 |
| **Space** | 슬로우모션 | 18초 | 보스전 생존 |
| **ESC** | 일시정지 | - | 전략 재정비 |

### 🏆 스테이지 구성

| Stage | 테마 | 등장 알고리즘 | 핵심 전략 | 난이도 |
|-------|------|-------------|----------|--------|
| **1** | 튜토리얼 | Bug1 × 3 | 기본 조작 익히기 | ⭐ |
| **2** | 패턴 학습 | Bug1, Bug2, Tangent | 벽 따라 움직이는 패턴 파악 | ⭐⭐ |
| **3** | APF 트랩 | Bug2, APF × 2, Tangent | U자 구조로 APF 무력화 | ⭐⭐⭐ |
| **4** | 그래프 차단 | Tangent, PRM, RRT, APF × 2 | 벽으로 경로 끊기 | ⭐⭐⭐⭐ |
| **5** | 확률 전쟁 | Bug2, Tangent, APF, Belief × 2, RRT, PRM | 노이즈로 추적 방해 | ⭐⭐⭐⭐⭐ |
| **6** | **보스전** | **전 알고리즘 8마리** | 모든 기술 총동원 | ⭐⭐⭐⭐⭐⭐ |
| **7+** | 무한 모드 | 점점 증가 (최대 12마리) | 생존 한계 도전 | ∞ |

### 💡 알고리즘별 대응 치트시트

```
Bug 계열     → 복잡한 장애물 주변으로 유도
APF          → E키로 U자/O자 함정 만들기 ★★★
PRM/RRT      → 벽 설치로 그래프 갱신 강제
Belief       → Q키로 센서 교란, 벽 뒤에 숨기 ★★★
```

## 🚀 빠른 시작

### 설치 요구사항
- Python 3.8 이상
- Windows / macOS / Linux

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
1. **Stage 1**에서 Bug1 적의 움직임 패턴 관찰
2. **E키**로 벽을 세워 적 가두기 연습
3. **대시**는 아껴두었다가 위급할 때만 사용
4. **미니맵**을 보고 열쇠 위치 파악

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
- [ ] D* / D* Lite (동적 재계획)
- [ ] Hybrid A* (자동차 경로)
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

### 🎮 지금 바로 플레이하세요!

```bash
python main.py
```

**즐거운 학습과 게임이 되시길 바랍니다!** ⭐

Made with 💜 for Robotics & Game Development Education

</div>
