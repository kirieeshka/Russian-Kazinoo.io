import random

money = 10
a = ["банан", "банан", "банан", "арбуз", "арбуз", "арбуз", "вишня", "вишня", "клубника", "клубника", "7"]
s = random.choice(a)
d = random.choice(a)
q = random.choice(a)
if s == "банан" and s == d == q or s == "арбуз" and s == d == q:
    money = 50 * money
    print(s, d, q, money)
elif s == "вишня" and s == d == q or s == "клубника" and s == d == q:
    money = money * 100
    print(s, d, q, money)
elif s == "7" and s == d == q:
    money = money * 1000
    print(s, d, q, money)
else:
    money = 0 + 5
print(money)