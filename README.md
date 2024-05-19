# deepseek-api-fix
Fix DeepSeek API

## 用途
解决 DeepSeek API 和 OpenAI 接口不一致，导致无法使用 npm 包 @ai-sdk/openai 的问题：
* messages 中 content 不支持 list
* stream response 中最后一个 chunk 的 role 为 null

## 用法
```bash
pipenv install
pipenv run uvicorn main:app --host 0.0.0.0 --port 9999 --workers 4
```

