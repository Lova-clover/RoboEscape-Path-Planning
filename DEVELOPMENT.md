# 🎮 RoboEscape: Algorithm Hunters - 개발 문서

## 📐 설계 철학

이 프로젝트는 로봇 알고리즘(Path-Planning)을 재미있는 게임으로 구현한 것입니다.
각 적은 실제 로봇공학에서 사용되는 경로 계획 알고리즘으로 움직이며,
플레이어는 각 알고리즘의 약점을 이용해 적들을 회피합니다.

## 🏗️ 프로젝트 구조

```
RoboEscape/
├── main.py              # 게임 진입점
├── config.py            # 모든 상수 및 설정
├── requirements.txt     # Python 의존성
│
├── game/                # 게임 엔진
│   ├── engine.py        # 메인 게임 루프 및 상태 관리
│   ├── level.py         # 맵 생성 및 관리
│   ├── grid.py          # 그리드 시스템 및 좌표 변환
│   ├── player.py        # 플레이어 로직
│   ├── ui.py            # HUD 및 UI
│   ├── particles.py     # 파티클 이펙트
│   └── enemies/         # 적 AI
│       ├── __init__.py  # 기본 Enemy 클래스
│       ├── bug.py       # Bug 알고리즘 적들
│       └── apf.py       # APF 알고리즘 적
│
└── algos/               # Path-Planning 알고리즘
    ├── bug.py           # Bug1, Bug2, Tangent Bug
    ├── apf.py           # Artificial Potential Field
    ├── prm.py           # (예정) Probabilistic Roadmap
    ├── rrt.py           # (예정) Rapidly-exploring Random Tree
    └── belief.py        # (예정) Bayesian Localization
```

## 🎯 구현된 알고리즘

### 1. Bug Algorithms

#### Bug1
- **원리**: 장애물을 만나면 한 바퀴 돌며 목표에 가장 가까운 점을 찾음
- **구현**: `algos/bug.py::Bug1Planner`
- **게임에서**: 벽 주변을 빙빙 도는 패턴
- **약점**: 복잡한 장애물에서 시간 낭비

```python
# 핵심 로직
def plan_step(self, current_pos, goal_pos, grid_map):
    if self.state == 'go_to_goal':
        # 목표로 직진
        next_pos = self._move_towards(current_pos, goal_pos)
        if obstacle_hit:
            self.state = 'follow_wall'
    elif self.state == 'follow_wall':
        # 벽 따라 이동, 최소 거리 점 기록
        if circumnavigation_complete:
            self.state = 'leave_wall'
```

#### Bug2
- **원리**: Start-Goal 직선(M-line)을 유지하려고 함
- **구현**: M-line 거리 기반 의사결정
- **게임에서**: 직선 경로를 고집하는 패턴
- **약점**: M-line 밖으로 유도하면 효율 하락

#### Tangent Bug
- **원리**: 센서 범위 내 장애물의 Tangent 포인트를 활용
- **구현**: 시야 기반 전략적 코너링
- **게임에서**: 영리하게 코너를 도는 패턴
- **약점**: 센서 범위 제한

### 2. Artificial Potential Field (APF)

- **원리**: 목표는 인력, 장애물은 척력으로 작용
- **구현**: `algos/apf.py::APFPlanner`
- **핵심 수식**:
  ```
  F_attractive = k_att * (goal - current)
  F_repulsive = k_rep * Σ (1/d - 1/d_inf) * (1/d²) * direction
  F_total = F_attractive + F_repulsive
  ```
- **게임에서**: 매우 빠르고 직진성이 강함
- **약점**: **로컬 미니멈** - U자/O자 구조에 갇힘

```python
# 로컬 미니멈 감지
def detect_local_minimum(self, force_history, threshold=0.1, window=5):
    if len(force_history) < window:
        return False
    recent_forces = force_history[-window:]
    avg_force = sum(recent_forces) / window
    return avg_force < threshold
```

## 🎨 게임 메커니즘

### 좌표 시스템

게임은 두 좌표계를 사용합니다:

1. **Grid 좌표** (정수): 타일맵, 경로 계획에 사용
2. **World 좌표** (실수): 실제 객체 위치, 렌더링에 사용

```python
# 변환 함수
def grid_to_world(gx, gy):
    return gx * TILE_SIZE + TILE_SIZE / 2, gy * TILE_SIZE + TILE_SIZE / 2

def world_to_grid(x, y):
    return int(x // TILE_SIZE), int(y // TILE_SIZE)
```

### 충돌 감지

- **플레이어/적**: 원형 충돌 (Circle Collision)
- **벽**: 타일 기반 충돌 검사
- **임시 장벽**: 동적 맵 업데이트

```python
def check_collision_circle(x, y, radius, grid_map):
    # 원의 경계 상자 계산
    # 각 타일과 원의 거리 체크
    # 충돌 시 True 반환
```

