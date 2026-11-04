'''
## 실습 문제 5: Random-Restart로 지역 최소 완화하기

Hill-Climbing은 가장 가까운 지역 최소에서 멈추고, 어디서 멈출지는 시작점이 정합니다. `rugged` 는 전역 최소 `(0, 0)` 외에 정수 격자 근처마다 지역 최소가 있는 함수입니다. 가장 단순한 대응은 시작점을 바꿔 여러 번 돌리고 최선을 취하는 Random-Restart입니다. 앞 문제의 코드는 제공 코드에 들어 있습니다. (이론 3-3, 5장)

- **요구사항:**
    1. `random_restart(make_problem, algorithm, restarts, **kwargs)` 를 완성하세요. `seed` 를 0 부터 `restarts - 1` 까지 바꿔 가며 `algorithm(make_problem(seed), **kwargs)` 를 실행합니다. 값이 가장 작은 결과를 `best` 에 담고, 모든 실행의 평가 횟수를 `total_evals` 에 더합니다.
    2. 추가 코드 작성 없이 출력 결과를 확인하는 항목입니다. 출력 코드는 `rugged` 에 `steepest_ascent` 를 단일 실행한 20번 요약을 먼저 출력합니다. 한 줄에 값이 1 미만인 횟수, 평균 값, 최소 값, 최대 값이 나옵니다.
    3. 추가 코드 작성 없이 출력 결과를 확인하는 항목입니다. 이어서 `rugged` 에 `steepest_ascent` 로 재시작을 10, 100, 300번 적용한 결과를 출력합니다. 한 줄에 재시작 횟수, 해, 최선 값, 총 평가 횟수가 나옵니다. 시작점에서 `delta=0.1` 인 격자로만 움직이므로 `(0, 0)` 에 정확히 닿지 않아 값이 0 이 아닐 수 있습니다.
    4. 추가 코드 작성 없이 출력 결과를 확인하는 항목입니다. 마지막으로 도시 20개 TSP에 재시작을 1, 5, 20번 적용한 결과를 출력합니다. 한 줄에 재시작 횟수, SAHC-T의 최선 비용과 총 평가 횟수, FCHC-T의 최선 비용과 총 평가 횟수가 나옵니다. SAHC-T는 TSP에 적용한 `steepest_ascent`, FCHC-T는 TSP에 적용한 `first_choice` 입니다. FCHC-T의 `limit_stuck=200` 은 `**kwargs` 로 전달됩니다.

함수 끝의 `return` 문은 남기고 TODO를 작성하세요.

제공 코드와 출력 코드는 수정하지 마세요. 출력한 값으로 채점하므로, 제출 전에 직접 넣은 `print` 는 지우세요.

## Practice Problem 5: Easing Local Minima with Random-Restart

Hill-Climbing stops at the nearest local minimum, and the starting point decides where that is. `rugged` has its global minimum at `(0, 0)` and local minima near integer grid points. The simplest response is Random-Restart, which runs the search several times from different starting points and takes the best result. The code from the earlier problems is included in the provided code. (Theory Chapters 3-3 and 5)

- **Requirements:**
    1. Complete `random_restart(make_problem, algorithm, restarts, **kwargs)`. For each `seed` from 0 to `restarts - 1`, run `algorithm(make_problem(seed), **kwargs)`. Store the result with the smallest value in `best`, and add the evaluations of every run to `total_evals`.
    2. This item asks you to inspect the output; no additional code is needed. The output code first prints a summary of 20 single runs of `steepest_ascent` on `rugged`. One line shows the number of runs with a value below 1, the mean value, the minimum value, and the maximum value.
    3. This item asks you to inspect the output; no additional code is needed. It then prints the results of 10, 100, and 300 restarts using `steepest_ascent` on `rugged`. Each line shows the number of restarts, the solution, the best value, and the total number of evaluations. The search moves only on a grid with `delta=0.1` from its starting point, so it may not reach `(0, 0)` exactly and the value may remain above 0.
    4. This item asks you to inspect the output; no additional code is needed. Finally, it prints the results of 1, 5, and 20 restarts on the 20-city TSP. Each line shows the number of restarts, the best cost and total evaluations of SAHC-T, and the best cost and total evaluations of FCHC-T. SAHC-T is `steepest_ascent` applied to TSP, and FCHC-T is `first_choice` applied to TSP. `limit_stuck=200` for FCHC-T is passed through `**kwargs`.

Keep the final `return` statement when completing the TODO.

Do not modify the provided code or the output code. Grading is based on the printed values, so remove any `print` you added before submitting.
'''

