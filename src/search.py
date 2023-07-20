from database import LiteDatabase

db = LiteDatabase()

search_query = "schema mysql database"


def get_keys_from_dict(source_dict):
    return [key for key, value in source_dict.items()]


def search(query):
    words = query.split()

    results = [db.search(word) for word in words]

    if len(results) == 1:
        return get_keys_from_dict(results[0])

    intersect = results[0]
    for i in range(1, len(results)):
        intersect = {x: intersect[x] for x in intersect if x in results[i]}

    return get_keys_from_dict(intersect)


search_result = search(search_query)
