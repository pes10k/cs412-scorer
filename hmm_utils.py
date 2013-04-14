def trim_starts(tags):
    while (len(tags) > 1 and tags[0] == "START" and tags[1] == "START"):
        tags = tags[1:]
    return tags
