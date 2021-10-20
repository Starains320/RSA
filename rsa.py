import base64
import random


# 扩展欧几里得除法
def euc_div(a, b):
    if b > a:
        a, b = b, a
    if b == 0:
        return 1, 0, a
    else:
        s, t, gcd = euc_div(b, a % b)
        s, t = t, (s - (a // b) * t)
        return s, t, gcd


# 平方乘算法
def quick_mod(base, power, mod):
    base = base % mod
    ans = 1
    power = int(power)
    while power != 0:
        if (power & 1) == 1:
            ans = (ans * base) % mod
        power >>= 1
        base = pow(base, 2) % mod
    return ans


# miller-rabin 素性检验
def witness(a, n):
    d = n - 1
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    while d % 2 == 0:
        d = int(d / 2)
    t = quick_mod(a, d, n)
    while d != n - 1 and t != 1 and t != n - 1:
        t = quick_mod(t, 2, n)
        d <<= 1
    return t == n - 1 or d & 1


def isPrime(p):
    k = 5
    while k > 0:
        a = random.randint(1, p - 1)
        if not witness(a, p):
            return False
        k = k - 1
    return True


def CRT(c, d, n, p, q):
    if p < q:
        p, q = q, p
    b1 = quick_mod(c, d, p)
    b2 = quick_mod(c, d, q)
    m1 = (euc_div(q, p)[1] + p) % p
    m2 = (euc_div(p, q)[0] + q) % q
    return (b1 * q * m1 + b2 * p * m2) % n


# 得到随机大素数p,q
def get_pq():
    pq_list = []
    while len(pq_list) < 2:
        n = random.randint(pow(2, 53), pow(2, 54))
        if n % 2 == 0:
            n += 1
        while 1:
            if isPrime(n) and n not in pq_list:
                break
            n += 2
        pq_list.append(n)
    return pq_list[0], pq_list[1]


def encrypt(m, e, n):
    return quick_mod(m, e, n)


def decrypt(c, d, n):
    return quick_mod(c, d, n)


def main():
    p, q = get_pq()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    a = euc_div(phi, e)
    d = (a[1] + phi) % phi
    print("p=%d\nq=%d\ns*phi+t*e=%d\ned mod phi=%d" % (p, q, phi * a[0] + e * a[1], (e * d) % phi))
    m1 = int(input("请输入明文"))
    # m1 = 110108200203206032\
    c = encrypt(m1, e, n)
    print("密文是：%d" % c)
    m21 = decrypt(c, d, n)
    print("解密后的明文是：%d" % m21)
    m22 = CRT(c, d, n, p, q)
    print("中国剩余定理优化解密后的明文是：%d" % m22)

if __name__ == '__main__':
    main()
