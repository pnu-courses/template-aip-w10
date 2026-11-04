'''
## 실습 문제 4: TSP에 같은 알고리즘 적용하기

TSP는 모든 도시를 정확히 한 번씩 방문하고 출발 도시로 돌아오는 최단 순회 경로를 찾는 문제입니다. 상태는 도시 번호의 순열이고, `[2, 0, 3, 1]` 은 도시 2, 0, 3, 1 을 거쳐 다시 2로 돌아오는 경로입니다. 순열에는 `±delta` 를 쓸 수 없으므로 경로의 한 구간을 뒤집어(inversion) 이웃을 만듭니다. 제공 코드의 알고리즘 `steepest_ascent`, `first_choice` 는 수치 문제에 쓰던 코드 그대로입니다. (이론 4장, 5장)

- **요구사항:**
    1. `distance_matrix(locations)` 를 완성하세요. `table[i][j]` 가 도시 `i` 와 `j` 사이의 거리인 `n x n` 리스트를 반환합니다. (힌트: `math.hypot(x1 - x2, y1 - y2)`)
    2. `evaluate(order)` 를 완성하세요. 경로를 따라 이동한 총 거리를 `total` 에 구하고, 마지막 도시에서 출발 도시로 돌아오는 거리도 더합니다. 마지막 줄의 `round` 는 지우지 마세요.
    3. `inversion(current, i, j)` 를 완성하세요. 양 끝 인덱스 `i`, `j` 를 포함한 구간을 뒤집은 새 순열을 반환합니다. `current` 는 바꾸지 않습니다. (힌트: `neighbor[i:j + 1] = neighbor[i:j + 1][::-1]`)
    4. `mutants(current)` 를 완성하세요. `i < j` 인 모든 `(i, j)` 쌍의 이웃을 리스트로 반환합니다. 도시가 `n` 개면 이웃은 `n(n-1)/2` 개입니다. (힌트: `itertools.combinations(range(self.n), 2)`)
    5. 추가 코드 작성 없이 출력 결과를 확인하는 항목입니다. 출력 코드는 도시 20개 문제에서 무작위 경로의 비용과 SAHC-T, FCHC-T 의 결과를 차례로 출력합니다. SAHC-T는 TSP에 적용한 `steepest_ascent`, FCHC-T는 TSP에 적용한 `first_choice` 입니다. FCHC-T는 개선에 `limit_stuck=200` 번 연속 실패하면 멈춥니다. `random_mutant` 는 제공합니다.

`distance_matrix` 의 `return table`, `evaluate` 의 `return round(total, 6)` 은 남기세요. `inversion` 의 자리표시 `return current[:]`, `mutants` 의 자리표시 `return []` 는 지우고 작성하세요. 출력의 처음 7줄에 나오는 값은 출력 코드의 해당 식을 보고 확인하세요. `show` 는 한 줄에 비용, 평가 횟수, 이동 횟수를 출력합니다.

제공 코드와 출력 코드는 수정하지 마세요. 출력한 값으로 채점하므로, 제출 전에 직접 넣은 `print` 는 지우세요.

## Practice Problem 4: Applying the Same Algorithms to TSP

TSP finds the shortest tour that visits every city exactly once and returns to the starting city. A state is a permutation of city numbers, and `[2, 0, 3, 1]` is the tour that goes through cities 2, 0, 3, and 1 and returns to 2. A permutation cannot use `±delta`, so a neighbor is built by reversing one section of the tour (inversion). The algorithms `steepest_ascent` and `first_choice` in the provided code are unchanged from the numerical problem. (Theory Chapters 4 and 5)

- **Requirements:**
    1. Complete `distance_matrix(locations)`. It returns an `n x n` list where `table[i][j]` is the distance between cities `i` and `j`. (Hint: `math.hypot(x1 - x2, y1 - y2)`)
    2. Complete `evaluate(order)`. Compute the total distance along the tour in `total`, including the distance from the last city back to the starting city. Do not remove the `round` on the last line.
    3. Complete `inversion(current, i, j)`. It returns a new permutation with the section from index `i` to `j`, including both endpoints, reversed. It does not change `current`. (Hint: `neighbor[i:j + 1] = neighbor[i:j + 1][::-1]`)
    4. Complete `mutants(current)`. It returns a list of the neighbors for every pair `(i, j)` with `i < j`. With `n` cities there are `n(n-1)/2` neighbors. (Hint: `itertools.combinations(range(self.n), 2)`)
    5. This item asks you to inspect the output; no additional code is needed. On the 20-city problem, the output code prints, in order, the cost of a random tour and the results of SAHC-T and FCHC-T. SAHC-T is `steepest_ascent` applied to TSP, and FCHC-T is `first_choice` applied to TSP. FCHC-T stops after `limit_stuck=200` consecutive failures to improve. `random_mutant` is provided.

Keep `return table` in `distance_matrix` and `return round(total, 6)` in `evaluate`. Replace the placeholder `return current[:]` in `inversion` and `return []` in `mutants` with your code. Read the corresponding expressions in the output code to see which values the first 7 lines print. `show` prints the cost, the number of evaluations, and the number of moves on one line.

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

# 제공 코드 끝. / End of provided code.

# TODO: distance_matrix 의 return table, evaluate 의 return round(total, 6) 은 남기세요.
#       inversion 의 return current[:] 와 mutants 의 return [] 는 지우고 작성하세요.
# TODO: Keep return table in distance_matrix and return round(total, 6) in evaluate.
#       Replace return current[:] in inversion and return [] in mutants with your code.

def distance_matrix(locations):
    n = len(locations)
    table = [[0.0] * n for _ in range(n)]
    # TODO: table[i][j] 에 도시 i 와 j 사이의 거리를 담으세요.
    # TODO: Store the distance between cities i and j in table[i][j].
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
        # TODO: order 를 따라 이동한 총 거리를 total 에 구하세요. 마지막 도시에서 출발 도시로 돌아오는 거리도 더하세요.
        # TODO: Compute the total distance along order in total, including the distance from the last city back to the first.
        return round(total, 6)    # 같은 길이의 경로 간 부동소수점 오차 방지 / Avoid floating-point differences between equal-length tours.

    def inversion(self, current, i, j):
        # TODO: 양 끝 인덱스 i, j 를 포함한 구간을 뒤집은 새 순열을 반환하세요. current 는 바꾸지 마세요.
        # TODO: Return a new permutation with the section from i to j, including both endpoints, reversed. Do not change current.
        return current[:]

    def mutants(self, current):
        # TODO: i < j 인 모든 (i, j) 쌍의 이웃을 리스트로 반환하세요.
        # TODO: Return a list of the neighbors for every pair (i, j) with i < j.
        return []

    def random_mutant(self, current):
        i, j = sorted(int(v) for v in self.rng.choice(self.n, 2, replace=False))
        return self.inversion(current, i, j)

# 출력 코드: 수정하지 마세요. / Output code: do not modify.
def show(result):
    state, value, evals, path = result
    print(round(float(value), 2), evals, len(path) - 1)


tri = TspProblem(distance_matrix([(0, 0), (3, 0), (0, 4)]))
print(float(tri.dist[0][1]), float(tri.dist[0][2]), float(tri.dist[1][2]), float(tri.dist[2][2]))
print(float(tri.evaluate([0, 1, 2])))

rect = TspProblem(distance_matrix([(0, 0), (4, 0), (4, 3), (0, 3)]))
print(float(rect.evaluate([0, 1, 2, 3])), float(rect.evaluate([0, 2, 1, 3])))

hexa = TspProblem(distance_matrix([(0, 0), (1, 0), (2, 0), (2, 1), (1, 1), (0, 1)]))
sample = list(range(6))
print(hexa.inversion(sample, 2, 4))
print(hexa.inversion(sample, 0, 5))
print(sample)
neighbors = hexa.mutants(sample)
print(len(neighbors), len(set(tuple(nb) for nb in neighbors)), sample in neighbors)

NUM_CITIES = 20
city_rng = np.random.default_rng(11)
locations = [tuple(int(v) for v in city_rng.integers(0, 101, size=2)) for _ in range(NUM_CITIES)]
dist = distance_matrix(locations)

random_problem = TspProblem(dist, seed=0)
print(round(float(random_problem.evaluate(random_problem.random_init())), 2))
show(steepest_ascent(TspProblem(dist, seed=0)))
show(first_choice(TspProblem(dist, seed=0), limit_stuck=200))
