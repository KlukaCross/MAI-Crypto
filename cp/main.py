import matplotlib.pyplot as plt

from CompactFIPS202_numpy import SHA3_256


def diff_bits(text1, text2, rounds_number):
    hash1 = SHA3_256(text1, rounds_number)
    hash2 = SHA3_256(text2, rounds_number)

    hash1 = int.from_bytes(hash1, byteorder='big')
    hash2 = int.from_bytes(hash2, byteorder='big')

    diff = hash1 ^ hash2

    diff_bits_number = bin(diff).count("1")
    return diff_bits_number


def main():
    test1 = b'0'
    test2 = b'1'

    rounds = [i for i in range(1, 25)]
    diffs = [diff_bits(test1, test2, i) for i in rounds]

    plt.plot(rounds, diffs, "-r")
    plt.scatter(rounds, diffs)
    plt.xlabel('Количество раундов')
    plt.ylabel('Количество различных бит')
    plt.show()


if __name__ == "__main__":
    main()
