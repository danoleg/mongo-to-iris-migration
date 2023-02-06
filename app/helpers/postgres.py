def get_table_data(table, cur, limit: int = None):

    limit_subquery = ""
    if limit:
        limit_subquery = f"LIMIT {limit}"
    try:
        cur.execute(f"SELECT count(*) FROM {table};")
        count = cur.fetchone()

        cur.execute(f"SELECT * FROM {table} {limit_subquery};")
        row_data = cur.fetchall()
    except Exception as e:
        return False, 0, None

    field_names = [i[0] for i in cur.description]
    collection = {}
    counter = 0

    for i in row_data:
        item = {}
        for field, value in list(map(lambda x, y:(x,y), field_names, list(i))):
            item[field] = value
        collection[counter] = item
        counter += 1

    return collection, count[0], field_names, row_data