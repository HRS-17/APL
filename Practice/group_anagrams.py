def group_anagrams(words):
    groups = {}
    for word in words:
        # sort the letters in the word to create a key
        key = ''.join(sorted(word))
        if key in groups:
            groups[key].append(word)
        else:
            groups[key] = [word]
    # return only the grouped values
    print(groups)
    return list(groups.values())

# Example usage
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams(words))
