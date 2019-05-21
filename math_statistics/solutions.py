from collections import defaultdict

import matplotlib.pyplot as plt

with open('data', 'r') as f:
    data = []
    for line in f.readlines():
        data.extend([int(x) for x in line.split()])

print("Вихідні дані:")
print(" ".join([str(x) for x in data]))


print()
print("Обсяг вибірки:", len(data))

print()
print("Варіаційний ряд:")
variance = defaultdict(int)
for item in data:
    variance[item] += 1

for item in variance.keys():
    variance[item] /= len(data)

for k, v in sorted(variance.items()):
    print(f"{k}, {v:.02f}")

items, values = zip(*sorted(variance.items()))

plt.title("Полігон частот")
plt.plot(items, values, 'r-')
plt.axis([1, 8, 0, 1])
plt.show()

print()
print("Емпірична функція розподілу:")
distribution = {}
for i in range(1, 9):
    distribution[i] = sum(values[:i])

for k, v in sorted(distribution.items()):
    print(f"{k}, {v:.02f}")

items, values = zip(*sorted(distribution.items()))

plt.title("Емпірична функція розподілу")
plt.plot(items, values, 'b-')
plt.axis([1, 8, 0, 1])
plt.show()

print()
median = sum(items) / 2
print("Медіана:", median)

max_count = max([data.count(v) for v in items])
mode = [v for v in items if data.count(v) == max_count]
print("Мода:", mode)
