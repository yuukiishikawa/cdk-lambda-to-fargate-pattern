from time import sleep
import argparse

"""
This module contains a simple 'Hello, World!' program.
"""


parser = argparse.ArgumentParser(description='コマンドライン引数を取得するデモ')
# '--params'という引数を追加
parser.add_argument('--params', type=str, help='パラメータを指定')
# 引数を解析
args = parser.parse_args()

print('Hello, World!')
# 'params'引数の値を取得して表示
print(f"受け取ったparamsの値: {args.params}")

sleep(10)
print('10秒後')
