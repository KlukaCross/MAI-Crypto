import time


class EllipticCurve:
    """An elliptic curve over a prime field.

    The field is specified by the parameter 'p'.
    The curve coefficients are 'a' and 'b'.
    """

    def __init__(self, p, a, b):
        self.p = p
        self.a = a % p
        self.b = b % p

        assert pow(2, p - 1, p) == 1
        assert (4 * a * a * a + 27 * b * b) % p != 0

    def is_on_curve(self, point):
        """Checks whether the given point lies on the elliptic curve."""
        if point is None:
            return True

        x, y = point
        return (y * y - x * x * x - self.a * x - self.b) % self.p == 0

    def add(self, point1, point2):
        """Returns the result of point1 + point2 according to the group law."""
        assert self.is_on_curve(point1)
        assert self.is_on_curve(point2)

        if point1 is None:
            return point2
        if point2 is None:
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 * x1 + self.a) * inverse_mod(2 * y1, self.p)
        else:
            m = (y1 - y2) * inverse_mod(x1 - x2, self.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % self.p,
                  -y3 % self.p)

        assert self.is_on_curve(result)

        return result

    def double(self, point):
        """Returns 2 * point."""
        return self.add(point, point)

    def neg(self, point):
        """Returns -point."""
        if point is None:
            return None

        x, y = point
        result = x, -y % self.p

        assert self.is_on_curve(result)

        return result

    def mult(self, n, point):
        """Returns n * point computed using the double and add algorithm."""
        if n < 0:
            return self.neg(self.mult(-n, point))

        result = None
        addend = point

        while n:
            if n & 1:
                result = self.add(result, addend)
            addend = self.double(addend)
            n >>= 1

        return result

    def __str__(self):
        a = abs(self.a)
        b = abs(self.b)
        a_sign = '-' if self.a < 0 else '+'
        b_sign = '-' if self.b < 0 else '+'

        return 'y^2 = (x^3 {} {}x {} {}) mod {}'.format(
            a_sign, a, b_sign, b, self.p)


def inverse_mod(n, p):
    """Returns the inverse of n modulo p.

    This function returns the only integer x such that (x * n) % p == 1.

    n must be non-zero and p must be a prime.
    """
    if n == 0:
        raise ZeroDivisionError('division by zero')
    if n < 0:
        return p - inverse_mod(-n, p)

    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, n

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_s - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (n * x) % p == 1

    return x % p


def get_order_of_point(curve, point):
    p = point
    order = 0
    while p := curve.add(p, point):
        order += 1

    return order


def get_primes(n):
    is_prime = [True] * (n+1)
    primes = []
    for i in range(2, n+1):
        if is_prime[i]:
            for j in range(2*i, n+1, i):
                is_prime[j] = False
            primes.append(i)
    return primes


def get_first_n_points(curve, n):
    points = []
    for x in range(curve.p):
        for y in range(curve.p):
            if curve.is_on_curve((x, y)):
                points.append((x, y))
                if len(points) >= n:
                    return points


def main():
    n = int(input())
    a = int(input())
    b = int(input())
    required_time = int(input())  # in seconds
    prime_step = int(input())
    start_step = int(input())

    primes = get_primes(n)
    max_time = 0
    max_point = 0
    max_p = 0
    max_point_order = 0
    cur_i = start_step
    while max_time < required_time and cur_i < len(primes):
        p = primes[cur_i]
        curve = EllipticCurve(p, a, b)
        points = get_first_n_points(curve, 2)
        for point in points:
            start_time = time.time()
            point_order = get_order_of_point(curve, point)
            end_time = time.time()
            cur_time = end_time - start_time
            if max_time < cur_time:
                max_time = cur_time
                max_point = point
                max_p = p
                max_point_order = point_order
            print(f"p={p}, cur_time={cur_time}, point={point}")
        cur_i += prime_step

    print(f"a={a}, b={b}, p={max_p}, time={max_time} seconds, point order={max_point_order}, point={max_point}")


if __name__ == '__main__':
    main()
