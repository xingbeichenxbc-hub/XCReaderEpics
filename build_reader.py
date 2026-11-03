#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XClassics 荷马史诗三语对读 —— 独立网页构建脚本
将《伊利亚特》《奥德赛》两份 JSON 内嵌进 reader_template.html，
生成单个可发布的 HTML 文件（无外部依赖，可离线打开 / 部署）。
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

FILES = {
    'iliad': os.path.join(HERE, '伊利亚特.json'),
    'odyssey': os.path.join(HERE, '奥德赛.json'),
}
TEMPLATE = os.path.join(HERE, 'reader_template.html')
OUTPUT = os.path.join(HERE, '荷马史诗三语对读.html')
PLACEHOLDER = '__EPIC_DATA__'


def read_version(template):
    m = re.search(r'<meta\s+name="version"\s+content="([^"]+)"', template)
    return m.group(1) if m else 'unknown'


def main():
    data = {}
    for key, path in FILES.items():
        with open(path, encoding='utf-8') as f:
            data[key] = json.load(f)
        print(f'[load] {key}: {path}  '
              f'(books={len(data[key]["books"])})')

    # 序列化：保留非 ASCII（体积更小），并将 '<' 转义为 \u003c，
    # 避免脚本标签内出现 "</script>" 等提前闭合序列。
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    blob = blob.replace('<', '\\u003c')

    with open(TEMPLATE, encoding='utf-8') as f:
        template = f.read()

    version = read_version(template)

    assert PLACEHOLDER in template, '模板中未找到占位符 ' + PLACEHOLDER
    out = template.replace(PLACEHOLDER, blob)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(out)

    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f'[done] XCReaderEpics {version} -> {OUTPUT}  ({size_kb:.1f} KB)')


if __name__ == '__main__':
    main()
