# Docker容器ImportError修复步骤

## 问题修复
已修复 `app_improved.py` 中的导入错误：
- **修复前**: `from docling.backend.docling_parse_backend import DoclingParseV2DocumentBackend`
- **修复后**: `from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend`

## 立即执行的命令

### 1. 打开命令提示符/PowerShell

### 2. 停止现有容器
```cmd
docker stop docling-granite
docker rm docling-granite
```

### 3. 导航到Docker目录
```cmd
cd "D:\NOVELSYS-SWARM\.claude\docker\docling"
```

### 4. 重新构建容器(使用修复后的代码)
```cmd
docker-compose build --no-cache
```

### 5. 启动新容器
```cmd
docker-compose up -d
```

### 6. 检查容器状态
```cmd
docker ps
```

### 7. 查看日志确认启动成功
```cmd
docker logs docling-granite
```

### 8. 测试API端点
```cmd
curl http://localhost:8000/
```

## 预期结果

### 成功的日志应该显示：
```
INFO:     Initializing Enhanced Docling converter with optimized settings...
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### API响应应该返回：
```json
{
    "service": "Enhanced Docling PDF Processor",
    "version": "2.53.0",
    "model": "Granite-Docling-258M + DocLayoutNet + TableFormer",
    "backend": "DoclingParseV4 (Latest & Fastest)",
    "accuracy_mode": "Maximum",
    "status": "ready"
}
```

## 如果仍有错误

1. **查看完整日志**: `docker logs docling-granite --follow`
2. **检查容器内部**: `docker exec -it docling-granite /bin/bash`
3. **测试Python导入**: `python -c "from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend; print('Import successful')"`

## 修复的关键变更

### 导入修复
```python
# 错误的导入 (导致ImportError)
from docling.backend.docling_parse_backend import DoclingParseV2DocumentBackend

# 正确的导入 (Docling 2.53.0)
from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
```

### 实例化修复
```python
# 修复前
backend=DoclingParseV2DocumentBackend(),  # 10x faster PDF loading

# 修复后
backend=DoclingParseV4DocumentBackend(),  # Latest V4 backend for best performance
```

## 测试输出目录

修复后，处理的PDF文件将保存到：
- **主机路径**: `D:\NOVELSYS-SWARM\.claude\testing\`
- **容器内路径**: `/data/processed/`

立即执行上述命令来修复容器启动问题！