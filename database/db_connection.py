import psycopg2


def connect_db():
    connection = psycopg2.connect(
        host="localhost",
        database="lagos_home_finder",
        user="postgres",
        password="NgwabaSQL2008",
        port="5432"
    )

    return connection