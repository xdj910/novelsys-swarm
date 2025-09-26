#!/usr/bin/env python3
"""
Entity Dictionary Manager Script
Handles creation and updates of entity dictionaries from Bible and high-quality chapters
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class EntityDictionaryManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path(f"data/projects/{project_name}")
        self.dict_path = self.project_path / "shared" / "entity_dictionary.yaml"
        # No longer use system-wide shared path
        
    def create_from_bible(self, bible_path: str) -> None:
        """Create entity dictionary from project Bible"""
        print(f"Creating entity dictionary for project: {self.project_name}")
        
        # Load Bible
        with open(bible_path, 'r', encoding='utf-8') as f:
            bible = yaml.safe_load(f)
        
        # Extract entities
        entities = self._extract_entities_from_bible(bible)
        
        # Create dictionary structure
        entity_dict = {
            "metadata": {
                "version": "1.0",
                "project": self.project_name,
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "learning_threshold": 95,
                "auto_accept_confidence": 0.95,
                "manual_review_threshold": 0.80,
                "chapters_learned_from": []
            },
            "configuration": {
                "locations": {
                    "allow_variations": True,
                    "strict_on_facts": True
                },
                "characters": {
                    "allow_informal_references": True,
                    "strict_on_critical_facts": True
                },
                "objects": {
                    "allow_functional_descriptions": True,
                    "maintain_consistency": True
                }
            },
            "entities": entities,
            "learning_log": {
                "pending_patterns": [],
                "rejected_patterns": [],
                "learned_patterns": []
            }
        }
        
        # Save to project directory
        self.dict_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            yaml.dump(entity_dict, f, allow_unicode=True, default_flow_style=False)
        
        # Also save to shared directory
        self.shared_dict_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.shared_dict_path, 'w', encoding='utf-8') as f:
            yaml.dump(entity_dict, f, allow_unicode=True, default_flow_style=False)
        
        print(f"[SUCCESS] Created entity dictionary with {len(entities.get('characters', {}))} characters, {len(entities.get('locations', {}))} locations")
        print(f"   Saved to: {self.dict_path}")
        
    def _extract_entities_from_bible(self, bible: Dict) -> Dict:
        """Extract entities from Bible content"""
        entities = {
            "locations": {},
            "characters": {},
            "objects": {}
        }
        
        # Extract characters
        characters = bible.get("characters", {})
        
        # Process protagonists
        for char in characters.get("protagonists", []):
            char_key = self._create_key(char.get("name", "unknown"))
            entities["characters"][char_key] = {
                "canonical": char.get("name"),
                "source": "bible",
                "bible_reference": f"characters.protagonists",
                "critical_facts": {
                    "age": char.get("age"),
                    "profession": char.get("profession"),
                    "background": char.get("background"),
                    "relationships": char.get("relationships", [])
                },
                "variations": {
                    "confirmed": {
                        "formal": [char.get("name")],
                        "informal": [],
                        "nicknames": char.get("nicknames", [])
                    },
                    "forbidden": [],
                    "pending_review": []
                }
            }
        
        # Process antagonists
        for char in characters.get("antagonists", []):
            char_key = self._create_key(char.get("name", "unknown"))
            entities["characters"][char_key] = {
                "canonical": char.get("name"),
                "source": "bible",
                "bible_reference": f"characters.antagonists",
                "critical_facts": {
                    "role": char.get("role"),
                    "motivation": char.get("motivation")
                },
                "variations": {
                    "confirmed": {
                        "formal": [char.get("name")],
                        "informal": []
                    },
                    "forbidden": [],
                    "pending_review": []
                }
            }
        
        # Process supporting characters
        for char in characters.get("supporting", []):
            char_key = self._create_key(char.get("name", "unknown"))
            entities["characters"][char_key] = {
                "canonical": char.get("name"),
                "source": "bible",
                "bible_reference": f"characters.supporting",
                "critical_facts": {
                    "role": char.get("role"),
                    "relationship": char.get("relationship")
                },
                "variations": {
                    "confirmed": {
                        "formal": [char.get("name")],
                        "informal": []
                    },
                    "forbidden": [],
                    "pending_review": []
                }
            }
        
        # Extract locations from world_building
        world = bible.get("world_building", {})
        
        # Primary setting
        primary_setting = world.get("primary_setting", {})
        if primary_setting.get("name"):
            loc_key = self._create_key(primary_setting["name"])
            entities["locations"][loc_key] = {
                "canonical": primary_setting["name"],
                "source": "bible",
                "bible_reference": "world_building.primary_setting",
                "critical_facts": {
                    "type": primary_setting.get("type"),
                    "description": primary_setting.get("description"),
                    "significance": primary_setting.get("significance")
                },
                "variations": {
                    "confirmed": {
                        "formal": [primary_setting["name"]],
                        "informal": []
                    },
                    "forbidden": [],
                    "pending_review": []
                }
            }
        
        # Key locations
        for idx, location in enumerate(world.get("key_locations", [])):
            if location.get("name"):
                loc_key = self._create_key(location["name"])
                entities["locations"][loc_key] = {
                    "canonical": location["name"],
                    "source": "bible",
                    "bible_reference": f"world_building.key_locations[{idx}]",
                    "critical_facts": {
                        "description": location.get("description"),
                        "significance": location.get("significance")
                    },
                    "variations": {
                        "confirmed": {
                            "formal": [location["name"]],
                            "informal": []
                        },
                        "forbidden": [],
                        "pending_review": []
                    }
                }
        
        # Extract important objects
        for idx, obj in enumerate(world.get("important_objects", [])):
            if obj.get("name"):
                obj_key = self._create_key(obj["name"])
                entities["objects"][obj_key] = {
                    "canonical": obj["name"],
                    "source": "bible",
                    "bible_reference": f"world_building.important_objects[{idx}]",
                    "critical_facts": {
                        "description": obj.get("description"),
                        "significance": obj.get("significance")
                    },
                    "variations": {
                        "confirmed": {
                            "formal": [obj["name"]],
                            "informal": []
                        },
                        "forbidden": [],
                        "pending_review": []
                    }
                }
        
        return entities
    
    def update_from_chapter(self, chapter_num: int, quality_score: float) -> None:
        """Update dictionary from high-quality chapter"""
        if quality_score < 95:
            print(f"[WARNING] Chapter {chapter_num} score ({quality_score}) < 95, skipping learning")
            return
        
        print(f"[LEARNING] Learning from chapter {chapter_num} (score: {quality_score})")
        
        # Load existing dictionary
        if not self.dict_path.exists():
            print(f"[ERROR] Entity dictionary not found at {self.dict_path}")
            return
            
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            entity_dict = yaml.safe_load(f)
        
        # Check if already learned from this chapter
        if chapter_num in entity_dict["metadata"].get("chapters_learned_from", []):
            print(f"[INFO] Already learned from chapter {chapter_num}")
            return
        
        # Read chapter content
        chapter_path = self.project_path / f"chapters/ch{chapter_num:03d}/content.md"
        if not chapter_path.exists():
            print(f"[ERROR] Chapter file not found: {chapter_path}")
            return
            
        with open(chapter_path, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        # Extract variations (simplified logic)
        new_variations = self._extract_variations(chapter_content, entity_dict)
        
        # Update dictionary with new variations
        updates_made = 0
        for entity_type, variations in new_variations.items():
            for entity_key, new_vars in variations.items():
                if entity_key in entity_dict["entities"].get(entity_type, {}):
                    existing_informal = entity_dict["entities"][entity_type][entity_key]["variations"]["confirmed"].get("informal", [])
                    for var in new_vars:
                        if var not in existing_informal:
                            existing_informal.append(var)
                            updates_made += 1
                            print(f"   + Added variation: {entity_key} → '{var}'")
        
        # Update metadata
        entity_dict["metadata"]["chapters_learned_from"].append(chapter_num)
        entity_dict["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Add to learning log
        entity_dict["learning_log"]["learned_patterns"].append({
            "chapter": chapter_num,
            "score": quality_score,
            "timestamp": datetime.now().isoformat(),
            "variations_added": updates_made
        })
        
        # Save updated dictionary
        with open(self.dict_path, 'w', encoding='utf-8') as f:
            yaml.dump(entity_dict, f, allow_unicode=True, default_flow_style=False)
        
        # Update shared dictionary
        with open(self.shared_dict_path, 'w', encoding='utf-8') as f:
            yaml.dump(entity_dict, f, allow_unicode=True, default_flow_style=False)
        
        print(f"[SUCCESS] Updated entity dictionary: {updates_made} new variations added")
        print(f"   Total chapters learned from: {len(entity_dict['metadata']['chapters_learned_from'])}")
    
    def _extract_variations(self, content: str, entity_dict: Dict) -> Dict:
        """Extract potential variations from chapter content"""
        # This is a simplified implementation
        # In production, would use NLP to identify entity references
        
        variations = {
            "characters": {},
            "locations": {},
            "objects": {}
        }
        
        # For now, just return empty - would need proper NLP implementation
        # to actually extract variations from text
        
        return variations
    
    def _create_key(self, name: str) -> str:
        """Create a valid key from entity name"""
        return name.lower().replace(" ", "_").replace("-", "_")
    
    def get_status(self) -> Dict:
        """Get current dictionary status"""
        if not self.dict_path.exists():
            return {"exists": False}
        
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            entity_dict = yaml.safe_load(f)
        
        return {
            "exists": True,
            "project": entity_dict["metadata"].get("project"),
            "created": entity_dict["metadata"].get("created"),
            "last_updated": entity_dict["metadata"].get("last_updated"),
            "total_entities": sum(len(entities) for entities in entity_dict["entities"].values()),
            "chapters_learned": len(entity_dict["metadata"].get("chapters_learned_from", [])),
            "characters": len(entity_dict["entities"].get("characters", {})),
            "locations": len(entity_dict["entities"].get("locations", {})),
            "objects": len(entity_dict["entities"].get("objects", {}))
        }


def main():
    """Main entry point for command-line usage"""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python entity_dict_manager.py create <project_name> <bible_path>")
        print("  python entity_dict_manager.py update <project_name> <chapter_num> <quality_score>")
        print("  python entity_dict_manager.py status <project_name>")
        sys.exit(1)
    
    command = sys.argv[1]
    project_name = sys.argv[2]
    
    manager = EntityDictionaryManager(project_name)
    
    if command == "create":
        if len(sys.argv) < 4:
            print("Error: Bible path required for create command")
            sys.exit(1)
        bible_path = sys.argv[3]
        manager.create_from_bible(bible_path)
        
    elif command == "update":
        if len(sys.argv) < 5:
            print("Error: Chapter number and quality score required for update command")
            sys.exit(1)
        chapter_num = int(sys.argv[3])
        quality_score = float(sys.argv[4])
        manager.update_from_chapter(chapter_num, quality_score)
        
    elif command == "status":
        status = manager.get_status()
        if not status["exists"]:
            print(f"[ERROR] No entity dictionary found for project: {project_name}")
        else:
            print(f"[STATUS] Entity Dictionary Status for '{project_name}':")
            print(f"   Created: {status['created']}")
            print(f"   Last Updated: {status['last_updated']}")
            print(f"   Total Entities: {status['total_entities']}")
            print(f"   - Characters: {status['characters']}")
            print(f"   - Locations: {status['locations']}")
            print(f"   - Objects: {status['objects']}")
            print(f"   Chapters Learned From: {status['chapters_learned']}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()