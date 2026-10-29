#!/usr/bin/env python3
"""
RIE TAXONOMY LOADER v1.0 — Externalized Dynamic Ontology Engine
Directive Reference: RIE-DIR-L5-PHASE-6B-IMPLEMENTATION-REMEDIATION-v1.0
Governing Authority: Human Architect Level 5 — Human Architect
Execution Steward: RIE-STEWARD-001 (Autonomous Repository Steward)
Classification: SYSTEM_COMPONENT (REMEDIATION_V3_DEV)
Operating Mode: ZERO NETWORK — DETERMINISTIC OFFLINE ONTOLOGY

Purpose:
Loads, validates, and manages domain ontologies from external JSON definitions.
Decouples domain knowledge (finance, environmental engineering, photogrammetry, etc.)
from core engine code, enabling runtime adaptation without engine modification.
"""

import os
import sys
import re
import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple

def log_provenance() -> Tuple[str, str]:
    """Mandatory Self-Verifying Provenance Header."""
    script_path = os.path.abspath(__file__)
    try:
        with open(script_path, "rb") as f:
            content_hash = hashlib.sha256(f.read()).hexdigest()
    except Exception as e:
        content_hash = f"UNKNOWN ({e})"
    return script_path, content_hash

DEFAULT_TAXONOMY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "core_domains.json"
)

class TaxonomyLoader:
    """
    Manages externalized domain ontologies for RIE epistemic engines.
    """
    def __init__(self, taxonomy_path: Optional[str] = None):
        self.taxonomy_path = taxonomy_path or DEFAULT_TAXONOMY_PATH
        self.taxonomy_data: Dict[str, Any] = {}
        self.load_taxonomy()

    def load_taxonomy(self, custom_path: Optional[str] = None) -> None:
        """Loads domain taxonomy from JSON file."""
        target = custom_path or self.taxonomy_path
        if not os.path.exists(target):
            raise FileNotFoundError(f"Domain taxonomy file not found: {target}")
        
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Basic schema integrity verification
        if "domains" not in data or not isinstance(data["domains"], dict):
            raise ValueError(f"Invalid taxonomy structure in {target}: missing 'domains' dictionary")
            
        self.taxonomy_data = data
        self.taxonomy_path = target

    def list_domains(self) -> List[str]:
        """Returns list of registered domain keys."""
        return list(self.taxonomy_data.get("domains", {}).keys())

    def get_domain(self, domain_key: str) -> Dict[str, Any]:
        """Retrieves domain configuration dictionary."""
        domains = self.taxonomy_data.get("domains", {})
        if domain_key in domains:
            return domains[domain_key]
        # Fallback to default domain or first available domain
        default_key = self.taxonomy_data.get("default_domain", "macroeconomics")
        if default_key in domains:
            return domains[default_key]
        if domains:
            return next(iter(domains.values()))
        raise KeyError(f"No domains registered in taxonomy.")

    def add_domain(self, domain_key: str, domain_def: Dict[str, Any]) -> None:
        """Adds a new domain to the runtime taxonomy."""
        required_keys = ["domain_id", "domain_code", "display_name", "entity_keywords"]
        for rk in required_keys:
            if rk not in domain_def:
                raise ValueError(f"Domain definition missing required key: {rk}")
                
        if "domains" not in self.taxonomy_data:
            self.taxonomy_data["domains"] = {}
        self.taxonomy_data["domains"][domain_key] = domain_def

    def remove_domain(self, domain_key: str) -> bool:
        """Removes a domain from the runtime taxonomy."""
        domains = self.taxonomy_data.get("domains", {})
        if domain_key in domains:
            del domains[domain_key]
            return True
        return False

    def modify_domain(self, domain_key: str, updates: Dict[str, Any]) -> bool:
        """Modifies attributes of an existing domain."""
        domains = self.taxonomy_data.get("domains", {})
        if domain_key not in domains:
            return False
        domains[domain_key].update(updates)
        return True

    def discover_module_domains(self, modules_root=None):
        """Auto-discovers and registers domain packs from modules/*/domain_module.json."""
        if modules_root is None:
            modules_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "modules"))
        loaded = []
        if not os.path.exists(modules_root):
            return loaded
        for item in os.listdir(modules_root):
            mod_dir = os.path.join(modules_root, item)
            if not os.path.isdir(mod_dir):
                continue
            manifest = os.path.join(mod_dir, "domain_module.json")
            if os.path.exists(manifest):
                try:
                    with open(manifest, "r", encoding="utf-8") as mf:
                        mod_data = json.load(mf)
                    if mod_data.get("enabled", True):
                        d_id = mod_data.get("domain_id", item)
                        self.add_domain(d_id, mod_data)
                        loaded.append(d_id)
                except Exception as e:
                    print(f"Warning: Failed to load module at {manifest}: {e}", file=sys.stderr)
        return loaded

    def detect_domain_from_text(self, text: str) -> str:
        """
        Dynamically classifies text into the best-matching registered domain
        based on keyword frequency and entity density.
        """
        text_lower = text.lower()
        words = set(re.findall(r'\b[a-zA-Z]{3,}\b', text_lower))
        
        domain_scores: Dict[str, int] = {}
        for d_key, d_def in self.taxonomy_data.get("domains", {}).items():
            keywords = set(k.lower() for k in d_def.get("entity_keywords", []))
            overlap = len(words & keywords)
            domain_scores[d_key] = overlap
            
        if not domain_scores:
            return self.taxonomy_data.get("default_domain", "macroeconomics")
            
        best_domain = max(domain_scores.items(), key=lambda x: x[1])
        if best_domain[1] > 0:
            return best_domain[0]
        return self.taxonomy_data.get("default_domain", "macroeconomics")

    def get_entity_keywords(self, domain_key: str) -> List[str]:
        """Returns entity keywords for given domain."""
        return self.get_domain(domain_key).get("entity_keywords", [])

    def get_polarity_vectors(self, domain_key: str) -> Dict[str, List[str]]:
        """Returns positive and negative polarity vectors for given domain."""
        return self.get_domain(domain_key).get("polarity_vectors", {"positive": [], "negative": []})

    def get_research_question_templates(self, domain_key: str) -> List[str]:
        """Returns research question templates for given domain."""
        return self.get_domain(domain_key).get("research_question_templates", [])

    def get_causal_h1_templates(self, domain_key: str) -> List[str]:
        """Returns causal H1 templates for given domain."""
        return self.get_domain(domain_key).get("causal_h1_templates", [])

    def get_dialectical_h2_templates(self, domain_key: str) -> List[str]:
        """Returns dialectical H2 templates for given domain."""
        return self.get_domain(domain_key).get("dialectical_h2_templates", [])

    def get_concept_blueprints(self, domain_key: str) -> List[Dict[str, Any]]:
        """Returns concept blueprints for given domain."""
        return self.get_domain(domain_key).get("concept_blueprints", [])

    def save_to_file(self, target_path: Optional[str] = None) -> None:
        """Persists current taxonomy to JSON file."""
        target = target_path or self.taxonomy_path
        with open(target, "w", encoding="utf-8") as f:
            json.dump(self.taxonomy_data, f, indent=2)

if __name__ == "__main__":
    path, h = log_provenance()
    print(f"[{os.path.basename(__file__)}] Provenance Verified: {h[:16]}...")
    loader = TaxonomyLoader()
    print(f"Loaded domains: {loader.list_domains()}")
    test_text = "Heavy rainfall caused significant sediment runoff and high turbidity in the silt basin."
    detected = loader.detect_domain_from_text(test_text)
    print(f"Test detection for environmental snippet: '{detected}'")
