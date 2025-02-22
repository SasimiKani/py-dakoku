#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
from hashlib import sha512
from src.conn import *

form = cgi.FieldStorage()
id = form.getvalue("id", "")
password = form.getvalue("password", "")

# 認証情報を取得
auth = refExecute(f"select password from password where ID = {id};")

if len(auth) > 0:
	if len(auth) == 0:
		body = f"""
		<form action="./signup.py" method="post">
			<input type="hidden" name="id" value="{id}は使われてます">
		</form>
		<script>
		document.forms[0].submit();
		</script>
		"""
		
		print(body)

# ハッシュ化
if password != "":
	hash = sha512(password.encode()).hexdigest()

# 登録
insertExecute(f"insert into password values({id}, '{hash}');")

body = f"""
<!DOCTYPE html>
<html>
<head>
	<title>登録</title>
</head>
<body>
	<form action="./home.py" method="post">
		<input type="hidden" name="id" value="{id}">
		<input type="hidden" name="hash" value="{hash}">
	</form>
	
	<script>
	document.forms[0].submit();
	</script>
</body>
</html>

"""

print(body)