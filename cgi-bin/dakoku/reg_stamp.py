#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
print("Content-Type: text/html; charset=UTF-8")

from hashlib import sha512
from src.conn import *

form = cgi.FieldStorage()
password = form.getvalue("password", "")
hash = form.getvalue("hash", "")
id = form.getvalue("id", "")
waking = form.getvalue("waking", "")

if password != "":
	hash = sha512(password.encode()).hexdigest()

# 認証情報を取得
auth = refExecute(f"select password from password where ID = {id};")

# 未認証の場合はパスワード入力に遷移
if id != "":
	# 未登録の場合は登録
	if len(auth) == 0:
		body = f"""
		<form action="./signup.py" method="post">
			<input type="hidden" name="id" value="{id}">
		</form>
		<script>
		document.forms[0].submit();
		</script>
		"""
		
		print(body)
		exit()

	# 認証
	elif hash == "" or auth[0][0] != hash:
		body = f"""
		<form action="./auth.py" method="post">
			<input type="hidden" name="id" value="{id}">
		</form>
		<script>
		document.forms[0].submit();
		</script>
		"""
		
		print(body)
		exit()

	sql = ""
	if waking == "wakeup":
		sql = f"insert into stamp values ({id}, 0, now());"
	elif waking == "sleep":
		sql = f"insert into stamp values ({id}, 1, now());"

if waking != "":
	insertExecute(sql)

body = f"""
<form action="./home.py" method="post">
	<input type="hidden" name="hash" value="{hash}">
	<input type="hidden" name="id" value="{id}">
</form>
<script>
document.forms[0].submit();
</script>
"""

print(body)