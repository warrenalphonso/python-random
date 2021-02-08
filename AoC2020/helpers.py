def data(day: int, parser=str, sep="\n") -> list: 
    """Split day's input file into sections separated by `sep`, and apply 
    parser to each. From Norvig."""
    with open(f"data/{day}.txt") as f:
        sections = f.read().rstrip().split(sep)
        return list(map(parser, sections))

def first(iterable, default=None) -> object:
    "Return first item in iterable, or default."
    return next(iter(iterable), default)

def quantify(iterable, pred=bool) -> int:
    return sum(1 for i in iterable if pred(i))
