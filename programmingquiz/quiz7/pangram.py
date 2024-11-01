def pangram(s):
    s=s.lower()
    s1 = set()

    for i in s:
        if not i.isalpha():
            continue
        s1.add(i)
    if len(s1)==26:
        return True
    else:
        return False
print(pangram("the quick brown fox jumps over the lazy dog")) 
