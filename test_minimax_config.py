#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Minimax模型配置的简单脚本
此脚本可以在较低版本的Python上运行，用于验证AI模型配置
"""

import os
import sys
import json

def test_minimax_config():
    print("="*60)
    print("TrendRadarAI - Minimax模型配置测试")
    print("="*60)
    
    # 检查是否安装了litellm
    try:
        import litellm
        print("Success: litellm 库已安装")
        if hasattr(litellm, '__version__'):
            print(f"   版本: {litellm.__version__}")
    except ImportError:
        print("Error: litellm 库未安装")
        print("   请运行: pip install litellm")
        return False
    
    # 测试配置
    print("\n📝 测试配置:")
    print("   模型: minimax/MiniMax-M2.1")
    print("   API基础URL: https://api.minimax.io/v1")
    
    # 检查API密钥
    api_key = os.getenv("MINIMAX_API_KEY") or os.getenv("AI_API_KEY")
    if api_key:
        masked_key = f"{api_key[:5]}{'*' * (len(api_key)-5)}" if len(api_key) > 5 else "****"
        print(f"   API密钥: {masked_key} (已配置)")
    else:
        print("   API密钥: Error 未配置")
        print("   请设置环境变量 MINIMAX_API_KEY 或 AI_API_KEY")
        return False

    print("\nTesting: 开始测试API连接...")

    try:
        # 尝试调用模型
        response = litellm.completion(
            model="minimax/MiniMax-M2.1",
            messages=[{
                "role": "user",
                "content": "你好，请简单介绍一下自己，用一句话回答。"
            }],
            api_key=api_key,
            api_base="https://api.minimax.io/v1",
            timeout=30
        )

        print("Success: API连接测试成功!")
        print(f"   模型响应: {response.choices[0].message.content[:100]}...")
        return True

    except Exception as e:
        print(f"Error: API连接测试失败: {str(e)}")

        # 根据错误类型给出建议
        if "401" in str(e) or "authentication" in str(e).lower():
            print("   建议: 检查API密钥是否正确")
        elif "404" in str(e) or "model" in str(e).lower():
            print("   建议: 检查模型名称是否正确")
        elif "connection" in str(e).lower() or "timeout" in str(e).lower():
            print("   建议: 检查网络连接或API基础URL")
        else:
            print("   建议: 检查API密钥权限和账户状态")
        return False

def check_project_config():
    """检查项目配置文件"""
    import yaml

    config_path = "config/config.yaml"
    local_config_path = "config/local_config.yaml"

    if not os.path.exists(config_path):
        print(f"\nWarning: 配置文件不存在: {config_path}")
        print("   您可以创建一个示例配置文件")
        return False

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 检查本地配置文件
        local_api_key = ""
        if os.path.exists(local_config_path):
            with open(local_config_path, 'r', encoding='utf-8') as f:
                local_config = yaml.safe_load(f)
                local_api_key = local_config.get('ai', {}).get('api_key', '')

        ai_config = config.get('ai', {})
        model = ai_config.get('model', '')
        config_api_key = ai_config.get('api_key', '')

        print(f"\nCheck: 项目配置检查:")
        print(f"   模型: {model}")

        # API密钥优先级: 环境变量(GitHub Secrets) > 本地配置文件 > config参数
        env_api_key = os.environ.get("MINIMAX_API_KEY", "") or os.environ.get("AI_API_KEY", "")
        final_api_key = env_api_key or local_api_key or config_api_key

        if local_api_key:
            print(f"   API密钥: 已配置 (来自本地配置文件)")
        elif env_api_key:
            print(f"   API密钥: 已配置 (来自环境变量)")
        elif config_api_key:
            print(f"   API密钥: 已配置 (来自主配置文件)")
        else:
            print(f"   API密钥: 未配置")

        if 'minimax' in model.lower():
            print("   Success: 检测到Minimax模型配置")
            return True
        else:
            print("   Warning: 未配置Minimax模型")
            return False

    except Exception as e:
        print(f"   Error: 配置文件读取错误: {e}")
        return False

def create_sample_config():
    """创建示例配置文件"""
    sample_config = """# config/config.yaml - TrendRadarAI 配置文件
# Minimax 模型配置示例

# AI 模型配置
ai:
  # 使用 Minimax M2 模型
  model: 'minimax/MiniMax-M2.1'
  
  # API 密钥（留空以使用环境变量）
  api_key: ''  # 通过环境变量 AI_API_KEY 或 MINIMAX_API_KEY 设置
  
  # API 基础 URL
  api_base: 'https://api.minimax.io/v1'
  
  # 模型参数
  timeout: 120
  temperature: 1.0
  max_tokens: 2000
  
  # 高级选项
  num_retries: 1
  fallback_models: []

# AI 分析功能
ai_analysis:
  enabled: true
  language: 'Chinese'
  max_news_for_analysis: 30
  include_rss: false
  include_rank_timeline: true
"""
    
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    config_path = os.path.join(config_dir, "config.yaml")
    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(sample_config)
        print(f"\nSuccess: 示例配置文件已创建: {config_path}")
        print("Tip: 请编辑此文件并添加您的API密钥")
    else:
        print(f"\nInfo: 配置文件已存在: {config_path}")

def main():
    print("TrendRadarAI - Minimax模型配置验证工具")
    print("此工具可在低版本Python上运行，用于验证AI模型配置")
    
    # 检查基本依赖
    try:
        import yaml
    except ImportError:
        print("Warning: 缺少yaml库，正在尝试安装...")
        try:
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
            import yaml
            print("Success: yaml库安装成功")
        except:
            print("Error: 无法安装yaml库，请手动运行: pip install pyyaml")
            return
    
    # 创建示例配置（如果不存在）
    create_sample_config()
    
    # 检查项目配置
    config_ok = check_project_config()
    
    # 如果配置了Minimax模型，进行API测试
    if config_ok:
        print("\n" + "="*60)
        print("开始API连接测试...")
        test_minimax_config()
    
    print("\n" + "="*60)
    print("测试完成!")
    print("\nTips: 使用说明:")
    print("   1. 获取Minimax API密钥")
    print("   2. 设置环境变量: set MINIMAX_API_KEY=your_api_key")
    print("   3. 确保Python版本 >= 3.10")
    print("   4. 安装uv工具: pip install uv")
    print("   5. 运行项目: uv run python -m trendradar")
    print("="*60)

if __name__ == "__main__":
    main()