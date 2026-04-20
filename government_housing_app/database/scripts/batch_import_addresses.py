from __future__ import annotations

import argparse
from pathlib import Path

from store_test_lookup import ensure_database_ready, store_lookup


def load_addresses(file_path: Path | None, inline_addresses: list[str]) -> list[str]:
    addresses = list(inline_addresses)
    if file_path is not None:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        addresses.extend(line.strip() for line in lines if line.strip() and not line.strip().startswith("#"))
    deduped: list[str] = []
    seen: set[str] = set()
    for address in addresses:
        if address not in seen:
            deduped.append(address)
            seen.add(address)
    return deduped


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Batch import multiple addresses into raw JSON storage and SQLite."
    )
    parser.add_argument(
        "addresses",
        nargs="*",
        help='One or more addresses. Example: "1600 Pennsylvania Ave NW, Washington, DC 20500"',
    )
    parser.add_argument(
        "--file",
        help="Optional text file with one address per line. Lines starting with # are ignored.",
    )
    args = parser.parse_args()

    file_path = Path(args.file).expanduser().resolve() if args.file else None
    addresses = load_addresses(file_path, args.addresses)
    if not addresses:
        raise SystemExit("No addresses supplied. Pass addresses directly or use --file.")

    ensure_database_ready()

    successes = 0
    failures = 0
    for index, address in enumerate(addresses, start=1):
        print(f"[{index}/{len(addresses)}] {address}")
        try:
            result = store_lookup(address)
        except Exception as exc:
            failures += 1
            print(f"  failed: {exc}")
            continue

        successes += 1
        geocode_result = result["geocode_result"]
        tract_metrics = result["tract_metrics"]
        print(f"  matched: {geocode_result['matched_address']}")
        print(f"  tract: {geocode_result['geoid_tract']}")
        if tract_metrics["median_home_value_usd"] is None:
            print("  price: data unavailable for this tract")
        else:
            print(f"  price: ${tract_metrics['median_home_value_usd']:,.0f}")

    print()
    print("Batch import summary")
    print(f"  total: {len(addresses)}")
    print(f"  successes: {successes}")
    print(f"  failures: {failures}")


if __name__ == "__main__":
    main()
