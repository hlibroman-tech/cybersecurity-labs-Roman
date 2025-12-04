# ВАРІАНТ 1: ВРАЗЛИВИЙ
user_input = request.GET['category']
sql_query = "SELECT * FROM products WHERE category = '" + user_input + "'"
cursor.execute(sql_query)

# ВАРІАНТ 2: БЕЗПЕЧНИЙ
user_input = request.GET['category']
sql_query = "SELECT * FROM products WHERE category = ?"
cursor.execute(sql_query, (user_input,))