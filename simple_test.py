#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的Minimax配置验证脚本
"""

import os
import yaml

def check_config():
    """检查配置文件"""
    print("="*50)
    print("TrendRadarAI - Minimax配置验证")
    print("="*50)
    
    # 检查配置文件是否存在
    config_path = "config/config.yaml"
    if not os.path.exists(config_path):
        print(f"Error: 配置文件不存在: {config_path}")
        return False
    
    # 读取配置文件
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        ai_config = config.get('ai', {})
        model = ai_config.get('model', '')
        api_key = ai_config.get('api_key', '')
        api_base = ai_config.get('api_base', '')
        
        print(f"模型: {model}")
        print(f"API基础URL: {api_base}")
        print(f"API密钥配置: {'已配置' if api_key else '未配置(将使用环境变量)'}")
        
        if 'minimax' in model.lower():
            print("Success: 检测到Minimax模型配置")
            return True
        else:
            print("Warning: 未配置Minimax模型")
            return False
            
    except Exception as e:
        print(f"Error: 配置文件读取错误: {e}")
        return False

def check_env_vars():
    """检查环境变量和本地配置"""
    import yaml

    print("\n检查配置:")

    # 检查本地配置文件
    local_config_path = "config/local_config.yaml"
    local_api_key = ""
    if os.path.exists(local_config_path):
        try:
            with open(local_config_path, 'r', encoding='utf-8') as f:
                local_config = yaml.safe_load(f)
                local_api_key = local_config.get('ai', {}).get('api_key', '')
        except:
            pass

    minimax_key = os.getenv("MINIMAX_API_KEY")
    ai_key = os.getenv("AI_API_KEY")

    if minimax_key:
        masked = f"{minimax_key[:5]}{'*'*(len(minimax_key)-5)}" if len(minimax_key) > 5 else "****"
        print(f"MINIMAX_API_KEY: {masked} (来自环境变量/GitHub Secrets) - 优先级最高")
    else:
        print("MINIMAX_API_KEY: 未设置")

    if ai_key:
        masked = f"{ai_key[:5]}{'*'*(len(ai_key)-5)}" if len(ai_key) > 5 else "****"
        print(f"AI_API_KEY: {masked} (来自环境变量/GitHub Secrets) - 优先级最高")
    else:
        print("AI_API_KEY: 未设置")

    if local_api_key:
        masked = f"{local_api_key[:5]}{'*'*(len(local_api_key)-5)}" if len(local_api_key) > 5 else "****"
        print(f"Local Config API Key: {masked} (来自本地配置文件) - 优先级较低")
    else:
        print("Local Config API Key: 未设置")

    # API密钥优先级: 环境变量(GitHub Secrets) > 本地配置文件 > config参数
    return bool(minimax_key or ai_key or local_api_key)

def main():
    print("TrendRadarAI - Minimax配置验证工具")
    print("此工具验证配置是否正确设置")
    
    # 检查配置
    config_ok = check_config()
    
    # 检查环境变量
    env_ok = check_env_vars()
    
    print("\n" + "="*50)
    print("验证结果:")
    
    if config_ok:
        print("OK: 配置文件中已设置Minimax模型")
    else:
        print("Error: 配置文件中未设置Minimax模型")

    if env_ok:
        print("OK: 已设置API密钥环境变量")
    else:
        print("Error: 未设置API密钥环境变量")

    if config_ok and env_ok:
        print("\nSuccess: 配置验证通过！")
        print("现在可以运行项目来测试Minimax API连接。")
    else:
        print("\nWarning: 配置验证未完全通过。")
        print("请确保:")
        print("- 配置文件中设置了正确的模型名称")
        print("- 设置了API密钥环境变量")
    
    print("="*50)

if __name__ == "__main__":
    main()