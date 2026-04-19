import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_sync_module():
    script_path = (
        Path(__file__).resolve().parents[1]
        / "scripts"
        / "sync_skills_from_manifest.py"
    )
    spec = spec_from_file_location("sync_skills_from_manifest", script_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
