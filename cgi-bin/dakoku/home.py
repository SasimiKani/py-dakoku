#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
print("Content-Type: text/html; charset=shift-jis")

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

def formatDelta(delta):
	if delta == None:
		return "-"
	
	# timedeltaオブジェクトから総秒数を取得
	total_seconds = int(delta.total_seconds())
	
	# 時・分・秒に変換
	hours = total_seconds // 3600
	minutes = (total_seconds % 3600) // 60
	seconds = total_seconds % 60
	
	# hh:mm:ss形式に整形
	formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
	
	return formatted_time

stamp = refExecute(f"select * from totalling({id});")
table = ""
if stamp != None:
	table = "".join(list( map(lambda row : f"""
	<tr>
		<td>{row[2].split(" ")[0]}</td>
		<td>{row[2].split(" ")[1]}</td>
		<td>{["起床", "入眠"][row[1]]}</td>
		<td>{formatDelta(row[3])}</td>
	</tr>
	""", stamp) ))

body = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="shift-jis">
	<title>寝起き打刻</title>
	<link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon">
	<link rel="stylesheet" href="/css/style.css">
</head>
<body>
	<main>
		<h1>ホーム</h1>
		<div>
			<form action="./home.py" method="post">
				<input type="hidden" name="hash" value="{hash}">
				<label>ID：</label>
				<input id="id_box" type="number" name="id" value="{id}" size="2">
				<input type="hidden" name="waking" value="">
				<input type="submit" value="参照" onclick="clickRef();">
				<input type="submit" value="グラフ" onclick="clickGraph();">
				<input type="submit" value="おはよう" onclick="clickWakeup();">
				<input type="submit" value="おやすみ" onclick="clickSleep();">
				<input type="hidden" value="参照・登録" onclick="clickRegist();">
			</form>
		</div>
		<div id="div_table">
			<table border="1">
				<tr>
					<th>日付</th>
					<th>時刻</th>
					<th>寝起き</th>
					<th>覚醒/睡眠時間</th>
				</tr>
				{table}
			</table>
		</div>
	</main>
	
	<script>
	if ("{id}" == "") {{
		document.querySelector('[value="参照"]').style.display = "none";
		document.querySelector('[value="グラフ"]').style.display = "none";
		document.querySelector('[value="おはよう"]').style.display = "none";
		document.querySelector('[value="おやすみ"]').style.display = "none";
		document.querySelector('[value="参照・登録"]').type = "submit";
	}}
	
	function clickRef() {{
		document.querySelector('[name=waking]').value='';
		document.forms[0].action='./home.py';
	}};
	function clickGraph() {{
		document.querySelector('[name=waking]').value='';
		document.forms[0].action='./graph.py';
	}};
	function clickWakeup() {{
		document.querySelector('[name=waking]').value='wakeup';
		document.forms[0].action='./reg_stamp.py';
	}};
	function clickSleep() {{
		document.querySelector('[name=waking]').value='sleep';
		document.forms[0].action='./reg_stamp.py';
	}};
	</script>
</body>
</html>
"""

print(body)