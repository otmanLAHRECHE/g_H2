import sqlite3



def load_services():
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'SELECT * FROM service'
    cur.execute(sql_q)
    results = cur.fetchall()
    connection.close()
    return results


def create_service(service_name):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'INSERT INTO service (service_name) values (?)'
    cur.execute(sql_q, (service_name,))
    connection.commit()
    connection.close()

def update_service(id, service_name):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'UPDATE service SET service_name= ? where service_id = ?'
    cur.execute(sql_q, (service_name, id))
    connection.commit()
    connection.close()


def delete_service(id):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'DELETE FROM service WHERE service_id=?'
    cur.execute(sql_q, (id,))
    connection.commit()
    connection.close()


def get_service_id_from_name(service_name):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'SELECT service_id FROM service where service_name=?'
    cur.execute(sql_q, (service_name,))
    results = cur.fetchall()
    connection.close()
    return results