def modify_lists():
    original = [1, 2, 3]
    reference = original
    copy = original[:]
    reference.append(4)
    print(original)
    print(copy)
    print(reference)
    return len(original), len(copy)
print(modify_lists())