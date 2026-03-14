#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置文件诊断工具
用于检查和修复所有角色的配置文件
"""

import json
import os

# 默认配置
DEFAULT_SETTINGS = {
    'window_width': 240,
    'window_height': 135,
    'bg_width': 240,
    'bg_height': 135,
    'keyboard_x': 94,
    'keyboard_y': 84,
    'keyboard_width': 25,
    'keyboard_height': 25,
    'keyboard_press_offset': 5,
    'mouse_x': 190,
    'mouse_y': 90,
    'mouse_width': 25,
    'mouse_height': 25,
    'max_mouse_offset': 20,
    'mouse_sensitivity': 0.3,
    'sync_scale_enabled': False
}

def check_and_fix_config(character_name, config_path):
    """检查并修复单个角色的配置文件"""
    print(f"\n检查角色: {character_name}")
    print(f"配置文件: {config_path}")
    
    if not os.path.exists(config_path):
        print(f"  ❌ 配置文件不存在，创建默认配置...")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4, ensure_ascii=False)
        print(f"  ✅ 已创建默认配置文件")
        return True
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        fixed = False
        issues = []
        
        # 检查关键配置项
        if config.get('keyboard_press_offset', 0) <= 0:
            issues.append(f"keyboard_press_offset={config.get('keyboard_press_offset')} (应该>0)")
            config['keyboard_press_offset'] = DEFAULT_SETTINGS['keyboard_press_offset']
            fixed = True
        
        # 检查所有必需的配置项
        for key, default_value in DEFAULT_SETTINGS.items():
            if key not in config:
                issues.append(f"缺失配置项: {key}")
                config[key] = default_value
                fixed = True
            elif config[key] is None:
                issues.append(f"{key}=None (无效值)")
                config[key] = default_value
                fixed = True
        
        if issues:
            print(f"  ⚠️  发现问题:")
            for issue in issues:
                print(f"     - {issue}")
        
        if fixed:
            # 保存修复后的配置
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            print(f"  ✅ 已自动修复配置文件")
            return True
        else:
            print(f"  ✅ 配置正常")
            return False
            
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON格式错误: {e}")
        print(f"  🔧 重新创建配置文件...")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_SETTINGS, f, indent=4, ensure_ascii=False)
        print(f"  ✅ 已重新创建配置文件")
        return True
    except Exception as e:
        print(f"  ❌ 检查失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("配置文件诊断工具")
    print("=" * 60)
    
    img_dir = 'img'
    if not os.path.exists(img_dir):
        print(f"❌ 找不到img目录")
        return
    
    fixed_count = 0
    total_count = 0
    
    # 遍历所有角色文件夹
    for folder in os.listdir(img_dir):
        folder_path = os.path.join(img_dir, folder)
        if os.path.isdir(folder_path):
            config_path = os.path.join(folder_path, 'config.json')
            total_count += 1
            if check_and_fix_config(folder, config_path):
                fixed_count += 1
    
    print("\n" + "=" * 60)
    print(f"检查完成: 共{total_count}个角色，修复了{fixed_count}个配置文件")
    print("=" * 60)
    
    if fixed_count > 0:
        print("\n建议: 请重启程序以应用修复后的配置")
    
    input("\n按回车键退出...")

if __name__ == '__main__':
    main()
