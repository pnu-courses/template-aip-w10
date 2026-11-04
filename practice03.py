'''
## 실습 문제 3: First-Choice Hill-Climbing과 평가 횟수 비교

First-Choice(FCHC)는 이웃을 하나씩 무작위로 만들어 더 좋으면 바로 옮겨 가고, `limit_stuck` 번 연속으로 실패하면 멈춥니다. 한 번의 결과는 시작점에 좌우되므로, 같은 문제를 여러 번 풀어 값과 평가 횟수를 함께 비교합니다. 앞 문제의 코드는 제공 코드에 들어 있습니다. (이론 3장)

- **요구사항:**
    1. `first_choice(problem, limit_stuck=100)` 을 완성하세요. `problem.random_mutant(current)` 로 만든 새 이웃을 `problem.evaluate` 로 한 번만 평가합니다. 그 값이 현재 값보다 작으면 옮겨 가고 `path` 에 추가한 뒤 `stuck` 을 0 으로 되돌립니다. 작지 않으면 `stuck` 을 1 늘립니다. `stuck` 이 `limit_stuck` 에 닿으면 멈춥니다.
    2. `compare(make_problem, repeat, limit_stuck)` 을 완성하세요. `seed` 를 0 부터 `repeat - 1` 까지 바꿔 가며 `make_problem(seed)` 로 매번 새 문제를 만들어 두 알고리즘을 실행하고, 각 결과의 `(값, 평가 횟수)` 를 `sahc`, `fchc` 리스트에 담습니다. SAHC 부분은 미리 들어 있습니다.
    3. 추가 코드 작성 없이 출력 결과를 확인하는 항목입니다. 출력 코드는 같은 시작점에서의 두 알고리즘 결과, `limit_stuck` 을 2, 10, 100 으로 바꾼 FCHC 결과, 20번 실행 요약을 차례로 출력합니다.

함수 끝의 `return` 문은 남기고 TODO를 작성하세요. `show` 는 한 줄에 해, 값, 평가 횟수, 이동 횟수를 출력합니다. `summary` 는 한 줄에 평균 값, 평균 평가 횟수, 최소 평가 횟수, 최대 평가 횟수를 출력합니다.

제공 코드와 출력 코드는 수정하지 마세요. 출력한 값으로 채점하므로, 제출 전에 직접 넣은 `print` 는 지우세요.

## Practice Problem 3: First-Choice Hill-Climbing and Comparing Evaluation Counts

First-Choice (FCHC) builds one random neighbor at a time, moves to it right away if it is better, and stops after `limit_stuck` failures in a row. A single result depends on the starting point, so solve the same problem several times and compare the value and the number of evaluations together. The code from the earlier problems is included in the provided code. (Theory Chapter 3)

- **Requirements:**
    1. Complete `first_choice(problem, limit_stuck=100)`. Evaluate each new neighbor from `problem.random_mutant(current)` exactly once with `problem.evaluate`. If its value is smaller than the current value, move to it, add it to `path`, and reset `stuck` to 0. Otherwise, increase `stuck` by 1. Stop when `stuck` reaches `limit_stuck`.
    2. Complete `compare(make_problem, repeat, limit_stuck)`. For each `seed` from 0 to `repeat - 1`, build a new problem with `make_problem(seed)` for each algorithm, run both algorithms, and store each result's `(value, evaluations)` in the lists `sahc` and `fchc`. The SAHC part is already provided.
    3. This item asks you to inspect the output; no additional code is needed. The output code prints, in order, the results of both algorithms from the same starting point, the FCHC results with `limit_stuck` set to 2, 10, and 100, and a summary of 20 runs.

Keep the final `return` statements when completing the TODOs. `show` prints the solution, the value, the number of evaluations, and the number of moves on one line. `summary` prints the mean value, the mean number of evaluations, the minimum number of evaluations, and the maximum number of evaluations on one line.

Do not modify the provided code or the output code. Grading is based on the printed values, so remove any `print` you added before submitting.
'''

# 제공 코드: 수정하지 마세요. / Provided code: do not modify.
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


def bowl(point):
    x, y = point
    return (x - 3) ** 2 + 2 * (y + 1) ** 2            # 최솟값 0 at (3, -1)


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

# 제공 코드 끝. / End of provided code.

def first_choice(problem, limit_stuck=100):
    """FCHC: 무작위 이웃이 더 좋으면 즉시 이동. limit_stuck 번 연속 실패하면 정지."""
    problem.num_eval = 0
    current = problem.random_init()
    value_c = problem.evaluate(current)
    path = [current]
    stuck = 0
    # TODO: random_mutant 로 만든 새 이웃을 problem.evaluate 로 한 번만 평가하세요.
    #       그 값이 현재 값보다 작으면 옮겨 가고 path 에 추가한 뒤 stuck 을 0 으로 되돌리세요.
    #       작지 않으면 stuck 을 1 늘리고, stuck 이 limit_stuck 에 닿으면 멈추세요.
    # TODO: Evaluate each new neighbor from random_mutant exactly once with problem.evaluate.
    #       If its value is smaller than the current value, move to it, add it to path,
    #       and reset stuck to 0. Otherwise, increase stuck by 1. Stop when stuck reaches limit_stuck.
    return current, value_c, problem.num_eval, path


def compare(make_problem, repeat, limit_stuck):
    """seed 를 바꿔 가며 두 알고리즘을 repeat 번 실행해 (값, 평가 횟수) 를 모은다."""
    sahc, fchc = [], []
    for seed in range(repeat):
        _, value, evals, _ = steepest_ascent(make_problem(seed))
        sahc.append((value, evals))
        # TODO: first_choice(make_problem(seed), limit_stuck=limit_stuck) 도 같은 방식으로 실행해 fchc 에 담으세요.
        # TODO: Run first_choice(make_problem(seed), limit_stuck=limit_stuck) the same way and store the result in fchc.
    return sahc, fchc

# 출력 코드: 수정하지 마세요. / Output code: do not modify.
def show(result):
    state, value, evals, path = result
    print([round(v, 3) for v in state], round(value, 4), evals, len(path) - 1)


def summary(results):
    if not results:
        print(None)
        return
    values = [r[0] for r in results]
    evals = [r[1] for r in results]
    print(round(float(np.mean(values)), 5), round(float(np.mean(evals)), 1), min(evals), max(evals))


make_bowl = lambda seed: NumericProblem(bowl, low=[-10, -10], high=[10, 10], delta=0.05, seed=seed)

show(steepest_ascent(make_bowl(5)))
show(first_choice(make_bowl(5), limit_stuck=100))

for limit in [2, 10, 100]:
    show(first_choice(make_bowl(5), limit_stuck=limit))

sahc, fchc = compare(make_bowl, repeat=20, limit_stuck=100)
summary(sahc)
summary(fchc)
