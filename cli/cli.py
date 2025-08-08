import argparse
from dependency_injection.container import ServiceContainer

def main():
    container = ServiceContainer()
    text_loader = container.load_text_uc

    parser = argparse.ArgumentParser(description="Quran Viewer CLI")
    parser.add_argument("sura", type=int, help="Sura ID")
    parser.add_argument("aya", type=int, nargs="?", default=0, help="Optional Aya ID")
    args = parser.parse_args()

    result = text_loader.execute(args.sura, args.aya)
    for aya_id, text in result:
        print(f"[{aya_id}] {text}")

if __name__ == "__main__":
    main()