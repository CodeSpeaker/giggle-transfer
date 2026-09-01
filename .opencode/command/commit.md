---
description: 按照 Conventional Commits 规范生成提交信息并提交代码
agent: build
---

请根据以下 Conventional Commits 规范生成提交信息：

## 格式规范

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 类型 (type)

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 bug |
| `docs` | 文档更新 |
| `style` | 代码格式调整（不影响功能） |
| `refactor` | 重构（非新增功能、非修复bug） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖更新 |
| `revert` | 回滚提交 |

## 作用域 (scope) - 可选

本项目建议的作用域：
- `sender` - 发送模块
- `receiver` - 接收模块
- `protocol` - 协议相关
- `audio` - 音频处理
- `cli` - 命令行接口
- `deps` - 依赖管理
- `ci` - CI/CD 配置
- `docs` - 文档

## 示例

```
feat(sender): 添加文件分片发送功能

fix(audio): 修复高频音频播放时的削波问题

docs: 更新 README 中的使用示例

refactor(protocol): 重构编码器以支持可变长度帧

chore(deps): 升级 ggwave 到 0.4.3
```

## 要求

1. **subject 行**：使用祈使语气，首字母小写，不超过 50 字符
2. **body**：说明变更动机和对比行为，每行不超过 72 字符
3. **footer**：包含 Breaking Changes 或 Issue 关联（如 `Closes #123`）

## 当前变更上下文

$ARGUMENTS

---

请基于上述规范和当前变更生成符合规范的提交信息并提交代码。