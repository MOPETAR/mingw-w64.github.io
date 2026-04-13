import json

from .pipeline import run_phase1_pipeline


if __name__ == "__main__":
    print(json.dumps(run_phase1_pipeline(), ensure_ascii=False, indent=2))
