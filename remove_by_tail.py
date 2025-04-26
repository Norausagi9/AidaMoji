#!/usr/bin/env python3
# coding: utf-8
"""
Usage:
  python3 remove_by_tail.py <character>

指定した語尾（最後の文字）を持つ単語を words.json からすべて削除します。
例: python3 remove_by_tail.py ん
      → "ん"で終わる単語をすべて除外
"""
import json
import sys
import os

def load_words(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{path}' が見つかりません。", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{path}' の JSON 形式が不正です。", file=sys.stderr)
        sys.exit(1)

def save_words(words, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    tail = sys.argv[1]
    if len(tail) != 1:
        print("Error: 語尾は1文字で指定してください。", file=sys.stderr)
        sys.exit(1)

    json_path = 'words.json'
    words = load_words(json_path)

    # フィルタリング
    filtered = [w for w in words if not w.endswith(tail)]
    removed_count = len(words) - len(filtered)

    # 上書き保存
    save_words(filtered, json_path)

    print(f"Removed {removed_count} entries ending with '{tail}'. {len(filtered)} entries remain.")

if __name__ == '__main__':
    main()
