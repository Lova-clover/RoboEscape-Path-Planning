# 🤖 RoboEscape: Algorithm Hunters

**다른 사람들이 놀랄 만한 Path-Planning 알고리즘 게임!**

탑뷰 2D 생존 게임으로, 실제 로봇공학의 경로 계획 알고리즘이 적 AI로 구현되어 있습니다.

## ✨ 게임 하이라이트

- 🎓 **교육적**: 7가지 실제 Path-Planning 알고리즘을 게임으로 체험
- 🎮 **게임성**: 각 알고리즘의 약점을 이용한 전략적 플레이
- 🎨 **시각화**: 알고리즘의 사고 과정을 실시간으로 확인
- 🏆 **6개 스테이지 + 보스전**: 점진적으로 증가하는 난이도
- 💥 **파티클 이펙트**: 화려한 비주얼과 피드백

## 🧠 구현된 알고리즘 (전부!)

### 1. Bug Algorithms (기초 추적)
- **Bug1**: 장애물 한 바퀴 돌며 최단 경로 탐색
- **Bug2**: M-line 기반 직진 추적
- **Tangent Bug**: 시야 기반 전략적 코너링

### 2. Artificial Potential Field (강력한 추적)
- **APF**: 인력/척력 기반 빠른 추격
- **약점**: 로컬 미니멈에 갇힘 (U자 함정!)

### 3. Sampling-Based Planning (그래프/트리 기반)
- **PRM**: 로드맵 사전 구축, 최적 경로
- **RRT**: 실시간 트리 탐색, 동적 경로

### 4. Probabilistic Localization (확률적 추적)
- **Belief Filter**: 베이지안 필터 기반 위치 추정
- **노이즈 폭탄**에 취약!

## 🎯 게임 특징

- ⚡ **6개 스테이지**: 각 스테이지마다 특화된 맵과 알고리즘 조합
- 🎨 **실시간 시각화**: PRM 그래프, RRT 트리, Belief 히트맵 표시
- 🎪 **스킬 시스템**: 대시, 장벽 설치, 노이즈 폭탄
- 📊 **통계 시스템**: 플레이 데이터 기록
- 🎵 **사운드**: 효과음 시스템 (옵션)
- 🏆 **보스전**: Stage 6에서 모든 알고리즘 총집합!

## 🕹️ 조작법

- **WASD**: 이동
- **Shift**: 대시 (쿨타임)
- **E**: 장벽 설치 (APF 로컬 미니멈 유도)
- **Q**: 노이즈 폭탄 (Belief 적 교란)
- **Space**: 슬로우 모션 (제한적)
- **ESC**: 일시정지

## 🚀 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 게임 실행
python main.py
```

## 📁 프로젝트 구조

```
RoboEscape/
├── main.py              # 게임 시작
├── config.py            # 모든 설정
├── requirements.txt     # 의존성
│
├── game/                # 게임 엔진
│   ├── engine.py        # 메인 루프
│   ├── level.py         # 6개 스테이지 맵
│   ├── player.py        # 플레이어
│   ├── ui.py            # HUD/UI
│   ├── particles.py     # 파티클 이펙트
│   ├── sound.py         # 사운드
│   └── enemies/         # 적 AI (7종)
│
└── algos/               # Path-Planning
    ├── bug.py           # Bug1/2/Tangent
    ├── apf.py           # APF
    ├── prm.py           # PRM
    ├── rrt.py           # RRT
    └── belief.py        # Bayesian Filter
```

## 🎓 알고리즘별 약점 공략

### Bug Algorithms
- 복잡한 장애물 주변에서 헤맴
- 벽을 따라 도는 패턴 예측 가능

### APF Enemy
- 로컬 미니멈에 쉽게 빠짐
- U자/O자 구조로 유도하여 무력화

### PRM/RRT Enemy
- 장벽 설치로 그래프 경로 차단
- 복잡한 구조에서 재계산 시간 지연

### Belief Enemy
- 노이즈 폭탄으로 위치 추정 교란
- 벽 뒤에 숨으면 추적 정확도 하락

## ✅ 개발 완료!

- [x] 7가지 Path-Planning 알고리즘 완전 구현
- [x] 6개 스테이지 + 보스전 + 무한 모드
- [x] 실시간 알고리즘 시각화 (PRM 그래프, RRT 트리, Belief 히트맵)
- [x] 파티클 이펙트 시스템
- [x] 사운드 시스템 (효과음)
- [x] 완벽한 문서화 (4종)
- [x] 스테이지별 특화 맵
- [x] 다음 스테이지 자동 진행

## 🎯 지금 바로 플레이!

```bash
# Windows
run_game.bat

# Mac/Linux
./run_game.sh
```

자세한 가이드: [QUICKSTART.md](QUICKSTART.md)

## 📝 라이선스

MIT License
