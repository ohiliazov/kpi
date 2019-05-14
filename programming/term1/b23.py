"""
Завдання №23.
Визначити, чи є задане шестизначне число “щасливим” (сума перших трьох цифр має дорівнювати сумі останніх трьох цифр)?
"""

while True:
    try:
        n = input("Введіть шестизначне число: ")

        assert len(n) == 6
        int(n)

        break

    except (AssertionError, ValueError):
        print("Ви ввели не шестизначне число.")

left = right = 0

for i in range(6):

    if i < 3:
        left += int(n[i])
    else:
        right += int(n[i])

if left > 9:
    left = left // 10 + left % 10

if right > 9:
    right = right // 10 + right % 10

if left == right:
    print("Це щасливе число.")
else:
    print("Це нещасливе число.")