### 스킬 시스템

| 스킬 | 키 | 쿨타임 | 효과 |
|------|-----|---------|------|
| 대시 | Shift | 2초 | 빠른 이동, 무적 아님 |
| 장벽 | E | 5초 | 임시 벽 3개 설치 (8초 지속) |
| 노이즈 | Q | 10초 | Belief 적 교란 (예정) |
| 슬로우모션 | Space | 15초 | 시간 느리게 (예정) |

## 📊 성능 최적화

### 그리드 최적화
- **화면 밖 타일 컬링**: 보이는 타일만 렌더링
- **경로 재계산 주기**: 적마다 0.3~0.5초 간격
- **장애물 캐싱**: 주변 장애물 미리 수집

### 파티클 최적화
- **수명 관리**: 자동 소멸
- **최대 개수 제한**: 메모리 보호
- **알파 블렌딩**: Pygame SRCALPHA

## 🔧 커스터마이징 가이드

### 새 적 추가하기

1. **알고리즘 구현** (`algos/` 폴더)
```python
class MyPlanner:
    def plan_step(self, current_pos, goal_pos, grid_map):
        # 경로 계획 로직
        return next_position
```

2. **Enemy 클래스 생성** (`game/enemies/` 폴더)
```python
class MyEnemy(EnemyBase):
    def __init__(self, x, y):
        super().__init__(x, y, SPEED, COLOR, "MyEnemy")
        self.planner = MyPlanner()
    
    def update(self, dt, player, level):
        # 적 업데이트 로직
        next_grid = self.planner.plan_step(...)
        self.path = [next_grid]
        self.move_along_path(dt, level)
```

3. **스테이지에 추가** (`game/engine.py`)
```python
def _spawn_enemies(self):
    # ...
    self.enemies.append(MyEnemy(*grid_to_world(x, y)))
```

### 새 스테이지 추가하기

`game/level.py`에서:

```python
def _generate_stage4(self):
    """스테이지 4: 특수 맵"""
    # 장애물 배치
    for i in range(10, 20):
        self.grid_map[10][i] = TILE_WALL
    
    # 특수 구조물
    # ...
```

### 밸런스 조정

`config.py`에서 주요 값들:

```python
# 플레이어
PLAYER_SPEED = 200          # 이동 속도
PLAYER_MAX_HEALTH = 3       # 체력
PLAYER_DASH_COOLDOWN = 2.0  # 대시 쿨타임

# 적
ENEMY_APF_SPEED = 120       # APF 속도
APF_ATTRACT_GAIN = 1.0      # 인력 강도
APF_REPULSE_GAIN = 100.0    # 척력 강도

# 스킬
SKILL_WALL_COOLDOWN = 5.0   # 장벽 쿨타임
SKILL_WALL_DURATION = 8.0   # 장벽 지속시간
```

## 🐛 디버그 모드

`config.py`에서 디버그 옵션:

```python
DEBUG_SHOW_GRID = True      # 그리드 라인 표시
DEBUG_SHOW_PATHS = True     # 적 경로 표시
DEBUG_SHOW_BELIEF = False   # Belief 분포 표시 (예정)
DEBUG_SHOW_APF_FIELD = False # APF 필드 시각화 (예정)
```

## 📈 향후 계획

### 단기 (v1.0)
- [x] Bug 알고리즘 (Bug1, Bug2, Tangent)
- [x] APF 알고리즘
- [x] 기본 UI/HUD
- [x] 파티클 이펙트
- [ ] 사운드 효과
- [ ] 튜토리얼 모드

### 중기 (v2.0)
- [ ] PRM (Probabilistic Roadmap) 적
- [ ] RRT (Rapidly-exploring Random Tree) 적
- [ ] Belief/Kalman Filter 적
- [ ] 슬로우 모션 구현
- [ ] 더 많은 스테이지

### 장기 (v3.0)
- [ ] 멀티플레이어 (협동)
- [ ] 랭킹 시스템
- [ ] 커스텀 맵 에디터
- [ ] 모바일 포팅

## 🎓 교육적 가치

이 게임은 다음을 학습할 수 있습니다:

1. **Path-Planning 알고리즘**: 실제로 동작하는 모습
2. **알고리즘 장단점**: 각 상황에서의 성능 차이
3. **게임 개발**: Pygame 기반 2D 게임 구조
4. **AI 행동 패턴**: 게임 AI 설계

## 📚 참고 자료

- [Path-Planning 알고리즘 설명](https://github.com/Lova-clover/Path-Planning)
- [Pygame 공식 문서](https://www.pygame.org/docs/)
- [Bug Algorithms 논문](https://ieeexplore.ieee.org/)
- [APF 원리](https://en.wikipedia.org/wiki/Artificial_potential_field)

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

**Made with ❤️ for robotics education**
