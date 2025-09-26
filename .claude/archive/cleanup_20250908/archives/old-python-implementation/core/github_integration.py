"""
GitHub Integration for NOVELSYS-SWARM
实现GitHub Issues作为持久化数据库
借鉴CCPM的Issue-as-Database理念
"""

import os
import json
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class GitHubIntegration:
    """
    GitHub集成管理器
    使用GitHub CLI (gh) 进行所有操作
    """
    
    def __init__(self, owner: str = None, repo: str = None):
        self.owner = owner
        self.repo = repo
        self.initialized = False
        self._check_gh_cli()
    
    def _check_gh_cli(self) -> bool:
        """检查GitHub CLI是否已安装并认证"""
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True
            )
            self.initialized = result.returncode == 0
            if not self.initialized:
                logger.warning("GitHub CLI未认证，请运行: gh auth login")
            return self.initialized
        except FileNotFoundError:
            logger.error("GitHub CLI未安装，请访问: https://cli.github.com/")
            return False
    
    def _run_gh_command(self, args: List[str]) -> Tuple[bool, str]:
        """执行GitHub CLI命令"""
        if not self.initialized:
            return False, "GitHub CLI未初始化"
        
        try:
            result = subprocess.run(
                ["gh"] + args,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def create_novel_repo(self, project_name: str, description: str = None) -> Tuple[bool, str]:
        """
        创建新的小说项目仓库
        """
        desc = description or f"NOVELSYS-SWARM Novel Project: {project_name}"
        
        # 创建仓库
        success, output = self._run_gh_command([
            "repo", "create", project_name,
            "--description", desc,
            "--private",  # 默认私有
            "--clone"
        ])
        
        if success:
            self.owner = self._get_current_user()
            self.repo = project_name
            
            # 创建初始结构
            self._create_initial_structure(project_name)
            
            return True, f"成功创建仓库: {self.owner}/{self.repo}"
        else:
            return False, f"创建仓库失败: {output}"
    
    def _get_current_user(self) -> str:
        """获取当前GitHub用户名"""
        success, output = self._run_gh_command(["api", "user", "--jq", ".login"])
        return output.strip() if success else "unknown"
    
    def _create_initial_structure(self, project_name: str):
        """创建初始Issue结构"""
        # 创建Bible Issue (Epic)
        self.create_issue(
            title=f"[Bible] {project_name} 小说设定",
            body=self._get_bible_template(),
            labels=["bible", "epic"]
        )
        
        # 创建里程碑
        self._run_gh_command([
            "api", f"repos/{self.owner}/{self.repo}/milestones",
            "--method", "POST",
            "--field", f"title=Volume 1",
            "--field", f"description=第一卷"
        ])
    
    def create_issue(self, title: str, body: str, labels: List[str] = None) -> Tuple[bool, int]:
        """
        创建GitHub Issue
        返回: (成功与否, Issue编号)
        """
        args = ["issue", "create", "--title", title, "--body", body]
        
        if labels:
            args.extend(["--label", ",".join(labels)])
        
        if self.repo:
            args.extend(["--repo", f"{self.owner}/{self.repo}"])
        
        success, output = self._run_gh_command(args)
        
        if success:
            # 解析Issue编号
            try:
                issue_num = int(output.split("/")[-1].strip())
                return True, issue_num
            except:
                return True, 0
        else:
            return False, -1
    
    def update_issue(self, issue_num: int, comment: str) -> bool:
        """
        添加Issue评论（用于进度更新）
        """
        args = ["issue", "comment", str(issue_num), "--body", comment]
        
        if self.repo:
            args.extend(["--repo", f"{self.owner}/{self.repo}"])
        
        success, _ = self._run_gh_command(args)
        return success
    
    def get_issue(self, issue_num: int) -> Optional[Dict]:
        """
        获取Issue详情
        """
        args = ["issue", "view", str(issue_num), "--json", 
                "title,body,comments,labels,state"]
        
        if self.repo:
            args.extend(["--repo", f"{self.owner}/{self.repo}"])
        
        success, output = self._run_gh_command(args)
        
        if success:
            try:
                return json.loads(output)
            except:
                return None
        return None
    
    def sync_chapter_to_issue(self, chapter_num: int, chapter_data: Dict) -> bool:
        """
        同步章节到GitHub Issue
        """
        # 检查Issue是否存在
        issue = self.get_issue(chapter_num + 1)  # Issue从1开始，章节从0开始
        
        if not issue:
            # 创建新Issue
            title = f"第{chapter_num}章: {chapter_data.get('title', '未命名')}"
            body = self._format_chapter_body(chapter_data)
            success, issue_num = self.create_issue(
                title=title,
                body=body,
                labels=["chapter", f"ch-{chapter_num}"]
            )
        else:
            # 更新现有Issue
            issue_num = chapter_num + 1
            comment = self._format_progress_comment(chapter_data)
            success = self.update_issue(issue_num, comment)
        
        return success
    
    def _get_bible_template(self) -> str:
        """获取Bible Issue模板"""
        return """
# 📚 小说Bible设定

## 🌍 世界观设定
- **时代背景**: 
- **地理环境**: 
- **社会结构**: 
- **科技/魔法水平**: 

## 👥 主要角色
### 主角
- **姓名**: 
- **年龄/性别**: 
- **性格特征**: 
- **核心动机**: 
- **成长轨迹**: 

### 配角
[待添加]

## 📖 故事主线
- **开端**: 
- **发展**: 
- **高潮**: 
- **结局**: 

## 🎯 核心主题
- **主题思想**: 
- **要探讨的问题**: 
- **价值观传递**: 

## 📝 写作规范
- **文风**: 
- **人称**: 
- **节奏**: 
- **目标字数**: 

---
*此Issue作为小说的核心设定文档，所有章节都应遵循这里的设定*
"""
    
    def _format_chapter_body(self, chapter_data: Dict) -> str:
        """格式化章节Issue内容"""
        return f"""
# 章节信息

## 📊 基本信息
- **章节号**: {chapter_data.get('number', 0)}
- **标题**: {chapter_data.get('title', '未命名')}
- **字数**: {chapter_data.get('word_count', 0)}
- **创建时间**: {chapter_data.get('created_at', datetime.now().isoformat())}

## 📝 章节大纲
{chapter_data.get('outline', '待添加')}

## 🎭 8-Stream分析
- [ ] Character Psychology - 角色心理
- [ ] Narrative Structure - 叙事结构
- [ ] World Building - 世界构建
- [ ] Prose Craft - 文笔工艺
- [ ] Continuity Guard - 连贯性守护
- [ ] Foreshadowing - 伏笔管理
- [ ] Dialogue Master - 对话艺术
- [ ] Emotion Weaver - 情感编织

## 📈 质量指标
- **目标质量**: 98分
- **当前质量**: {chapter_data.get('quality_score', 0)}分

## 🔗 关联
- **前承**: 第{chapter_data.get('number', 1)-1}章
- **后启**: 第{chapter_data.get('number', 1)+1}章
- **伏笔**: {chapter_data.get('foreshadowing', [])}

---
*使用8-Stream系统生成和优化*
"""
    
    def _format_progress_comment(self, chapter_data: Dict) -> str:
        """格式化进度更新评论"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""
## 🔄 进度更新 - {timestamp}

### ✅ 完成的Stream
{self._format_stream_status(chapter_data.get('streams', {}))}

### 📊 质量评分
- **综合得分**: {chapter_data.get('quality_score', 0)}/100
- **角色深度**: {chapter_data.get('character_score', 0)}/100
- **情节连贯**: {chapter_data.get('plot_score', 0)}/100
- **文字表达**: {chapter_data.get('prose_score', 0)}/100

### 📝 关键决策
{self._format_decisions(chapter_data.get('decisions', []))}

### 🚀 下一步
{self._format_next_steps(chapter_data.get('next_steps', []))}

### 💾 文件更新
- 章节内容: `data/chapters/ch{chapter_data.get('number', 0)}.md`
- 分析报告: `data/analysis/ch{chapter_data.get('number', 0)}_analysis.json`

---
*此更新由NOVELSYS-SWARM自动生成*
"""
    
    def _format_stream_status(self, streams: Dict) -> str:
        """格式化Stream状态"""
        result = []
        for stream, status in streams.items():
            emoji = "✅" if status.get('completed') else "⏳"
            score = status.get('score', 0)
            result.append(f"- {emoji} {stream}: {score}分")
        return "\n".join(result) if result else "- 暂无Stream完成"
    
    def _format_decisions(self, decisions: List) -> str:
        """格式化关键决策"""
        if not decisions:
            return "- 暂无关键决策"
        return "\n".join([f"- {d}" for d in decisions[:5]])
    
    def _format_next_steps(self, next_steps: List) -> str:
        """格式化下一步计划"""
        if not next_steps:
            return "- 待定"
        return "\n".join([f"- {s}" for s in next_steps[:3]])
    
    def create_chapter_issue_batch(self, num_chapters: int) -> List[int]:
        """
        批量创建章节Issue
        """
        issue_numbers = []
        
        for i in range(1, num_chapters + 1):
            title = f"第{i}章: [待定]"
            body = self._format_chapter_body({
                'number': i,
                'title': '待定',
                'outline': '待生成'
            })
            
            success, issue_num = self.create_issue(
                title=title,
                body=body,
                labels=["chapter", f"ch-{i}", "pending"]
            )
            
            if success:
                issue_numbers.append(issue_num)
                logger.info(f"创建章节Issue #{issue_num}")
        
        return issue_numbers
    
    def get_all_chapter_issues(self) -> List[Dict]:
        """
        获取所有章节Issue
        """
        args = ["issue", "list", "--label", "chapter", 
                "--json", "number,title,state,labels"]
        
        if self.repo:
            args.extend(["--repo", f"{self.owner}/{self.repo}"])
        
        success, output = self._run_gh_command(args)
        
        if success:
            try:
                issues = json.loads(output)
                # 按章节号排序
                issues.sort(key=lambda x: x.get('number', 0))
                return issues
            except:
                return []
        return []
    
    def close_issue(self, issue_num: int, reason: str = "completed") -> bool:
        """
        关闭Issue（章节完成时）
        """
        args = ["issue", "close", str(issue_num), "--reason", reason]
        
        if self.repo:
            args.extend(["--repo", f"{self.owner}/{self.repo}"])
        
        success, _ = self._run_gh_command(args)
        return success


class GitHubContextManager:
    """
    管理GitHub Issue中的上下文信息
    实现跨会话的记忆持久化
    """
    
    def __init__(self, github: GitHubIntegration):
        self.github = github
        self.context_cache = {}
    
    def save_context(self, issue_num: int, context_type: str, context_data: Dict) -> bool:
        """
        保存上下文到Issue评论
        """
        # 格式化上下文为特殊标记的评论
        comment = f"""
<!-- CONTEXT:{context_type} -->
```json
{json.dumps(context_data, ensure_ascii=False, indent=2)}
```
<!-- END_CONTEXT -->
"""
        
        return self.github.update_issue(issue_num, comment)
    
    def load_context(self, issue_num: int, context_type: str = None) -> Optional[Dict]:
        """
        从Issue加载上下文
        """
        issue = self.github.get_issue(issue_num)
        if not issue:
            return None
        
        contexts = {}
        
        # 解析评论中的上下文
        for comment in issue.get('comments', []):
            body = comment.get('body', '')
            
            # 查找上下文标记
            if '<!-- CONTEXT:' in body:
                # 提取上下文类型
                ctx_type = body.split('<!-- CONTEXT:')[1].split('-->')[0].strip()
                
                # 提取JSON数据
                if '```json' in body:
                    json_str = body.split('```json')[1].split('```')[0].strip()
                    try:
                        contexts[ctx_type] = json.loads(json_str)
                    except:
                        pass
        
        if context_type:
            return contexts.get(context_type)
        return contexts
    
    def sync_bible_to_issue(self, bible_data: Dict) -> bool:
        """
        同步Bible到Issue #1
        """
        return self.save_context(1, "bible", bible_data)
    
    def load_bible_from_issue(self) -> Optional[Dict]:
        """
        从Issue #1加载Bible
        """
        return self.load_context(1, "bible")
    
    def get_chapter_history(self, chapter_num: int) -> List[Dict]:
        """
        获取章节的完整历史记录
        """
        issue = self.github.get_issue(chapter_num + 1)
        if not issue:
            return []
        
        history = []
        for comment in issue.get('comments', []):
            if '进度更新' in comment.get('body', ''):
                history.append({
                    'timestamp': comment.get('createdAt'),
                    'content': comment.get('body')
                })
        
        return history


# 使用示例
if __name__ == "__main__":
    # 初始化GitHub集成
    gh = GitHubIntegration()
    
    # 创建小说项目
    success, msg = gh.create_novel_repo(
        "my-awesome-novel",
        "使用NOVELSYS-SWARM创作的科幻小说"
    )
    print(msg)
    
    # 创建章节Issue
    if success:
        issue_nums = gh.create_chapter_issue_batch(10)
        print(f"创建了{len(issue_nums)}个章节Issue")
        
        # 同步章节进度
        chapter_data = {
            'number': 1,
            'title': '觉醒',
            'word_count': 3000,
            'quality_score': 92,
            'streams': {
                'Character Psychology': {'completed': True, 'score': 95},
                'Narrative Structure': {'completed': True, 'score': 90}
            },
            'decisions': [
                '采用第一人称限制视角',
                '设置悬念钩子'
            ],
            'next_steps': [
                '深化主角内心冲突',
                '加强环境描写'
            ]
        }
        
        gh.sync_chapter_to_issue(1, chapter_data)
        print("章节进度已同步到GitHub")