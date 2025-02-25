#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
from hashlib import sha512
import cgitb
import io
import base64
import datetime
import time
import matplotlib
matplotlib.use('Agg')  # GUI環境がない場合にAggバックエンドを使用
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
plt.rcParams['font.family'] = 'Noto Sans CJK JP'

from src.conn import *

# CGIのエラーメッセージ表示を有効にする
cgitb.enable()

form = cgi.FieldStorage()
hash = form.getvalue("hash", "")
id = form.getvalue("id", "")
base_date = form.getvalue("base_date", "")

type = form.getvalue("type", "")

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
else:
		body = f"""
		<form action="./auth.py" method="post">
			<input type="hidden" name="id" value="">
		</form>
		<script>
		document.forms[0].submit();
		</script>
		"""
		
		print(body)

if base_date == "":
	today = time.localtime()
	base_date = "%04d-%02d-%02d" % (today.tm_year, today.tm_mon, today.tm_mday)

# データ取得（WAKING: 0=起床, 1=入眠）
if type == "week":
	stamp = refExecute(f"select * from graph_data({id}, to_date('{base_date}', 'YYYY-MM-DD'));")
elif type == "month":
	stamp = refExecute(f"select * from graph_data_m({id}, to_date('{base_date}', 'YYYY-MM-DD'));")
else:
	stamp = refExecute(f"select * from graph_data({id}, to_date('{base_date}', 'YYYY-MM-DD'));")

cats = {0: "起床", 1: "入眠"}

# すべてのレコードを、日時（datetime）とともにリスト化する
records = []
for cat, date_str, time_str in stamp:
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M:%S')
    records.append((cat, dt))
# すでに昇順になっている前提ですが、念のためソート
records.sort(key=lambda x: x[1])

# 入眠から起床のペアを抽出
pairs = []  # 各要素：(start_dt, end_dt)
i = 0
while i < len(records) - 1:
    cat, dt = records[i]
    # 入眠のレコードなら、次の起床を探す
    if cat == 1:
        # 次のレコードが起床かどうか
        j = i + 1
        while j < len(records):
            if records[j][0] == 0:
                # ペア成立
                pairs.append((dt, records[j][1]))
                i = j  # 次はこの起床レコードから再開
                break
            j += 1
    i += 1

# 散布図用の各データ点（元のstampの値）
x_scatter = {cats[0]: [], cats[1]: []}
y_scatter = {cats[0]: [], cats[1]: []}
for cat, date_str, time_str in stamp:
    d = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    t = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
    # 時刻を実数値（時間単位）に変換
    t_val = t.hour + t.minute/60 + t.second/3600
    # x軸は日付（matplotlib内部の数値）
    x_val = mdates.date2num(d)
    x_scatter[cats[cat]].append(x_val)
    y_scatter[cats[cat]].append(t_val)

# グラフの作成
fig, ax = plt.subplots(figsize=(16 * 0.7, 9 * 0.7))

bar_width = 0.3  # 棒の横幅（日単位）

first_bar = True  # 凡例用ラベルは1回のみ表示

# 各ペアごとに、入眠から起床の区間を描画
for start_dt, end_dt in pairs:
    # 入眠時刻（実数値：時間単位）
    start_hour = start_dt.hour + start_dt.minute/60 + start_dt.second/3600
    end_hour   = end_dt.hour   + end_dt.minute/60   + end_dt.second/3600
    # 日付ごとに棒を分割する場合の処理
    if start_dt.date() == end_dt.date():
        # 同じ日の場合：1本の棒
        x_center = mdates.date2num(start_dt.date())
        height = end_hour - start_hour
        if first_bar:
            ax.bar(x_center, height, width=bar_width, bottom=start_hour, 
                   color='gray', alpha=0.3, label='睡眠区間')
            first_bar = False
        else:
            ax.bar(x_center, height, width=bar_width, bottom=start_hour, 
                   color='gray', alpha=0.3)
    else:
        # 日を跨ぐ場合：入眠日の棒と起床日の棒に分割
        # 入眠日の棒：start_dtから24:00まで
        x_center_start = mdates.date2num(start_dt.date())
        height1 = 24 - start_hour
        if first_bar:
            ax.bar(x_center_start, height1, width=bar_width, bottom=start_hour, 
                   color='gray', alpha=0.3, label='睡眠区間')
            first_bar = False
        else:
            ax.bar(x_center_start, height1, width=bar_width, bottom=start_hour, 
                   color='gray', alpha=0.3)
        # 起床日の棒：0:00からend_dtまで
        x_center_end = mdates.date2num(end_dt.date())
        height2 = end_hour  # 0からend_hourまで
        ax.bar(x_center_end, height2, width=bar_width, bottom=0, 
               color='gray', alpha=0.3)

