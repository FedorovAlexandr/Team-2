def int_to_words(n):
    """Convert an integer n to English words."""

    ones = ['zero', 'one', 'two', 'three', 'four',
            'five', 'six', 'seven', 'eight', 'nine',
            'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
            'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
    tens = ['zero', 'ten', 'twenty', 'thirty', 'forty',
            'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    # 1000+
    for order, word in [(10**6, "million"), (10**3, "thousand")]:
        if n >= order:
            return "{0} {1}{2}".format(int_to_words(n // order), word,
                                       " {0}".format(int_to_words(n % order))
                                       if n % order else "")
    # 100-999
    if n >= 100:
        if n % 100:
            return "{0} hundred and {1}".format(int_to_words(n // 100),
                                                int_to_words(n % 100))
        else:
            return "{0} hundred".format(int_to_words(n // 100))
    # 0-99
    if n < 20:
        return ones[n]
    else:
        return "{0}{1}".format(tens[n // 10],
                               "-{0}".format(int_to_words(n % 10))
                               if n % 10 else "")
int_to_words(44)
