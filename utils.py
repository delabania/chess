def get_range_between(start, finish, length):
    """
    get_range_between(1, 3, 1) = [2]
    get_range_between(5, 2, 2) = [4, 3]
    """
    if start == finish:
        return [start] * length
    assert length == abs(finish - start) - 1
    return range(start, finish, (finish - start) // (length + 1))[1:]