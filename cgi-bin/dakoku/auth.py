#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
from src.conn import *

form = cgi.FieldStorage()
id = form.getvalue("id", "")

body = f"""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>認証</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
	<main>
		<h1>ログイン</h1>
		<form action="./home.py" method="post">
			<input type="number" name="id" value="{id}" placeholder="ID" required>
			<input type="password" name="password" placeholder="パスワード" required>
			<input type="submit" value="ログイン">
		</form>
	</main>
</body>
</html>

"""

print(body)
