# 🚀 RoboEscape 실행 가이드

## ⚡ 빠른 시작 (권장)

### Windows
```batch
run_game.bat
```
더블클릭하면 자동으로:
1. 가상환경 체크/생성
2. 의존성 설치
3. 게임 실행

### Mac/Linux
```bash
chmod +x run_game.sh
./run_game.sh
```

---

## 🎮 게임 플레이

### 조작법
```
W/A/S/D   - 이동
Shift     - 대시 (쿨타임 2.5초)
E         - 장벽 설치 (쿨타임 6초) - APF 적 무력화!
Q         - 노이즈 폭탄 (쿨타임 12초) - Belief 적 교란!
Space     - 슬로우 모션 (쿨타임 18초)
ESC       - 일시정지
```

### 목표
1. 노란색 열쇠 3개 수집
2. 녹색 출구로 탈출
3. 다양한 알고리즘 적들 회피

---

## 🎯 스테이지 구성

| Stage | 적 구성 | 핵심 학습 | 난이도 |
|-------|--------|----------|--------|
| 1 | Bug1 × 2 | 기본 회피 | ★☆☆☆☆☆ |
| 2 | Bug1/2/Tangent | 패턴 구분 | ★★☆☆☆☆ |
| 3 | Bug2 + APF × 2 | 로컬 미니멈 | ★★★☆☆☆ |
| 4 | Tangent/PRM/RRT/APF | 그래프 차단 | ★★★★☆☆ |
| 5 | Bug2/APF/Belief×2/RRT | 확률적 추적 | ★★★★★☆ |
| 6 | **전부 8마리** | **보스전** | ★★★★★★ |
| 7+ | 최대 12마리 | 무한 도전 | 💀💀💀 |

---

## 🧠 알고리즘 한눈에 보기

### 🔴 Bug Algorithms (기초)
- **Bug1** (연한 빨강): 벽 따라 한 바퀴
- **Bug2** (빨강): 직선 경로 고집
- **Tangent** (주황): 코너 전략

### 🔥 APF (강력)
- **APF** (진한 빨강): 빠른 추격, 로컬 미니멈 약점

### 🔵 Sampling-Based (그래프/트리)
- **PRM** (파랑): 로드맵 기반, 파란 선 보임
- **RRT** (하늘색): 트리 탐색, 가지 보임

### 🟣 Probabilistic (확률)
- **Belief** (보라): 확률 추정, 보라색 열기 보임

---

## 💡 핵심 전략

### Stage 3 (APF 처음 등장)
```
1. E키로 U자 구조 만들기:
   ██████
   █    █
   █    █

2. APF 적 유인

3. 로컬 미니멈에 갇힘 → 무력화!
```

### Stage 5 (Belief 처음 등장)
```
1. Q키 노이즈 폭탄 사용

2. Belief 적 혼란 (노란 원 표시)

3. 벽 뒤에 숨기 → 추적 정확도 하락
```

### Stage 6 (보스전!)
```
1. APF부터 무력화 (장벽 설치)
2. Bug들 회피하며 열쇠 수집
3. 노이즈로 Belief 교란
4. 장벽으로 PRM/RRT 차단
5. 탈출!
```

---

## 🎨 시각적 특징

### 알고리즘 시각화 켜기/끄기
게임 중 다음을 볼 수 있습니다:
- PRM: 파란색 그래프 네트워크
- RRT: 하늘색 탐색 트리
- Belief: 보라색 확률 히트맵
- 모든 적: 계획된 경로 (얇은 선)

### 파티클 이펙트
- 대시: 청록색 트레일
- 충돌: 빨간색 폭발
- 열쇠 수집: 노란색 폭발
- 장벽 설치: 파란색 폭발
- 노이즈 폭탄: 노란색 확산

---

## 📊 상세 문서

- [STAGE_GUIDE.md](STAGE_GUIDE.md) - 스테이지별 완전 공략
- [GAME_GUIDE.md](GAME_GUIDE.md) - 플레이어 가이드
- [DEVELOPMENT.md](DEVELOPMENT.md) - 개발자 문서

---

## ⚙️ 설정 조정

난이도나 성능을 조정하고 싶다면 [config.py](config.py) 수정:

```python
# 플레이어 강화
PLAYER_SPEED = 250  # 기본: 200
PLAYER_MAX_HEALTH = 5  # 기본: 3

# 적 약화
ENEMY_APF_SPEED = 100  # 기본: 120
ENEMY_BELIEF_SPEED = 70  # 기본: 90

# 스킬 강화
SKILL_WALL_COOLDOWN = 3.0  # 기본: 5.0
SKILL_NOISE_COOLDOWN = 6.0  # 기본: 10.0
```

---

## 🐛 문제 해결

### 게임이 시작되지 않음
```bash
pip uninstall pygame
pip install pygame
```

### 느린 프레임레이트
config.py에서:
```python
DEBUG_SHOW_PATHS = False  # 경로 표시 끄기
```

### 너무 어려움
config.py에서:
```python
STAGE_TIME_LIMIT = 300  # 기본: 180 (초)
```

---

## 🏆 완성도

✅ **구현 완료:**
- 7가지 Path-Planning 알고리즘
- 6개 스테이지 + 보스전 + 무한 모드
- 실시간 알고리즘 시각화
- 파티클 이펙트 시스템
- 사운드 시스템 (옵션)
- 완벽한 문서화

---

## 🎓 교육적 가치

이 게임을 통해 학습할 수 있는 것:

1. **Bug Algorithms**: 반응형 경로 계획
2. **Potential Fields**: 인력/척력 기반 제어
3. **PRM/RRT**: 샘플링 기반 경로 계획
4. **Bayesian Filter**: 확률적 상태 추정

실제 로봇공학에서 사용되는 알고리즘들을 게임으로!

---

## 📝 크레딧

- Path-Planning 알고리즘: 로봇공학 표준 알고리즘
- 게임 엔진: Pygame
- 개발: AI Assistant + Your Ideas

---

**즐거운 게임 되세요! 🎮🤖**

P.S. Stage 6 클리어하면 진짜 대단한 겁니다! 👑
