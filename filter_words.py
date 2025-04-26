#!/usr/bin/env python3
# coding: utf-8

import json
import sys


def load_words(path):
    """
    指定された JSON ファイルを読み込み、単語リストを返します。
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{path}' が見つかりません。", file=sys.stderr)
        sys.exit(1)


def save_words(words, path):
    """
    単語リストを JSON として保存します。
    """
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)


def main():
    # 処理対象のファイル名
    input_path = 'words.json'

    # 1) 元の単語リストを読み込む
    words = load_words(input_path)

    # 2) 長さが3文字以上の単語だけを残す
    filtered = [w for w in words if len(w) > 2]

    # 3) 削除件数を計算
    removed = len(words) - len(filtered)

    # 4) 上書き保存
    save_words(filtered, input_path)

    # 5) 完了メッセージ
    print(f"Removed {removed} entries of length 2 or less. {len(filtered)} entries remain.")


if __name__ == '__main__':
    main()
