import sys
import csv

# noqa Account name, Project name, date (YYYY-MM-DD), duration (month), expected annual yield, initial investment, current price, currency
# "Tudigo","chateau o","2023-12-25",12,8,10000,10000,"EUR"
# "Anaxago","Immeuble A","2023-12-25",12,8,10000,10000,"EUR"


def import_crowdlending_generic_csv(filename: str):
    results = []
    with open(filename, newline="") as csvfile:
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        if has_header:
            next(csv_reader)
        for row in csv_reader:
            keys = [
                "account_name",
                "name",
                "start_date",
                "month_duration",
                "annual_yield",
                "initial_investment",
                "current_price",
                "currency_code",
            ]
            results.append({keys[i]: row[i] for i in range(len(keys))})

    return results


def main() -> int:  # pragma: nocover
    """Main entry point."""
    args = sys.argv[1:]
    result = import_crowdlending_generic_csv(args[0])
    import json

    print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
