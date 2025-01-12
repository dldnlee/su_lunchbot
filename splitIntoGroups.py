import random

def split_into_groups(usernames, num_groups):
    random.shuffle(usernames)
    groups = [[] for _ in range(num_groups)]
    for index, username in enumerate(usernames):
        groups[index % num_groups].append(username)
    return groups