#!/usr/bin/env python3
"""
批量替换项目中的品牌和功能名称
将：
1. "喂来日程"改为"喂来日程"
2. "一点外卖"改为"一点外卖"
3. "未来日程"改为"未来日程"
"""

import os
import re
from pathlib import Path

# 定义替换规则
REPLACEMENTS = {
    "喂来日程": "喂来日程",
    "一点外卖": "一点外卖", 
    "未来日程": "未来日程",
    # 可能需要处理一些变体
    "一点外卖": "一点外卖",
    "未来日程": "未来日程",
}

# 要处理的文件扩展名
TEXT_EXTENSIONS = {
    '.md', '.vue', '.js', '.ts', '.py', '.json', '.txt', '.html', '.css'
}

# 排除的目录
EXCLUDE_DIRS = {
    'node_modules', '.git', '.vscode', '__pycache__', 'dist', 'build'
}

def should_process_file(filepath):
    """判断是否应该处理这个文件"""
    # 检查扩展名
    ext = Path(filepath).suffix.lower()
    if ext not in TEXT_EXTENSIONS:
        return False
    
    # 检查是否在排除目录中
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in str(filepath):
            return False
    
    return True

def replace_in_file(filepath):
    """在单个文件中进行替换"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 应用所有替换规则
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
        
        # 如果内容有变化，保存文件
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    
    except Exception as e:
        print(f"处理文件 {filepath} 时出错: {e}")
        return False

def main():
    project_root = Path(__file__).parent
    changed_files = []
    
    print("开始批量替换品牌名称...")
    print("替换规则:")
    for old, new in REPLACEMENTS.items():
        print(f"  {old} -> {new}")
    print()
    
    # 遍历所有文件
    for root, dirs, files in os.walk(project_root):
        # 从dirs中移除排除的目录
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            filepath = Path(root) / file
            if should_process_file(filepath):
                if replace_in_file(filepath):
                    changed_files.append(str(filepath.relative_to(project_root)))
    
    # 输出结果
    print(f"处理完成！共修改了 {len(changed_files)} 个文件:")
    for file in changed_files:
        print(f"  ✓ {file}")
    
    # 保存修改记录
    if changed_files:
        with open(project_root / "brand_rename.log", 'w', encoding='utf-8') as f:
            f.write("品牌名称修改记录\n")
            f.write("=" * 50 + "\n")
            f.write(f"修改时间: {os.path.getmtime(__file__)}\n")
            f.write(f"修改文件数: {len(changed_files)}\n\n")
            f.write("替换规则:\n")
            for old, new in REPLACEMENTS.items():
                f.write(f"  {old} -> {new}\n")
            f.write("\n修改的文件列表:\n")
            for file in changed_files:
                f.write(f"  {file}\n")

if __name__ == "__main__":
    main()