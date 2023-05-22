import csv
import sys


# code,quantity,price
# BTC,1.5,13456.77
def import_crypto_generic_csv(filename: str):
    results = {}
    with open(filename, newline="") as csvfile:
        sniffer = csv.Sniffer()
        has_header = sniffer.has_header(csvfile.read(2048))
        csvfile.seek(0)
        csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
        if has_header:
            next(csv_reader)
        for row in csv_reader:
            code = row[0]
            quantity = float(row[1])
            price = float(row[2])
            if code not in results:
                results[code] = {"quantity": quantity, "price": price}
            else:
                old_quantity = float(results[code]["quantity"])
                old_price = float(results[code]["price"])
                results[code] = {
                    "quantity": quantity + old_quantity,
                    "price": (old_quantity * old_price + price)
                    / (old_quantity + quantity),
                }
    return results


def main() -> int:  # pragma: nocover
    """Main entry point."""
    args = sys.argv[1:]
    result = import_crypto_generic_csv(args[0])
    import json

    print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
