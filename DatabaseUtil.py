def get_all_words():
    with open('database/words.txt','r') as f:
        words = f.read().splitlines()
    return [w.strip().upper() for w in words]