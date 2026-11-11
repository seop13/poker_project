"""족보 판정 모듈

점수는 (족보 등급, 비교용 숫자 리스트) 형태의 튜플이다.
튜플끼리는 앞에서부터 비교되므로, 점수가 크면 더 센 패다.
예) (2, [13, 7, 2]) = K와 7 투페어, 키커 2
"""
from collections import Counter
from itertools import combinations

HAND_NAMES = {
    9: '로열 플러시',
    8: '스트레이트 플러시',
    7: '포카드',
    6: '풀하우스',
    5: '플러시',
    4: '스트레이트',
    3: '트리플',
    2: '투페어',
    1: '원페어',
    0: '하이카드',
}


def _straight_high(values):
    """5장이 스트레이트면 가장 높은 숫자를, 아니면 None을 돌려준다"""
    unique = sorted(set(values), reverse=True)
    if len(unique) != 5:
        return None
    if unique[0] - unique[4] == 4:
        return unique[0]
    if unique == [14, 5, 4, 3, 2]:  # A-2-3-4-5 (A를 1로 사용)
        return 5
    return None


def evaluate_five(cards):
    """카드 5장의 점수를 계산한다"""
    values = sorted((card.value for card in cards), reverse=True)
    suits = [card.suit for card in cards]

    # 같은 숫자가 몇 장인지 센 다음, 장수가 많은 순 -> 숫자가 큰 순으로 정렬
    counts = Counter(values)
    groups = sorted(counts.items(), key=lambda item: (item[1], item[0]), reverse=True)
    ordered = [value for value, count in groups]  # 비교할 숫자 순서
    shape = [count for value, count in groups]    # 예: 투페어 -> [2, 2, 1]

    is_flush = len(set(suits)) == 1
    straight_high = _straight_high(values)

    if is_flush and straight_high:
        return (9 if straight_high == 14 else 8, [straight_high])
    if shape == [4, 1]:
        return (7, ordered)
    if shape == [3, 2]:
        return (6, ordered)
    if is_flush:
        return (5, values)
    if straight_high:
        return (4, [straight_high])
    if shape == [3, 1, 1]:
        return (3, ordered)
    if shape == [2, 2, 1]:
        return (2, ordered)
    if shape == [2, 1, 1, 1]:
        return (1, ordered)
    return (0, values)


def best_hand(cards):
    """7장 중에서 가장 센 5장 조합의 점수를 돌려준다"""
    return max(evaluate_five(combo) for combo in combinations(cards, 5))


def hand_name(score):
    """점수에서 족보 이름을 꺼낸다"""
    return HAND_NAMES[score[0]]