# 散布図（各記録点）の描画
ax.scatter(x_scatter[cats[0]], y_scatter[cats[0]], label=cats[0], color='blue', s=10)
ax.scatter(x_scatter[cats[1]], y_scatter[cats[1]], label=cats[1], color='red', s=10)

# 横軸（日付）の設定
ax.xaxis_date()
date_fmt = mdates.DateFormatter('%Y-%m-%d')
ax.xaxis.set_major_formatter(date_fmt)
fig.autofmt_xdate()

# 縦軸（時刻）のフォーマッター（hh:mm:ss形式）
def time_formatter(x, pos):
    hour = int(x)
    minute = int((x - hour) * 60)
    second = int(round((((x - hour) * 60) - minute) * 60))
    if second >= 60:
        second -= 60
        minute += 1
    if minute >= 60:
        minute -= 60
        hour += 1
    return f'{hour:2d}時'

ax.yaxis.set_major_formatter(FuncFormatter(time_formatter))
# 縦軸の目盛りを3時間毎に設定（0:00, 3:00, …, 21:00, 24:00に近い）
ax.set_yticks([i for i in range(0, 25, 3)])
# 縦軸は0:00〜24:00（必要に応じて反転する場合はset_ylimを変更）
ax.set_ylim(24, 0)

# 横方向のグリッド線追加
ax.yaxis.grid(True)

ax.set_xlabel('日付')
ax.set_ylabel('時刻')
ax.set_title('入眠から起床までの睡眠区間')
ax.legend()

# 画像をメモリ上に保存してbase64エンコード
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
img_data = buf.getvalue()
img_base64 = base64.b64encode(img_data).decode('utf-8')

print()
print(f"""
<html>
<head>
	<meta charset="shift-jis">
    <title>寝起きグラフ</title>
    <link rel="shortcut icon" href="/img/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <h1>寝起きグラフ</h1>
    <form action="./graph.py" method="post">
    	<label>日付：</label>
    	<input type="date" name="base_date" value="{base_date}" size="10">
		<input type="hidden" name="hash" value="{hash}" selected>
		<input type="hidden" name="id" value="{id}">
    	<label>以前1</label>
    	<select name="type">
    		<option value="week">週間</option>
    		<option value="month">ヶ月</option>
    	</select>
    	<label>を表示</label>
		<input type="submit" value="更新" onclick="return clickUpdate();">
    	<div id="msg"></div>
		<script>
		function clickUpdate() {{
			base_date = document.querySelector("input[name=base_date]").value;
			// チェック
			if (base_date.match("^[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}$") == null) {{
				document.querySelector("#msg").innerText = "日付は YYYY-MM-DD で入力";
				return false;
			}}
			document.querySelector("#msg").innerText = "";
			return true;
		}}
		</script>
    </form>
    <img src="data:image/png;base64,{img_base64}" alt="睡眠区間グラフ">
    <form action="./home.py" method="post">
		<input type="hidden" name="hash" value="{hash}">
		<input type="hidden" name="id" value="{id}">
		<input type="submit" value="ホーム">
	</form>
</body>
</html>
""")
