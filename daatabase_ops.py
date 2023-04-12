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
    results = cur.fetchall()
    connection.close()
    return results

def update_service(id, service_name):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'UPDATE service SET service_name= ? where service_id = ?'
    cur.execute(sql_q, (service_name, id))
    results = cur.fetchall()
    connection.close()
    return results


def delete_service(id):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'DELETE FROM service WHERE service_id=?'
    cur.execute(sql_q, (id,))
    results = cur.fetchall()
    connection.close()
    return results