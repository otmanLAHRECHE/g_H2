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

def get_service_name_from_id(service_id):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'SELECT service_name FROM service where service_id=?'
    cur.execute(sql_q, (service_id,))
    results = cur.fetchall()
    connection.close()
    return results


def load_workers():
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'SELECT * FROM worker'
    cur.execute(sql_q)
    results = cur.fetchall()
    connection.close()
    return results

def create_worker(first_name, last_name, service_id):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'INSERT INTO worker (first_name, last_name, service_id) values (?,?,?)'
    cur.execute(sql_q, (first_name, last_name, service_id))
    connection.commit()
    connection.close()

def update_worker(id, worker_id, first_name, last_name):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'UPDATE worker SET first_name= ? and last_name= ? where worker_id = ?'
    cur.execute(sql_q, (first_name, last_name, worker_id))
    connection.commit()
    connection.close()


def delete_worker(id):
    connection = sqlite3.connect("data/database.db")
    cur = connection.cursor()
    sql_q = 'DELETE FROM worker WHERE worker_id=?'
    cur.execute(sql_q, (id,))
    connection.commit()
    connection.close()
