from database import LiteDatabase

db = LiteDatabase()

search_query = "schema mysql database"


def search(query):
    words = query.split()

    results = [db.search(word) for word in words]

    if len(results) == 1:
        return results[0]

    intersect = results[0]
    for i in range(1, len(results)):
        intersect = {x: intersect[x] for x in intersect if x in results[i]}

    return intersect


search_result = search(search_query)

