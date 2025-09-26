"""
Entity Dictionary Manager for NOVELSYS-SWARM
智能管理实体名称变体，避免假阳性检测
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import re


class EntityDictionaryManager:
    """实体词典管理器 - 智能处理名称变体"""
    
    def __init__(self, dictionary_path: str = ".claude/agents/shared/entity_dictionary.yaml"):
        self.dictionary_path = Path(dictionary_path)
        self.dictionary = self._load_dictionary()
        self.learning_threshold = 95  # 只从95分以上章节学习
        self.auto_accept_confidence = 0.95
        self.manual_review_threshold = 0.80
        
    def _load_dictionary(self) -> Dict[str, Any]:
        """加载实体词典"""
        if self.dictionary_path.exists():
            with open(self.dictionary_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._create_empty_dictionary()
    
    def _create_empty_dictionary(self) -> Dict[str, Any]:
        """创建空词典结构"""
        return {
            "metadata": {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "learning_threshold": 95,
                "chapters_learned_from": []
            },
            "entities": {
                "locations": {},
                "characters": {},
                "objects": {}
            },
            "learning_log": {
                "pending_patterns": [],
                "rejected_patterns": []
            }
        }
    
    def save_dictionary(self):
        """保存词典到文件"""
        self.dictionary["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.dictionary_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.dictionary, f, allow_unicode=True, default_flow_style=False)
    
    def initialize_from_bible(self, bible_content: Dict[str, Any]) -> Dict[str, Any]:
        """从Bible初始化实体词典"""
        entities = {
            "locations": {},
            "characters": {},
            "objects": {}
        }
        
        # 提取地点
        if "universe" in bible_content and "island_profiles" in bible_content["universe"]:
            for island_name, island_data in bible_content["universe"]["island_profiles"].items():
                if "inn_name" in island_data:
                    inn_name = island_data["inn_name"]
                    entities["locations"][self._normalize_key(inn_name)] = {
                        "canonical": inn_name,
                        "source": "bible",
                        "bible_reference": f"universe.island_profiles.{island_name}.inn_name",
                        "variations": self._generate_location_variations(inn_name)
                    }
        
        # 提取角色
        if "characters" in bible_content:
            # 主角
            if "protagonist" in bible_content["characters"]:
                protagonist = bible_content["characters"]["protagonist"]
                name = protagonist.get("name", "")
                if name:
                    entities["characters"][self._normalize_key(name)] = {
                        "canonical": name,
                        "source": "bible",
                        "critical_facts": self._extract_critical_facts(protagonist),
                        "variations": self._generate_character_variations(name)
                    }
            
            # 配角
            if "primary_supporting_character" in bible_content["characters"]:
                supporting = bible_content["characters"]["primary_supporting_character"]
                name = supporting.get("name", "")
                if name:
                    entities["characters"][self._normalize_key(name)] = {
                        "canonical": name,
                        "source": "bible",
                        "critical_facts": self._extract_critical_facts(supporting),
                        "variations": self._generate_character_variations(name)
                    }
        
        self.dictionary["entities"] = entities
        self.save_dictionary()
        return entities
    
    def _normalize_key(self, text: str) -> str:
        """标准化键名（小写，下划线）"""
        return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')
    
    def _generate_location_variations(self, location_name: str) -> Dict[str, Any]:
        """生成地点名称变体"""
        variations = {
            "confirmed": {
                "formal": [location_name],
                "informal": [],
                "functional": [],
                "contextual": []
            },
            "pending_review": [],
            "forbidden": []
        }
        
        # 自动生成常见变体
        if "Casa" in location_name:
            parts = location_name.split()
            if len(parts) > 2:
                # Casa Vista Verde -> Casa Vista
                variations["confirmed"]["informal"].append(" ".join(parts[:2]))
            variations["confirmed"]["informal"].append("the casa")
            variations["confirmed"]["functional"].extend(["the inn", "the B&B"])
            variations["confirmed"]["contextual"].extend(["this place", "here"])
        
        return variations
    
    def _generate_character_variations(self, character_name: str) -> Dict[str, Any]:
        """生成角色名称变体"""
        variations = {
            "confirmed": {
                "formal": [],
                "informal": [],
                "narrative": []
            },
            "pending_review": [],
            "forbidden": []
        }
        
        parts = character_name.split()
        if len(parts) >= 2:
            # Sarah Mitchell -> Sarah, Mrs. Mitchell, Ms. Mitchell
            first_name = parts[0]
            last_name = parts[-1]
            variations["confirmed"]["informal"].append(first_name)
            variations["confirmed"]["formal"].extend([
                f"Mrs. {last_name}",
                f"Ms. {last_name}",
                f"Mr. {last_name}"  # Will be filtered based on gender
            ])
        
        return variations
    
    def _extract_critical_facts(self, character_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取关键事实（不可改变）"""
        critical_facts = {}
        
        # 年龄
        if "age" in character_data:
            critical_facts["age"] = {
                "value": character_data["age"],
                "acceptable_forms": [str(character_data["age"])]
            }
        
        # 职业历史
        if "occupation_former" in character_data:
            if "years" in str(character_data.get("backstory_key_elements", "")):
                # 提取年数
                import re
                years_match = re.search(r'(\d+)\s*years?', str(character_data.get("backstory_key_elements", "")))
                if years_match:
                    critical_facts["police_years"] = {
                        "value": int(years_match.group(1)),
                        "acceptable_forms": [years_match.group(1), f"{years_match.group(1)} years"]
                    }
        
        return critical_facts
    
    def is_approved_variation(self, text: str, entity_type: str = None, context: str = None) -> bool:
        """检查是否是已批准的变体"""
        text_lower = text.lower().strip()
        
        # 搜索所有实体类型
        for entity_category in self.dictionary["entities"].values():
            for entity_key, entity_data in entity_category.items():
                # 检查规范名称
                if entity_data["canonical"].lower() == text_lower:
                    return True
                
                # 检查确认的变体
                if "variations" in entity_data and "confirmed" in entity_data["variations"]:
                    for var_key, var_data in entity_data["variations"]["confirmed"].items():
                        # Handle different variation structures
                        if isinstance(var_data, dict):
                            # Complex structure with values key
                            if "values" in var_data:
                                values = var_data["values"]
                                if isinstance(values, list):
                                    for v in values:
                                        if v.lower() == text_lower:
                                            return True
                            # Perspective-based variations
                            else:
                                for perspective_values in var_data.values():
                                    if isinstance(perspective_values, list):
                                        for v in perspective_values:
                                            if v.lower() == text_lower:
                                                return True
                        elif isinstance(var_data, list):
                            # Simple list structure
                            for variation in var_data:
                                if variation.lower() == text_lower:
                                    return True
        
        return False
    
    def is_forbidden(self, text: str) -> Tuple[bool, Optional[str]]:
        """检查是否是禁止的变体"""
        normalized = self._normalize_key(text)
        
        for entity_category in self.dictionary["entities"].values():
            for entity_key, entity_data in entity_category.items():
                if "variations" in entity_data and "forbidden" in entity_data["variations"]:
                    for forbidden_item in entity_data["variations"]["forbidden"]:
                        if isinstance(forbidden_item, dict):
                            if self._normalize_key(forbidden_item.get("value", "")) == normalized:
                                return True, forbidden_item.get("reason", "Forbidden variation")
                        elif isinstance(forbidden_item, str):
                            if self._normalize_key(forbidden_item) == normalized:
                                return True, "Forbidden variation"
        
        return False, None
    
    def get_canonical_name(self, text: str) -> Optional[str]:
        """获取规范名称"""
        normalized = self._normalize_key(text)
        
        for entity_category in self.dictionary["entities"].values():
            for entity_key, entity_data in entity_category.items():
                # 检查是否匹配实体或其变体
                if entity_key == normalized:
                    return entity_data["canonical"]
                
                # 检查变体
                if "variations" in entity_data and "confirmed" in entity_data["variations"]:
                    for variation_list in entity_data["variations"]["confirmed"].values():
                        if isinstance(variation_list, list):
                            for variation in variation_list:
                                if self._normalize_key(variation) == normalized:
                                    return entity_data["canonical"]
        
        return None
    
    def check_critical_fact(self, fact_type: str, value: Any, entity_name: str) -> Tuple[bool, Optional[str]]:
        """检查关键事实是否正确"""
        normalized_entity = self._normalize_key(entity_name)
        
        for entity_category in self.dictionary["entities"].values():
            for entity_key, entity_data in entity_category.items():
                if entity_key == normalized_entity:
                    if "critical_facts" in entity_data and fact_type in entity_data["critical_facts"]:
                        fact_def = entity_data["critical_facts"][fact_type]
                        correct_value = fact_def.get("value")
                        acceptable_forms = fact_def.get("acceptable_forms", [])
                        
                        # 检查值是否正确
                        if str(value) == str(correct_value):
                            return True, None
                        if str(value) in acceptable_forms:
                            return True, None
                        
                        # 值不正确
                        return False, f"Should be {correct_value}, not {value}"
        
        return True, None  # 如果没有找到定义，默认接受
    
    def learn_from_chapter(self, chapter_num: int, chapter_content: str, quality_score: float) -> Dict[str, Any]:
        """从高质量章节学习新模式"""
        if quality_score < self.learning_threshold:
            return {"status": "skipped", "reason": f"Score {quality_score} below threshold {self.learning_threshold}"}
        
        learned_patterns = []
        
        # 提取潜在的变体模式
        patterns = self._extract_entity_patterns(chapter_content)
        
        for pattern in patterns:
            confidence = self._calculate_pattern_confidence(pattern)
            
            if confidence >= self.auto_accept_confidence:
                # 自动接受高置信度模式
                self._add_confirmed_variation(pattern)
                learned_patterns.append({
                    "pattern": pattern["text"],
                    "entity": pattern["entity"],
                    "status": "auto_accepted",
                    "confidence": confidence
                })
            elif confidence >= self.manual_review_threshold:
                # 添加到待审核
                self._add_to_pending_review(pattern, chapter_num, confidence)
                learned_patterns.append({
                    "pattern": pattern["text"],
                    "entity": pattern["entity"],
                    "status": "pending_review",
                    "confidence": confidence
                })
        
        # 更新学习记录
        if chapter_num not in self.dictionary["metadata"]["chapters_learned_from"]:
            self.dictionary["metadata"]["chapters_learned_from"].append(chapter_num)
        
        self.save_dictionary()
        
        return {
            "status": "learned",
            "patterns_found": len(learned_patterns),
            "auto_accepted": len([p for p in learned_patterns if p["status"] == "auto_accepted"]),
            "pending_review": len([p for p in learned_patterns if p["status"] == "pending_review"]),
            "details": learned_patterns
        }
    
    def _extract_entity_patterns(self, content: str) -> List[Dict[str, Any]]:
        """从内容中提取实体模式（简化版）"""
        patterns = []
        
        # 这里应该使用更复杂的NLP技术
        # 现在用简单的规则示例
        
        # 查找 "the casa" 类型的引用
        casa_patterns = re.findall(r'\b(the casa|Casa Vista|the inn|the B&B)\b', content, re.IGNORECASE)
        for pattern in set(casa_patterns):
            patterns.append({
                "text": pattern,
                "entity": "casa_vista_verde",
                "type": "location",
                "context": "narrative"
            })
        
        return patterns
    
    def _calculate_pattern_confidence(self, pattern: Dict[str, Any]) -> float:
        """计算模式置信度"""
        # 简化版置信度计算
        base_confidence = 0.5
        
        # 如果是常见变体，增加置信度
        common_variations = ["the casa", "the inn", "Casa Vista"]
        if pattern["text"] in common_variations:
            base_confidence += 0.3
        
        # 如果出现多次，增加置信度
        # （这里需要实际统计出现次数）
        base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _add_confirmed_variation(self, pattern: Dict[str, Any]):
        """添加确认的变体"""
        entity_type = pattern["type"]
        entity_key = pattern["entity"]
        
        if entity_type in self.dictionary["entities"]:
            if entity_key in self.dictionary["entities"][entity_type]:
                entity = self.dictionary["entities"][entity_type][entity_key]
                if "variations" not in entity:
                    entity["variations"] = {"confirmed": {}, "pending_review": [], "forbidden": []}
                
                # 添加到适当的类别
                context = pattern.get("context", "general")
                if context not in entity["variations"]["confirmed"]:
                    entity["variations"]["confirmed"][context] = []
                
                if pattern["text"] not in entity["variations"]["confirmed"][context]:
                    entity["variations"]["confirmed"][context].append(pattern["text"])
    
    def _add_to_pending_review(self, pattern: Dict[str, Any], chapter_num: int, confidence: float):
        """添加到待审核列表"""
        pending_entry = {
            "pattern": pattern["text"],
            "entity": pattern["entity"],
            "source_chapter": chapter_num,
            "confidence": confidence,
            "context": pattern.get("context", "unknown"),
            "status": "pending_review",
            "timestamp": datetime.now().isoformat()
        }
        
        self.dictionary["learning_log"]["pending_patterns"].append(pending_entry)
    
    def get_pending_reviews(self) -> List[Dict[str, Any]]:
        """获取待审核的模式"""
        return self.dictionary["learning_log"]["pending_patterns"]
    
    def approve_pattern(self, pattern_index: int):
        """批准待审核的模式"""
        if 0 <= pattern_index < len(self.dictionary["learning_log"]["pending_patterns"]):
            pattern = self.dictionary["learning_log"]["pending_patterns"].pop(pattern_index)
            # 转换为确认的变体
            self._add_confirmed_variation({
                "text": pattern["pattern"],
                "entity": pattern["entity"],
                "type": "location",  # 需要从实体类型推断
                "context": pattern["context"]
            })
            self.save_dictionary()
            return True
        return False
    
    def reject_pattern(self, pattern_index: int, reason: str = ""):
        """拒绝待审核的模式"""
        if 0 <= pattern_index < len(self.dictionary["learning_log"]["pending_patterns"]):
            pattern = self.dictionary["learning_log"]["pending_patterns"].pop(pattern_index)
            pattern["status"] = "rejected"
            pattern["rejection_reason"] = reason
            pattern["rejected_at"] = datetime.now().isoformat()
            self.dictionary["learning_log"]["rejected_patterns"].append(pattern)
            self.save_dictionary()
            return True
        return False


# 使用示例
if __name__ == "__main__":
    manager = EntityDictionaryManager()
    
    # 测试变体检查
    print(manager.is_approved_variation("Casa Vista"))  # 应该返回True（如果已配置）
    print(manager.is_approved_variation("the inn"))     # 应该返回True
    
    # 测试关键事实检查
    is_valid, error = manager.check_critical_fact("police_years", "25", "Sarah Mitchell")
    print(f"25 years is valid: {is_valid}")
    
    is_valid, error = manager.check_critical_fact("police_years", "30", "Sarah Mitchell")
    print(f"30 years is valid: {is_valid}, error: {error}")