'''
## 실습 문제 1: 수치 최적화 문제의 이웃 만들기

수치 최적화는 변수 값을 조절해 목적함수 값을 가장 작게 만드는 지점을 찾는 문제입니다. Hill-Climbing은 현재 상태에서 이웃으로 옮겨 가므로 이웃을 만드는 방법을 먼저 정해야 합니다. 수치 문제에서는 변수 하나만 `delta` 만큼 증가 또는 감소시켜 이웃을 만들고, 범위를 벗어나는 이웃은 만들지 않습니다. (이론 2장)

- **요구사항:**
    1. `mutate(current, i, d)` 를 완성하세요. `i` 번째 변수를 `d` 만큼 옮긴 새 상태를 반환합니다. 옮긴 값이 `self.low[i]` 이상 `self.high[i]` 이하가 아니면 `None` 을 반환합니다. `current` 는 바꾸지 않습니다. (힌트: `current[:]`)
    2. `mutants(current)` 를 완성하세요. 모든 변수에 `+delta` 와 `-delta` 를 적용해 범위 안의 이웃만 리스트로 반환합니다. 변수가 `n` 개면 이웃은 최대 `2n` 개입니다. (힌트: `mutate` 의 결과가 `None` 이 아닐 때만 추가)
    3. `random_mutant(current)` 를 완성하세요. 변수 하나와 `+delta`, `-delta` 중 하나를 `self.rng` 로 무작위로 골라 이웃 하나를 반환합니다. 범위를 벗어나면 범위 안의 이웃이 나올 때까지 다시 뽑습니다. (힌트: `self.rng.integers(len(current))`, `self.rng.choice([self.delta, -self.delta])`, `while True`)

세 메서드의 자리표시 `return` 문은 지우고 작성하세요. 출력 코드의 각 줄이 어떤 값을 출력하는지는 해당 줄의 식을 보고 확인하세요.

제공 코드와 출력 코드는 수정하지 마세요. 출력한 값으로 채점하므로, 제출 전에 직접 넣은 `print` 는 지우세요.

## Practice Problem 1: Building Neighbors for a Numerical Optimization Problem

Numerical optimization adjusts the values of variables to find the point where the objective function is smallest. Hill-Climbing moves from the current state to a neighbor, so the way neighbors are built must be decided first. In a numerical problem, a neighbor is built by increasing or decreasing one variable by `delta`, and neighbors outside the range are not built. (Theory Chapter 2)

- **Requirements:**
    1. Complete `mutate(current, i, d)`. It returns a new state with variable `i` moved by `d`. If the moved value is not between `self.low[i]` and `self.high[i]`, inclusive, it returns `None`. It does not change `current`. (Hint: `current[:]`)
    2. Complete `mutants(current)`. It applies `+delta` and `-delta` to every variable and returns a list of only the neighbors in range. With `n` variables there are at most `2n` neighbors. (Hint: add a neighbor only when the result of `mutate` is not `None`)
    3. Complete `random_mutant(current)`. It uses `self.rng` to pick one variable and one of `+delta` and `-delta` at random and returns that neighbor. If the neighbor is out of range, it draws again until one is in range. (Hint: `self.rng.integers(len(current))`, `self.rng.choice([self.delta, -self.delta])`, `while True`)

Replace the placeholder `return` statements in the three methods with your code. Read the expressions on each line of the output code to see which values it prints.

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

# 제공 코드 끝. / End of provided code.

# TODO: mutate, mutants, random_mutant 의 자리표시 return 문만 지우고 작성하세요.
# TODO: Replace only the placeholder return statements in mutate, mutants, and random_mutant with your code.

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
        # TODO: i 번째 변수를 d 만큼 옮긴 새 상태를 반환하세요. 옮긴 값이 범위를 벗어나면 None 을 반환하세요.
        # TODO: Return a new state with variable i moved by d. Return None if the moved value is out of range.
        return None

    def mutants(self, current):
        # TODO: 모든 변수에 +delta 와 -delta 를 적용해 범위 안의 이웃만 리스트로 반환하세요.
        # TODO: Apply +delta and -delta to every variable and return a list of only the neighbors in range.
        return []

    def random_mutant(self, current):
        # TODO: 변수 하나와 방향 하나를 self.rng 로 무작위로 골라 이웃 하나를 반환하세요. 범위를 벗어나면 다시 뽑으세요.
        # TODO: Use self.rng to pick one variable and one direction at random and return that neighbor.
        #       If it is out of range, draw again.
        return current[:]

# 출력 코드: 수정하지 마세요. / Output code: do not modify.
def bowl(point):
    x, y = point
    return (x - 3) ** 2 + 2 * (y + 1) ** 2            # 최솟값 0 at (3, -1)


def distinct(states):
    return sorted(set(tuple(float(v) for v in s) for s in states))


p = NumericProblem(bowl, low=[-10, -10], high=[10, 10], delta=0.05, seed=42)
q = NumericProblem(lambda s: sum(v ** 2 for v in s), low=[-1, -1, -1], high=[1, 1, 1], delta=0.5, seed=42)
start = [0.0, 0.0]

print(p.evaluate([3.0, -1.0]), p.evaluate(start))
print(p.mutate(start, 0, 0.05))
print(p.mutate(start, 1, -0.05))
print(p.mutate([10.0, 0.0], 0, 0.05))
print(q.mutate([0.5, 0.0, 0.0], 0, 0.5))
print(len(p.mutants(start)), len(q.mutants([0.0, 0.0, 0.0])), len(q.mutants([1.0, -1.0, 0.0])))
print(distinct(p.mutants(start)))
print(distinct(p.mutants([10.0, 10.0])))
print(distinct(p.random_mutant(start) for _ in range(200)))
print(distinct(p.random_mutant([10.0, 10.0]) for _ in range(200)))
print(start)
