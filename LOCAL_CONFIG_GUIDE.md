# 使用本地配置文件设置 API 密钥

## 概述

为了安全地管理您的 API 密钥，我们实现了多种配置方式：
1. 本地配置文件（适用于本地开发环境）
2. GitHub Actions Secrets（适用于 CI/CD 环境）

这些方式可以防止敏感信息被意外提交到版本控制系统中。

## 配置步骤

### 方式一：本地开发环境配置

编辑 `config/local_config.yaml` 文件：

```yaml
# 本地配置文件 - 存放敏感信息
# 此文件不会被提交到版本控制系统 (已加入 .gitignore)
#
# 注意：在 GitHub Actions 环境中，优先使用 GitHub Secrets 中的环境变量
# 详情请参见 LOCAL_CONFIG_GUIDE.md 中的 GitHub Actions 配置说明

# AI API 配置
ai:
  # Minimax API 密钥
  # 优先级: GitHub Secrets (环境变量) > local_config.yaml > config.yaml
  # 在 GitHub Actions 中，请使用 Settings > Secrets and variables > Actions 配置
  api_key: ""  # 本地开发环境使用，生产环境请配置 GitHub Secrets

# 其他本地配置项
# (可根据需要添加其他本地配置)
```

### 方式二：GitHub Actions 配置（推荐用于生产环境）

如果您在 GitHub 上 fork 了此项目并使用 GitHub Actions 运行，需要按以下步骤配置：

1. 在您的 GitHub 仓库中，导航到 `Settings` 选项卡
2. 在左侧菜单中选择 `Secrets and variables` > `Actions`
3. 点击 `New repository secret` 按钮
4. 添加以下密钥之一：
   - Name: `MINIMAX_API_KEY`, Value: 您的 Minimax API 密钥
   - 或者 Name: `AI_API_KEY`, Value: 您的 Minimax API 密钥
5. 点击 `Add secret` 保存

## API 密钥优先级

系统按照以下优先级顺序查找 API 密钥（从高到低）：

1. 环境变量 `MINIMAX_API_KEY` 或 `AI_API_KEY`（GitHub Actions Secrets 也属于环境变量）
2. `config/local_config.yaml` 文件中的 `ai.api_key` 值
3. 主配置文件 `config/config.yaml` 中的 `ai.api_key` 值

这种设计确保了在 GitHub Actions 环境中会优先使用安全的 Secrets，而在本地开发环境中可以使用本地配置文件。

## 验证配置

您可以使用以下命令验证配置是否正确加载：

```bash
python simple_test.py
```

或使用我们提供的验证脚本：

```bash
python validate_config_logic.py
```

## 测试大模型连接

当您填入真实的 API 密钥后，可以使用以下脚本测试与大模型的连接：

```bash
python test_model_connection.py
```

## 安全注意事项

1. `config/local_config.yaml` 文件已添加到 `.gitignore` 中，不会被提交到版本控制系统
2. 在 GitHub Actions 中，请始终使用 Secrets 存储 API 密钥，而不是在工作流文件中硬编码
3. 请确保不要在任何公共地方暴露您的 API 密钥
4. 建议定期轮换您的 API 密钥以提高安全性

## 故障排除

如果遇到连接问题，请检查：

1. 本地环境：API 密钥是否正确填入 `config/local_config.yaml`
2. GitHub Actions 环境：是否已在仓库的 Secrets 中正确配置了 `MINIMAX_API_KEY` 或 `AI_API_KEY`
3. API 密钥是否具有足够的权限
4. 网络连接是否正常
5. 模型名称和 API 基础 URL 是否正确配置