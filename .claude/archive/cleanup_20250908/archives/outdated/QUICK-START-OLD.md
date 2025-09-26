# NOVELSYS-SWARM 快速参考

## 3分钟快速上手

### 第一步：创建项目（自动完成所有设置）
```bash
/novel:project-new "我的第一本小说"
```

**系统会自动询问并完成：**
- [x] 项目类型（系列/独立）
- [x] 小说类型（都市/玄幻/科幻等）
- [x] 目标读者
- [x] 预计规模
- [x] 核心卖点
- 🎯 自动生成Bible
- 📁 创建所有目录
- 🧠 初始化上下文

### 第二步：开始写作
```bash
/novel:chapter-start 1
```

### 第三步：查看进度
```bash
/novel:status
```

## 常用命令速查

| 命令 | 作用 | 示例 |
|------|------|------|
| `/novel:project-new` | 创建新小说（含Bible） | `/novel:project-new "都市传说"` |
| `/novel:chapter-start` | 开始新章 | `/novel:chapter-start 1` |
| `/novel:chapter-continue` | 继续写作 | `/novel:chapter-continue 2` |
| `/novel:status` | 查看进度 | `/novel:status` |
| `/novel:project-list` | 所有项目 | `/novel:project-list` |
| `/novel:project-switch` | 切换项目 | `/novel:project-switch "另一本"` |
| `/novel:bible-create` | 更新Bible（可选） | `/novel:bible-create` |

## 工作流程变化

### 旧流程 [ ]
1. `/novel:project-new`  ->  创建空项目
2. `/novel:bible-create`  ->  再创建Bible
3. `/novel:chapter-start`  ->  开始写作

### 新流程 [x]
1. `/novel:project-new`  ->  一体化完成所有设置
2. `/novel:chapter-start`  ->  直接开始写作

## 文件位置

你的小说保存在：
```
data/projects/[你的小说名]/
+-- bible.yaml          # 小说设定（自动生成）
+-- project.json        # 项目信息
+-- chapters/           # 章节内容
|   +-- ch001/         
|       +-- content.md  # 第一章
+-- context/            # 上下文跟踪
|   +-- characters.json # 角色发展
|   +-- plot.json       # 剧情进展
|   +-- world.json      # 世界设定
+-- scenes/             # 场景素材
```

## 系列小说特殊结构

如果选择创建系列小说：
```
data/projects/[系列名]/
+-- series_bible/       # 系列总Bible
+-- book_bibles/        # 各本书Bible
+-- ...                 # 其他同上
```

## 完整文档

详细使用说明请查看：`.claude/docs/USAGE-GUIDE.md`

---
*NOVELSYS-SWARM v1.1 - 智能小说创作系统*
*最新更新：一体化项目创建流程*