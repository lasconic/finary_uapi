import csv
import sys


# "isin_code", "description","quantity","price","currency"
def import_stocks_generic_csv(filename: str):
    results = []
    with open(filename, newline="") as csvfile:
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        if has_header:
            next(csv_reader)
        for row in csv_reader:
            isin_code = row[0]
            description = row[1]
            quantity = row[2]
            price = row[3]
            currency = row[3]
            results.append(
                {
                    "description": description,
                    "isin_code": isin_code,
                    "quantity": quantity,
                    "price": price,
                    "currency": currency,
                }
            )

    return results


def main() -> int:  # pragma: nocover
    """Main entry point."""
    args = sys.argv[1:]
    result = import_stocks_generic_csv(args[0])
    import json

    print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
