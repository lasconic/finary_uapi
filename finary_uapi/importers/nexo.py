import logging
import sys
from typing import Dict

CryptoLines = Dict[str, Dict[str, float]]


def add_quantity(
    results: CryptoLines, currency: str, amount: float, price: float
) -> None:
    if currency not in results:
        results[currency] = {"quantity": amount, "price": price / amount}
    else:
        old_amount = results[currency]["quantity"]
        old_price = results[currency]["price"]
        results[currency]["quantity"] += amount
        if (old_amount + amount) != 0:
            results[currency]["price"] = (old_amount * old_price + price) / (
                old_amount + amount
            )


def import_nexo_csv(filename: str, diff_stacked: bool = False):
    file = open(filename, "r")
    list = file.readlines()
    file.close()

    list.pop(0)
    list.reverse()
    op_type = set()
    results: CryptoLines = {}
    for line in list:
        fields = line.split(",")
        input_currency = fields[2]
        currency = fields[4]
        amount = float(fields[5])
        if amount == 0:
            continue
        price = 0.0

        type = fields[1]
        op_type.add(type)
        if type == "Exchange":
            currency_price = float(fields[3])
            if input_currency == "EURX":
                price = -currency_price
            logging.debug(
                f"exchanged {amount} {currency} for {currency_price} {input_currency}"
            )
            add_quantity(
                results, input_currency, currency_price, 0
            )  # We substract the other currency
        elif type in [
            "Cashback",
            "Exchange Cashback",
            "Top up Crypto",
            "Referral Bonus",
            "Fixed Term Interest",
            "Interest",
            "Deposit To Exchange",
        ]:
            price = 0  # Nothing to change, just add it
        elif type in ["Withdrawal"]:
            amount = -amount
        elif type in ["Exchange To Withdraw", "Credit Card Fiatx Exchange To Withdraw"]:
            amount = -float(fields[3])
            currency = input_currency
        elif type == "Manual Sell Order":
            amount = float(fields[3])
            currency = input_currency
        else:
            continue

        add_quantity(results, currency, amount, price)

    # delete very small values
    delete = [key for key in results if abs(results[key]["quantity"]) < 1e-12]
    for key in delete:
        del results[key]

    total = 0.0
    for k in sorted(results.keys()):
        logging.debug(f'    "{k}": "{results[k]}"')
        total += results[k]["quantity"] * results[k]["price"]
        # EURX not available on Finary - Updating to EURS before submitting
        if k == "EURX":
            results["EURS"] = results[k]
            del results[k]
            logging.info("EURX is not supported by Finary and was changed to EURS")
    logging.info(f"Total invested : {total}")
    print(sorted(op_type))
    return results


def main() -> int:  # pragma: nocover
    """Main entry point."""
    logging.basicConfig(level=logging.DEBUG)
    args = sys.argv[1:]
    result = import_nexo_csv(args[0], len(args) > 1)
    import json

    print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
