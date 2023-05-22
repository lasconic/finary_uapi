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


def import_cc_csv(filename: str, diff_stacked: bool = False):
    file = open(filename, "r")
    list = file.readlines()
    file.close()

    list.pop(0)
    list.reverse()

    results: CryptoLines = {}
    for line in list:
        fields = line.split(",")
        currency = fields[2]
        amount = float(fields[3])
        price = 0.0

        type = fields[9]
        if type == "viban_purchase":
            currency = fields[4]
            amount = float(fields[5])
            price = float(fields[7])
        elif type in [
            "lockup_lock",
            "lockup_unlock",
            "lockup_upgrade",
            "supercharger_deposit",
            "supercharger_withdrawal",
            "crypto_earn_program_created",
            "crypto_earn_program_withdrawn",
        ]:
            if not diff_stacked:
                continue
            currency = currency + " (stacked)"
            price = 0
            amount = -amount
        elif type in ["crypto_exchange", "trading.limit_order.crypto_wallet.exchange"]:
            exchange_currency = fields[4]
            exchange_amount = float(fields[5])
            exchange_price = (
                results[currency]["price"] * -1 * amount
            ) / exchange_amount
            add_quantity(results, exchange_currency, exchange_amount, exchange_price)
        elif type in ["trading.limit_order.crypto_wallet.fund_lock"]:
            continue

        add_quantity(results, currency, amount, price)

    # delete very small values
    delete = [key for key in results if abs(results[key]["quantity"]) < 1e-12]
    for key in delete:
        del results[key]

    # remove stacked from total, and fix the price of stacked
    for k in results.keys():
        if k.endswith("(stacked)"):
            original_currency = k.split(" ")[0]
            # logging.debug(results[k])
            # logging.debug(results[original_currency])
            results[k]["price"] = results[original_currency]["price"]
            results[original_currency]["quantity"] -= results[k]["quantity"]

    total = 0.0
    for k in sorted(results.keys()):
        logging.debug(f'    "{k}": "{results[k]}"')
        total += results[k]["quantity"] * results[k]["price"]
    logging.info(f"Total invested : {total}")
    return results


def main() -> int:  # pragma: nocover
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    args = sys.argv[1:]
    result = import_cc_csv(args[0], len(args) > 1)
    import json

    print(json.dumps(result, indent=4))
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
