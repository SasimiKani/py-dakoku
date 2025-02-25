#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
from src.conn import *

form = cgi.FieldStorage()
id = form.getvalue("id", "")

print("Content-Type: text/html; charset=UTF-8")
body = f"""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>認証</title>
	<link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon">
	<link rel="stylesheet" href="/css/style.css">
</head>
<body>
	<main>
		<h1>ログイン</h1>
		<form action="./home.py" method="post">
			<input type="number" name="id" value="{id}" placeholder="ID(整数)" required>
			<input type="password" name="password" placeholder="パスワード" required>
			<input type="submit" value="ログイン">
		</form>
		<a href="./signup.py">未登録の人：サインアップ</a>
	</main>
</body>
</html>

"""

print(body)