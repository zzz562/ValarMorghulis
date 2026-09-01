# scripts

通用小脚本。

| 脚本 | 用途 | 备注 |
|------|------|------|
| `test_models.sh` | Muses 模型连通性测试（延迟 + 可用性） | 密钥走环境变量，**勿硬编码**：`MUSES_PERSONAL_KEY` / `MUSES_TEAM_KEY`（可选 `MUSES_BASE_URL`） |

```bash
export MUSES_PERSONAL_KEY=sk-...   # 个人 key
export MUSES_TEAM_KEY=sk-...       # 团队 key
./scripts/test_models.sh
```
