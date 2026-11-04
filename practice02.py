'''
## 실습 문제 2: Steepest-Ascent Hill-Climbing

Steepest-Ascent(SAHC)는 이웃을 전부 만들어 평가한 뒤 가장 좋은 이웃으로 옮겨 가고, 더 좋은 이웃이 없으면 멈춥니다. 이 실습은 최소화 문제이므로 목적함수 값이 작을수록 좋습니다. 문제 1의 코드는 제공 코드에 들어 있습니다. (이론 3장)

- **요구사항:**
    1. `best_of(neighbors, problem)` 을 완성하세요. 이웃마다 `problem.evaluate` 로 한 번씩만 평가해 값이 가장 작은 이웃과 그 값을 `(이웃, 값)` 으로 반환합니다.
    2. `steepest_ascent(problem)` 을 완성하세요. `problem.mutants(current)` 중 가장 좋은 이웃의 값이 현재 값보다 작으면 그 이웃으로 옮겨 가고 `path` 에 추가합니다. 작지 않으면 멈춥니다. (힌트: `while True`, `break`)
    3. 추가 코드 작성 없이 출력 결과를 확인하는 항목입니다. 출력 코드는 `delta` 를 0.5, 0.05, 0.01 로 바꿔 가며 결과를 출력합니다. `delta` 에 따라 값과 이동 횟수가 어떻게 달라지는지 확인하세요.

함수 끝의 `return` 문은 남기고 TODO를 작성하세요. 출력의 처음 4줄에 나오는 값은 출력 코드의 해당 식을 보고 확인하세요. `show` 는 한 줄에 해, 값, 평가 횟수, 이동 횟수를 출력합니다.

제공 코드와 출력 코드는 수정하지 마세요. 출력한 값으로 채점하므로, 제출 전에 직접 넣은 `print` 는 지우세요.

## Practice Problem 2: Steepest-Ascent Hill-Climbing

Steepest-Ascent (SAHC) builds and evaluates all neighbors, moves to the best one, and stops when no neighbor is better. This practice is a minimization problem, so a smaller objective value is better. The code from Problem 1 is included in the provided code. (Theory Chapter 3)

- **Requirements:**
    1. Complete `best_of(neighbors, problem)`. Evaluate each neighbor exactly once with `problem.evaluate` and return the neighbor with the smallest value and that value as `(neighbor, value)`.
    2. Complete `steepest_ascent(problem)`. If the best neighbor from `problem.mutants(current)` has a value smaller than the current value, move to it and add it to `path`. Otherwise, stop. (Hint: `while True`, `break`)
    3. This item asks you to inspect the output; no additional code is needed. The output code prints results with `delta` set to 0.5, 0.05, and 0.01. Check how the value and the number of moves change with `delta`.

Keep the final `return` statements when completing the TODOs. Read the corresponding expressions in the output code to see which values the first 4 lines print. `show` prints the solution, the value, the number of evaluations, and the number of moves on one line.

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

# 제공 코드 끝. / End of provided code.

def best_of(neighbors, problem):
    """이웃을 전부 평가해 (가장 좋은 이웃, 그 값) 을 돌려준다."""
    best, best_value = None, float('inf')
    # TODO: 이웃마다 problem.evaluate 로 한 번씩만 평가해 값이 가장 작은 이웃과 그 값을 best, best_value 에 담으세요.
    # TODO: Evaluate each neighbor exactly once with problem.evaluate and store the best neighbor and its value in best and best_value.
    return best, best_value


def steepest_ascent(problem):
    """SAHC: 더 좋은 이웃이 없을 때까지 가장 좋은 이웃으로 이동."""
    problem.num_eval = 0
    current = problem.random_init()
    value_c = problem.evaluate(current)
    path = [current]
    # TODO: best_of 로 가장 좋은 이웃을 고르세요. 현재 값보다 작으면 옮겨 가고 path 에 추가하고, 작지 않으면 멈추세요.
    # TODO: Pick the best neighbor with best_of. If its value is smaller than the current value, move to it and
    #       add it to path. Otherwise, stop.
    return current, value_c, problem.num_eval, path

# 출력 코드: 수정하지 마세요. / Output code: do not modify.
def show(result):
    state, value, evals, path = result
    print([round(v, 3) for v in state], round(value, 4), evals, len(path) - 1)


probe = NumericProblem(bowl, low=[-10, -10], high=[10, 10], seed=0)
print(best_of([[0.0, 0.0], [3.0, -1.0], [3.0, 0.0]], probe))
print(probe.num_eval)

for seed in [1, 2]:
    show(steepest_ascent(NumericProblem(bowl, low=[-10, -10], high=[10, 10], delta=0.05, seed=seed)))

for delta in [0.5, 0.05, 0.01]:
    show(steepest_ascent(NumericProblem(bowl, low=[-10, -10], high=[10, 10], delta=delta, seed=1)))
