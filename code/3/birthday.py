def has_duplicates(birthdays):
    d = dict()
    for b in birthdays:
        #print(str(b))
        if b not in d:
            d[b] = 1
        else:
            #d[b] += 1
			return True
	return False