#!/usr/bin/env python3
# coding: utf-8

import json
import sys
import re

# pykakasi と jaconv をインポート
try:
    from pykakasi import kakasi
    import jaconv
except ImportError:
    print("Error: 必要なライブラリがインストールされていません。", file=sys.stderr)
    print("  → `pip install pykakasi jaconv` を実行してください。", file=sys.stderr)
    sys.exit(1)

def load_wordlist(path):
    try:
        with open(path, encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: ファイルが見つかりません: {path}", file=sys.stderr)
        sys.exit(1)

def save_as_json(words, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print(f"✅ {len(words)} 語を '{output_path}' に保存しました。")

def is_pure_hiragana(s):
    # ひらがな（ぁ-ゔ）と長音符（ー）のみ許可
    return bool(re.fullmatch(r'[ぁ-ゔー]+', s))

def main():
    input_path  = 'wordlist.txt'
    output_path = 'words.json'

    # 1) テキスト読み込み
    words = load_wordlist(input_path)

    # 2) pykakasi で漢字を読みからひらがな化
    kakasi_inst = kakasi()
    kakasi_inst.setMode("J", "H")  # 漢字→ひらがな
    kakasi_inst.setMode("K", "H")  # カタカナ→ひらがな
    kakasi_inst.setMode("H", "H")  # ひらがな→ひらがな
    conv = kakasi_inst.getConverter()

    hira_list = []
    for w in words:
        # 漢字→ひらがな
        tmp = conv.do(w)
        # カタカナが残る場合は明示的にひらがなに
        tmp = jaconv.kata2hira(tmp)
        hira_list.append(tmp)

    # 3) 重複除去
    unique = list(dict.fromkeys(hira_list))

    # 4) ひらがな＋ー以外を除外
    filtered = [w for w in unique 
                if is_pure_hiragana(w)
                and len(w) > 2]

    # 5) ソート（あいうえお順）
    filtered.sort(key=lambda w: (w[0], w[-1]))

    # 6) JSON化して保存
    save_as_json(filtered, output_path)

if __name__ == '__main__':
    main()
