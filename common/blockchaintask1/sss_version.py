import random


PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481


def get_polynomial_value(coefficients, x):
    result = 0
    power = 0
    for coef in coefficients:
        result += (coef * pow(x, power, PRIME)) % PRIME
        result %= PRIME
        power += 1
    return result


def make_shares(secret, k, n):
    coefficients = [secret]
    for i in range(k - 1):
        coefficients.append(random.randint(0, PRIME - 1))

    shares = []
    for i in range(1, n + 1):
        x = i
        y = get_polynomial_value(coefficients, x)
        shares.append((x, y))
    return shares


def recover_secret(shares):
    total = 0
    for j, (xj, yj) in enumerate(shares):
        numerator = 1
        denominator = 1
        for m, (xm, _) in enumerate(shares):
            if m != j:
                numerator *= -xm
                denominator *= (xj - xm)
                numerator %= PRIME
                denominator %= PRIME
        lagrange = numerator * pow(denominator, -1, PRIME)
        lagrange %= PRIME
        total += yj * lagrange
        total %= PRIME
    return total


if __name__ == "__main__":
    secret_number = 123456789  
    k = 3  
    n = 5  

    print("Welcome to Polynomic Vault!")
    print("Original secret:", secret_number)

    all_shares = make_shares(secret_number, k, n)
    print("\n--- All Generated Shares ---")
    for share in all_shares:
        print("Share:", share)

  
    chosen = random.sample(all_shares, k)
    print("\n--- Chosen Shares for Recovery ---")
    for share in chosen:
        print("Using Share:", share)

    recovered = recover_secret(chosen)
    print("\nRecovered Secret is:", recovered)

    if recovered == secret_number:
        print("Yay! Secret recovered successfully :)")
    else:
        print("Oops! Something went wrong :(")
