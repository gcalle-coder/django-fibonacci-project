def fibonacci_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_custom(n):
    tot = [0, 1]
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        for i in range(n):
            tot.append(tot[-1] + tot[-2])
        # print(tot)
        return tot[n]


def fibonacci_optimized(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


# if __name__ == "__main__":
#    res = fibonacci_custom(4)
#    print(res)
