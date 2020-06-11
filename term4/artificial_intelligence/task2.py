import os
from collections import defaultdict, deque


ROUTES = {
    "Брест": {"Вільнюс": 531, "Вітебськ": 638, "Калінінград": 699},
    "Волгоград": {"Вороніж": 581, "Вітебськ": 1455, "Житомир": 1493},
    "Вороніж": {"Волгоград": 581, "Вітебськ": 869, "Ярославль": 739},
    "Вільнюс": {"Брест": 531, "Вітебськ": 360, "Даугавпілс": 211, "Калінінград": 333, "Каунас": 102, "Київ": 734},
    "Вітебськ": {
        "Брест": 638,
        "Волгоград": 1455,
        "Вороніж": 869,
        "Вільнюс": 360,
        "Нижній_Новгород": 911,
        "Орел": 522,
        "Санкт-Петербург": 602,
    },
    "Даугавпілс": {"Вільнюс": 211},
    "Донецьк": {"Житомир": 863, "Кишинів": 812, "Москва": 1084, "Орел": 709},
    "Житомир": {"Волгоград": 1493, "Донецьк": 863, "Київ": 131},
    "Казань": {"Москва": 815, "Уфа": 525},
    "Калінінград": {"Брест": 699, "Вільнюс": 333, "Санкт-Петербург": 739},
    "Каунас": {"Вільнюс": 102, "Рига": 267},
    "Кишинів": {"Донецьк": 812, "Київ": 467},
    "Київ": {"Вільнюс": 734, "Житомир": 131, "Кишинів": 467, "Одеса": 487, "Харків": 471},
    "Москва": {
        "Донецьк": 1084,
        "Казань": 815,
        "Мінськ": 690,
        "Нижній_Новгород": 411,
        "Орел": 368,
        "Санкт-Петербург": 664,
    },
    "Мурманськ": {"Мінськ": 2238, "Санкт-Петербург": 1412},
    "Мінськ": {"Москва": 690, "Мурманськ": 2238, "Ярославль": 940},
    "Нижній_Новгород": {"Вітебськ": 911, "Москва": 411},
    "Одеса": {"Київ": 487},
    "Орел": {"Вітебськ": 522, "Донецьк": 709, "Москва": 368},
    "Рига": {"Каунас": 267, "Санкт-Петербург": 641, "Таллінн": 308},
    "Самара": {"Уфа": 461},
    "Санкт-Петербург": {"Вітебськ": 602, "Калінінград": 739, "Москва": 664, "Мурманськ": 1412, "Рига": 641},
    "Сімферополь": {"Харків": 639},
    "Таллінн": {"Рига": 308},
    "Уфа": {"Казань": 525, "Самара": 461},
    "Харків": {"Київ": 471, "Сімферополь": 639},
    "Ярославль": {"Вороніж": 739, "Мінськ": 940},
}


def bfs(graph, start, end):

    if start == end:
        return [[start]]

    path_queue = deque([[start]])

    while path_queue:
        path = path_queue.popleft()

        # stop exploring path if the goal node reached
        if path[-1] == end:
            return path

        neighbours = graph[path[-1]]

        for neighbour in neighbours:
            if neighbour not in path:
                path_queue.append(path + [neighbour])


def dfs(graph, start, end, path: list = None, max_depth: int = None):
    max_depth = max_depth if max_depth is not None else len(graph)
    path = path or [start]

    if len(path) > max_depth + 1:
        return []

    if start == end:
        return path

    for neighbor in graph[start]:
        if neighbor not in path:
            result = dfs(graph, neighbor, end, path + [neighbor], max_depth)

            if result:
                return result


def scored_bfs(graph, start, end):

    if start == end:
        return [([start], 0)]

    path_queue = deque([([start], 0)])

    while path_queue:
        path, score = path_queue.popleft()

        # stop exploring path if the goal node reached
        if path[-1] == end:
            return path, score

        neighbours = graph[path[-1]]

        for neighbour, distance in neighbours.items():
            if neighbour not in path:
                path_queue.append((path + [neighbour], score + distance))


def scored_dfs(graph, start, end, path: list = None, score: int = 0, max_depth: int = None):
    max_depth = max_depth if max_depth is not None else len(graph)
    path = path or [start]

    if len(path) > max_depth + 1:
        return []

    if start == end:
        return path, score

    for neighbor, distance in graph[start].items():
        if neighbor not in path:
            result = scored_dfs(graph, neighbor, end, path + [neighbor], score + distance, max_depth)

            if result:
                return result


def iddfs(graph, start, end):
    for depth in range(len(graph)):
        result = dfs(graph, start, end, max_depth=depth)

        if result:
            return result


def greedy_search(graph, start, end):
    pass


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), "routes.txt")) as f:
        data = [line.strip().split(" ") for line in f.readlines()]

    routes = defaultdict(dict)
    for city1, city2, distance in data:
        routes[city1][city2] = int(distance)
        routes[city2][city1] = int(distance)

    bfs_res = bfs(routes, "Санкт-Петербург", "Житомир")
    dfs_res = dfs(routes, "Санкт-Петербург", "Житомир")
    rdfs_res = dfs(routes, "Санкт-Петербург", "Житомир", max_depth=4)
    iddfs_res = iddfs(routes, "Санкт-Петербург", "Житомир")

    print(bfs_res)
    print(dfs_res)
    print(rdfs_res)
    print(iddfs_res)
