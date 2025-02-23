#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
from src.conn import *

form = cgi.FieldStorage()
id = form.getvalue("id", "")
msg = form.getvalue("msg", "")

body = f"""
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>サインアップ</title>
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
	<main>
		<h1>新規登録</h1>
		<form action="./regist.py" method="post">
            <input type="number" name="id" value="{id}" placeholder="ID(整数)" equired>
			<input type="password" name="password" placeholder="パスワード" required>
			<input type="password" name="password_conf" placeholder="パスワード確認" required>
			<input type="submit" value="登録" onclick="return regist();">
			<div id="msg">{msg}</div>
		</form>
        <a href="./auth.py">登録済みの人：ログイン</a>
	</main>
	<script>
	function regist() {{
		var form = document.forms[0];
		var password = form.querySelector("[name=password]").value;
		var password_conf = form.querySelector("[name=password_conf]").value;
		
		if (password != password_conf) {{
			document.querySelector("#msg").innerText = "パスワードが一致しない";
			return false;
		}}
		
		return true;
	}}
	</script>
</body>
</html>

"""

print(body)
