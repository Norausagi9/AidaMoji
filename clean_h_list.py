#!/usr/bin/env python3
# coding: utf-8
"""
テキストファイルの各行から「()（）と中の文字」を除去し、残ったひらがな＋長音符のみを抽出して
JSON配列として標準出力に出力するスクリプト。

使い方:
  python clean_h_list.py text.txt > output.json
  cat input.txt | python3 clean_hiragana_list.py > output.json  # ファイル名指定なしでSTDINから読み込み
"""
import re
import json
import sys

# フル／半角かっこ「（）」と「()」と中身を除去
paren_pattern = re.compile(r'[（(][^）\)]*[）)]')
# ひらがな（ぁ-ん）と長音符（ー）のみ抽出
hiragana_pattern = re.compile(r'[ぁ-んー]+')

def clean_line(line: str) -> str:
    # 改行・前後空白除去
    s = line.strip()
    if not s:
        return ''
    # 「（…）」や「(...)」を削除
    s = paren_pattern.sub('', s)
    # ひらがな＋ー のみを結合
    matches = hiragana_pattern.findall(s)
    return ''.join(matches)


def main():
    # 入力ファイルまたはSTDIN
    if len(sys.argv) >= 2:
        try:
            with open(sys.argv[1], encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error: ファイル読み込みエラー: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()

    cleaned = []
    for ln in lines:
        c = clean_line(ln)
        if c:
            cleaned.append(c)

    # デバッグ出力
    print(f"// Input lines: {len(lines)}, Cleaned entries: {len(cleaned)}", file=sys.stderr)

    # JSON配列を出力
    print(json.dumps(cleaned, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
