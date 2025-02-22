from hashlib import sha512
import sys

# 引数
arg = sys.argv

# 引数が違うとだめ
if len(arg) != 3:
	print("引数は [ID] [password]")
	exit()

ID = arg[1]

if not (type(arg[1]) == str and arg[1].isnumeric()):
	print("第1引数は整数")
	exit()

# パスワードを暗号化
hash = sha512(arg[2].encode()).hexdigest()

print(f"insert into password values({ID}, '{hash}');")