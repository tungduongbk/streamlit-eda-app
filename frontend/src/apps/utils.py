import math

__all__ = ("millify",)


def millify(n):
    mill_names = [" $", " K$", " M$", " B$", " T$"]

    n = float(n)
    mill_idx = max(0, min(len(mill_names) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))

    return "{:.2f}{}".format(n / 10 ** (3 * mill_idx), mill_names[mill_idx])
