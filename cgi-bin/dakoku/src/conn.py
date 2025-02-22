import psycopg2
connection = None

def connect():
	global connection
	connection = psycopg2.connect("host=localhost port=5432 dbname=dakoku user=natura password=natura")
	connection.get_backend_pid()

def refExecute(query):
	res = None
	if query.find("select") != -1:
		connect()
		cur = connection.cursor()
		try:
			stat = query
			cur.execute(stat)
			res = cur.fetchall()
		except:
			rollback()
		finally:
			cur.close()
			close()
			return res
	else:
		close()
		return res

def insertExecute(query):
	if query.find("insert") != -1:
		connect()
		cur = connection.cursor()
		try:
			stat = query
			cur.execute(stat)
			commit()
		except:
			rollback()
		finally:
			cur.close()
			close()
	else:
		close()

def updateExecute(query):
	if query.find("update") != -1:
		connect()
		cur = connection.cursor()
		try:
			stat = query
			cur.execute(stat)
			commit()
		except:
			rollback()
		finally:
			cur.close()
			close()
	else:
		close()

def deleteExecute(query):
	if query.find("delete") != -1:
		connect()
		cur = connection.cursor()
		try:
			stat = query
			cur.execute(stat)
			commit()
		except:
			rollback()
		finally:
			cur.close()
			close()
	else:
		close()

def selectAll(table):
	connect()
	cur = connection.cursor()
	try:
		cur.execute(stat)
	except:
		rollback()
	finally:
		cur.close()
		close()

def dropTable(table):
	connect()
	cur = connection.cursor()
	try:
		cur.execute(stat)
		commit()
	except:
		rollback()
	finally:
		cur.close()
		close()

def commit():
	connection.commit()

def rollback():
	connection.rollback()

def close():
	connection.close()