# 제공 코드: 수정하지 마세요. / Provided code: do not modify.
import itertools
import math

import numpy as np


class Problem:
    """탐색 문제의 공통 인터페이스."""
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)   # 문제마다 독립된 난수 생성기
        self.num_eval = 0                        # evaluate() 호출 횟수

    def random_init(self):
        raise NotImplementedError

    def evaluate(self, state):
        raise NotImplementedError

    def mutants(self, current):
        raise NotImplementedError

    def random_mutant(self, current):
        raise NotImplementedError


class NumericProblem(Problem):
    def __init__(self, objective, low, high, delta=0.05, seed=None):
        super().__init__(seed)
        self.objective = objective
        self.low, self.high = low, high               # 변수별 범위 리스트
        self.delta = delta

    def random_init(self):
        return [float(self.rng.uniform(a, b)) for a, b in zip(self.low, self.high)]

    def evaluate(self, state):
        self.num_eval += 1
        return float(self.objective(state))

    def mutate(self, current, i, d):
        """i 번째 변수를 d 만큼 옮긴 새 상태. 범위를 벗어나면 None."""
        moved = current[i] + d
        if not (self.low[i] <= moved <= self.high[i]):
            return None
        neighbor = current[:]
        neighbor[i] = moved
        return neighbor

    def mutants(self, current):
        neighbors = []
        for i in range(len(current)):
            for d in (self.delta, -self.delta):
                nb = self.mutate(current, i, d)
                if nb is not None:
                    neighbors.append(nb)
        return neighbors

    def random_mutant(self, current):
        while True:                                   # 범위 안의 이웃이 나올 때까지
            i = int(self.rng.integers(len(current)))
            d = float(self.rng.choice([self.delta, -self.delta]))
            nb = self.mutate(current, i, d)
            if nb is not None:
                return nb


def rugged(point):
    x, y = point
    bump = lambda t: t ** 2 - 10 * np.cos(2 * np.pi * t) + 10   # 1 차원 Rastrigin
    return bump(x) + bump(y)                          # 전역 최솟값 0 at (0, 0)


def best_of(neighbors, problem):
    """이웃을 전부 평가해 (가장 좋은 이웃, 그 값) 을 돌려준다."""
    best, best_value = None, float('inf')
    for nb in neighbors:
        value = problem.evaluate(nb)
        if value < best_value:
            best, best_value = nb, value
    return best, best_value


def steepest_ascent(problem):
    """SAHC: 더 좋은 이웃이 없을 때까지 가장 좋은 이웃으로 이동."""
    problem.num_eval = 0
    current = problem.random_init()
    value_c = problem.evaluate(current)
    path = [current]
    while True:
        successor, value_s = best_of(problem.mutants(current), problem)
        if value_s >= value_c:                        # 개선 없음: 봉우리(여기서는 골짜기)
            break
        current, value_c = successor, value_s
        path.append(current)
    return current, value_c, problem.num_eval, path


