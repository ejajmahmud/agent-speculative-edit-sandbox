"""CLI for agent-speculative-edit-sandbox."""
import sys
import argparse
from .sandbox import SpeculativeSandbox


def main():
    parser = argparse.ArgumentParser(description="Agent Speculative Edit Sandbox CLI")
    parser.add_argument("--demo", action="store_true", help="Run speculative sandbox demo with valid and invalid code")
    args = parser.parse_args()

    if args.demo:
        sb = SpeculativeSandbox()
        res_valid = sb.stage_file("service.py", "def compute():\n    return 42\n")
        print(f"Valid Stage: Status={res_valid.valid} | Nodes={res_valid.ast_nodes}")

        res_invalid = sb.stage_file("service.py", "def broken_syntax(\n    return 42\n")
        print(f"Invalid Stage: Status={res_invalid.valid} | Error={res_invalid.error}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
