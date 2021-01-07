def find_generator(safe_prime):

    q = (safe_prime-1)//2
    i = 0

    for alpha in range(2, safe_prime-1):
        i = i+1

        if (alpha ** 2 % safe_prime) == 1:
            continue

        if fast_exponentiation(alpha, q, mod=safe_prime) == 1:
            continue

        return alpha