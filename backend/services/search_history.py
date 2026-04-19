# services/search_history.py
# 搜索历史与热门关键词管理（内存存储，可选持久化）

import json
import os
from collections import defaultdict
from typing import List

HISTORY_FILE = "search_history.json"

# 内存存储：{ "披萨": 15, "麻辣烫": 10, ... }
_keyword_freq = defaultdict(int)


def _load_from_file():
    """从文件加载历史记录（如果存在）"""
    global _keyword_freq
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _keyword_freq.update(data)
        except Exception:
            pass


def _save_to_file():
    """保存历史记录到文件"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(dict(_keyword_freq), f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# 启动时加载历史记录
_load_from_file()


def record_keywords(keywords: List[str]):
    """
    记录一组关键词，每出现一次频率 +1
    自动去重并转为小写（避免大小写差异）
    """
    if not keywords:
        return
    for kw in keywords:
        if kw and isinstance(kw, str):
            clean_kw = kw.strip().lower()
            if clean_kw:
                _keyword_freq[clean_kw] += 1
    _save_to_file()


def get_hot_keywords(limit: int = 5) -> List[str]:
    """
    返回频率最高的前 limit 个关键词（按频率降序）
    """
    sorted_kw = sorted(_keyword_freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_kw[:limit]]


def clear_history():
    """清空历史记录（可选，用于调试）"""
    global _keyword_freq
    _keyword_freq.clear()
    _save_to_file()