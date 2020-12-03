def fact(n):
    print(n)
    if n == 0:
        return 1
    ans =  n * fact(n-1)
    print("RETURNING:", ans)
    return ans

print(fact(5))