def first_choice(problem, limit_stuck=100):
    """FCHC: 무작위 이웃이 더 좋으면 즉시 이동. limit_stuck 번 연속 실패하면 정지."""
    problem.num_eval = 0
    current = problem.random_init()
    value_c = problem.evaluate(current)
    path = [current]
    stuck = 0
    while stuck < limit_stuck:
        successor = problem.random_mutant(current)
        value_s = problem.evaluate(successor)
        if value_s < value_c:
            current, value_c = successor, value_s
            path.append(current)
            stuck = 0
        else:
            stuck += 1
    return current, value_c, problem.num_eval, path


def distance_matrix(locations):
    n = len(locations)
    table = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            (x1, y1), (x2, y2) = locations[i], locations[j]
            table[i][j] = math.hypot(x1 - x2, y1 - y2)     # sqrt((x1-x2)^2 + (y1-y2)^2)
    return table


class TspProblem(Problem):
    def __init__(self, dist, seed=None):
        super().__init__(seed)
        self.dist = dist
        self.n = len(dist)

    def random_init(self):
        return [int(c) for c in self.rng.permutation(self.n)]

    def evaluate(self, order):
        self.num_eval += 1
        total = 0.0
        for i in range(self.n):
            total += self.dist[order[i]][order[(i + 1) % self.n]]   # 마지막은 출발 도시로
        return round(total, 6)    # 같은 길이의 경로 간 부동소수점 오차 방지 / Avoid floating-point differences between equal-length tours.

    def inversion(self, current, i, j):
        neighbor = current[:]
        neighbor[i:j + 1] = neighbor[i:j + 1][::-1]
        return neighbor

    def mutants(self, current):
        return [self.inversion(current, i, j)
                for i, j in itertools.combinations(range(self.n), 2)]   # 모든 (i, j) 쌍: n(n-1)/2 개

    def random_mutant(self, current):
        i, j = sorted(int(v) for v in self.rng.choice(self.n, 2, replace=False))
        return self.inversion(current, i, j)

# 제공 코드 끝. / End of provided code.

def random_restart(make_problem, algorithm, restarts, **kwargs):
    """make_problem(seed) 로 문제를 만들어 algorithm 을 restarts 번 돌리고 최선을 돌려준다."""
    best = (None, float('inf'), 0, [])                # (해, 값, 평가 횟수, path) / (solution, value, evaluations, path)
    total_evals = 0
    # TODO: seed 를 0 부터 restarts - 1 까지 바꿔 가며 algorithm(make_problem(seed), **kwargs) 를 실행하세요.
    #       값이 가장 작은 결과를 best 에 담고, 모든 실행의 평가 횟수를 total_evals 에 더하세요.
    # TODO: For each seed from 0 to restarts - 1, run algorithm(make_problem(seed), **kwargs).
    #       Store the result with the smallest value in best, and add the evaluations of every run to total_evals.
    return best[0], best[1], total_evals, best[3]

# 출력 코드: 수정하지 마세요. / Output code: do not modify.
make_rugged = lambda seed: NumericProblem(rugged, low=[-5.12, -5.12], high=[5.12, 5.12], delta=0.1, seed=seed)

values = [steepest_ascent(make_rugged(seed))[1] for seed in range(20)]
print(sum(v < 1 for v in values), round(float(np.mean(values)), 2), round(min(values), 2), round(max(values), 2))

for restarts in [10, 100, 300]:
    state, value, evals, _ = random_restart(make_rugged, steepest_ascent, restarts)
    print(restarts, None if state is None else [round(v, 2) for v in state], round(value, 4), evals)

NUM_CITIES = 20
city_rng = np.random.default_rng(11)
locations = [tuple(int(v) for v in city_rng.integers(0, 101, size=2)) for _ in range(NUM_CITIES)]
dist = distance_matrix(locations)

make_tsp = lambda seed: TspProblem(dist, seed=seed)

for restarts in [1, 5, 20]:
    s = random_restart(make_tsp, steepest_ascent, restarts)
    f = random_restart(make_tsp, first_choice, restarts, limit_stuck=200)
    print(restarts, round(s[1], 2), s[2], round(f[1], 2), f[2])
