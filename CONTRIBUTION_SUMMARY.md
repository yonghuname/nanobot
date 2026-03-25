# Nanobot 贡献总结

## 概览

本次为 nanobot 项目贡献了 4 个 Pull Request，修复了多个重要 bug 并添加了实用功能。

---

## PR #1: 修复 Cron 提醒被 Evaluator 抑制

**分支**: `fix/cron-reminder-suppression`  
**Issue**: #2369  
**类型**: Bug Fix

### 问题描述
用户设置的定时提醒（cron jobs）虽然成功触发，但消息被 evaluator 错误地判定为"常规确认"而被静默抑制，导致用户永远收不到提醒通知。

### 解决方案
- 更新 `nanobot/utils/evaluator.py` 中的系统 prompt
- 添加明确的"ALWAYS notify"规则，特别强调提醒关键词（'remind', 'reminder'）
- 重构通知规则为更结构化的格式，提高 LLM 判断准确性

### 修改文件
- `nanobot/utils/evaluator.py`: 优化 evaluator prompt
- `tests/agent/test_evaluator.py`: 添加提醒场景测试用例

### 测试结果
- ✅ 6/6 测试通过
- ✅ 代码风格检查通过

---

## PR #2: 优化 Heartbeat 服务跳过空任务

**分支**: `feat/heartbeat-skip-empty-tasks`  
**Issue**: #2406  
**类型**: Feature / Optimization

### 问题描述
即使 `HEARTBEAT.md` 文件为空或只包含注释/标题，heartbeat 服务仍每 30 分钟调用一次 LLM，浪费大量 API tokens 和费用。

### 解决方案
- 添加 `_has_active_tasks()` 方法，在调用 LLM 前检查文件内容
- 如果只有注释、空行或 markdown 标题，提前返回，跳过 LLM 调用
- 保持所有现有功能不变

### 修改文件
- `nanobot/heartbeat/service.py`: 添加预检查逻辑
- `tests/agent/test_heartbeat_service.py`: 添加 4 个新测试用例

### 测试结果
- ✅ 12/12 测试通过（包括 4 个新增测试）
- ✅ 代码风格检查通过

### 影响
为不使用 heartbeat 功能的用户每 30 分钟节省一次 LLM API 调用。

---

## PR #3: 添加 Groq 转录语言参数支持

**分支**: `feat/groq-transcription-language`  
**Issue**: #2421  
**类型**: Feature Enhancement

### 问题描述
Groq Whisper API 转录时未指定语言参数，依赖自动检测，偶尔会导致不准确的转录结果。

### 解决方案
- 在 `GroqTranscriptionProvider` 添加 `language` 参数（ISO-639-1 格式）
- 在 `ProviderConfig` schema 中添加 `transcription_language` 配置字段
- 更新 `BaseChannel` 和 `ChannelManager` 传递语言参数
- 从 Groq provider 配置中自动读取并应用到所有 channel

### 配置示例
```json
{
  "providers": {
    "groq": {
      "apiKey": "your-key",
      "transcriptionLanguage": "zh"
    }
  }
}
```

### 修改文件
- `nanobot/providers/transcription.py`: 添加语言参数支持
- `nanobot/config/schema.py`: 添加配置字段
- `nanobot/channels/base.py`: 传递语言参数
- `nanobot/channels/manager.py`: 从配置读取语言设置
- `tests/test_transcription.py`: 新增完整测试套件

### 测试结果
- ✅ 4/4 测试通过
- ✅ 代码风格检查通过

---

## PR #4: 修复连续 Assistant 消息导致的 API 错误

**分支**: `fix/subagent-consecutive-assistant-messages`  
**Issue**: #2376  
**类型**: Bug Fix

### 问题描述
当 subagent 结果（role=assistant）被添加到已以 assistant 消息结尾的对话历史时，会产生连续的 assistant 消息，导致 vLLM 等部分 LLM API 拒绝请求并报错："Cannot have 2 or more assistant messages at the end of the list"。

### 解决方案
在 `ContextBuilder.build_messages()` 中添加检测逻辑：
1. 检查历史最后一条消息的 role
2. 如果与当前消息 role 相同：
   - 字符串内容：合并到前一条消息
   - 复杂内容：将当前消息 role 改为 "user"
3. 避免任何连续相同 role 的情况

### 修改文件
- `nanobot/agent/context.py`: 添加连续消息检测和处理逻辑
- `tests/agent/test_consecutive_messages.py`: 新增专门测试文件，4 个测试用例

### 测试结果
- ✅ 4/4 新测试通过
- ✅ 17/17 相关测试通过（确保不破坏现有功能）
- ✅ 代码风格检查通过

---

## 工作流程

### 1. Issue 调研
- 获取并分析了 50+ 个 open issues
- 筛选出有明确复现步骤和解决方案的问题
- 优先选择影响用户体验的核心 bug

### 2. 代码实现
- 为每个 issue 创建独立分支（从最新的 upstream/main）
- 遵循项目代码规范（ruff）
- 添加完整的测试覆盖

### 3. 质量保证
- 所有修改都经过测试验证
- 确保不破坏现有功能
- 代码风格检查通过

### 4. 文档完善
- 编写清晰的 commit message
- 包含问题描述、解决方案和测试结果
- 添加 Co-Authored-By 标注

---

## 技术栈

- **Python 3.11+**
- **Pytest**: 测试框架
- **Ruff**: 代码风格检查
- **UV**: 包管理器

---

## 统计数据

- **总共提交**: 4 个独立分支
- **修改文件**: 12 个
- **新增测试**: 18 个测试用例
- **代码行数**: +300 行
- **测试通过率**: 100%

---

## 分支状态

所有分支都已：
- ✅ 基于最新的 upstream/main
- ✅ 通过所有测试
- ✅ 代码风格检查通过
- ✅ 推送到远程仓库
- ✅ 准备创建 PR

---

## PR 创建链接

1. **Cron 提醒修复**:  
   https://github.com/HKUDS/nanobot/compare/main...yonghuname:nanobot:fix/cron-reminder-suppression

2. **Heartbeat 优化**:  
   https://github.com/HKUDS/nanobot/compare/main...yonghuname:nanobot:feat/heartbeat-skip-empty-tasks

3. **Groq 语言参数**:  
   https://github.com/HKUDS/nanobot/compare/main...yonghuname:nanobot:feat/groq-transcription-language

4. **连续消息修复**:  
   https://github.com/HKUDS/nanobot/compare/main...yonghuname:nanobot:fix/subagent-consecutive-assistant-messages

---

## 维护者反馈待办

- [ ] 等待 code review
- [ ] 根据反馈修改
- [ ] 合并后更新本地分支
- [ ] 继续贡献其他 issues

---

## 经验总结

### 做得好的地方
1. **独立分支**: 每个 issue 一个分支，便于独立审查和合并
2. **完整测试**: 每个修改都有对应的测试用例
3. **小而精准**: 每个 PR 只解决一个明确的问题
4. **文档清晰**: commit message 和代码注释都很详细

### 可以改进
1. 提前与维护者沟通，确认修复方向
2. 更早地测试在真实环境中的表现
3. 考虑添加性能基准测试

---

**日期**: 2026-03-25  
**贡献者**: yonghuname (with Claude Sonnet 4.5)
