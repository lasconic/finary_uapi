"""
Finary command line
Usage:
    finary_api signin [MFA_CODE]
    finary_api me
    finary_api institution_connections
    finary_api dashboard net [all | 1w | 1m | ytd | 1y]
    finary_api dashboard gross [all | 1w | 1m | ytd | 1y]
    finary_api dashboard finary [all | 1w | 1m | ytd | 1y]
    finary_api portfolio [all | 1w | 1m | ytd | 1y]
    finary_api commodities [all | 1w | 1m | ytd | 1y]
    finary_api checking_accounts [all | 1w | 1m | ytd | 1y]
    finary_api fonds_euro_view [all | 1w | 1m | ytd | 1y]
    finary_api fonds_euro
    finary_api other_assets [all | 1w | 1m | ytd | 1y]
    finary_api saving_accounts [all | 1w | 1m | ytd | 1y]
    finary_api real_estates [all | 1w | 1m | ytd | 1y]
    finary_api startups
    finary_api investments
    finary_api cryptos
    finary_api cryptos distribution
    finary_api cryptos add <code> <quantity> <price> <account_id>
    finary_api cryptos update <code> <quantity> <price> <account_id>
    finary_api cryptos delete <code> <account_id>
    finary_api precious_metals search QUERY
    finary_api precious_metals
    finary_api precious_metals add <name> <quantity> <price>
    finary_api precious_metals delete <commodity_id>
    finary_api holdings_accounts [crypto | stocks | <account_name>]
    finary_api holdings_accounts add (crypto | stocks) <account_name>
    finary_api holdings_accounts add (checking | saving) <account_name> <bank_name> <account_type> <balance>
    finary_api holdings_accounts delete <account_id>
    finary_api holdings_accounts update <account_id> <account_name> [<account_balance>]
    finary_api generic_asset_categories
    finary_api generic_assets
    finary_api generic_assets add <name> <category> <quantity> <buying_price> <current_price>
    finary_api generic_assets update <asset_id> <name> <category> <quantity> <buying_price> <current_price>
    finary_api generic_assets delete <asset_id>
    finary_api crypto_chains
    finary_api crypto_currency search QUERY
    finary_api fiat_currency search QUERY
    finary_api institutions search QUERY
    finary_api securities search QUERY
    finary_api securities
    finary_api securities add <code> <quantity> <price> <account_id>
    finary_api securities delete <security_id>
    finary_api insights
    finary_api fees
    finary_api loans
    finary_api real_estates
    finary_api scpis search QUERY
    finary_api scpis
    finary_api import cryptocom FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_api import crypto_csv FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_api import stocks_csv FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_api import stocks_json FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]

Options:
  --new=NAME          Create a new account and import the lines
  --edit=account_id   Edit the line with new value if it exists, create it otherwise
  --add=account_id    If line exists, add the quantity and change the price accordingly, create it otherwise
"""
import json
import sys

from docopt import docopt

from .auth import prepare_session
from .crypto_chains import get_crypto_chains
from .currencies import get_currencies
from .generic_asset_categories import get_generic_asset_categories
from .user_holdings_accounts import (
    add_checking_saving_account,
    add_holdings_account,
    get_holdings_accounts,
    delete_holdings_account,
    get_holdings_account_per_name_or_id,
    update_holdings_account,
)
from .importers.cryptocom import import_cc_csv
from .importers.crypto_generic_csv import import_crypto_generic_csv
from .importers.stocks_generic_csv import import_stocks_generic_csv
from .institutions import get_institutions
from .user_portfolio import (
    get_portfolio_cryptos_distribution,
    get_portfolio_investments,
)
from .precious_metals import get_precious_metals
from .user_generic_assets import (
    add_user_generic_asset,
    delete_user_generic_asset,
    get_user_generic_assets,
    update_user_generic_asset,
)
from .user_real_estates import get_user_real_estates
from .user_scpis import get_user_scpis
from .scpis import get_scpis
from .securities import get_securities
from .signin import signin
from .user_startups import get_user_startups
from .user_cryptos import (
    add_user_crypto_by_code,
    delete_user_crypto_by_code,
    get_user_cryptos,
    update_user_crypto_by_code,
)
from .user_fonds_euro import get_user_fonds_euro
from .user_me import get_user_me, get_user_me_institution_connections
from .user_precious_metals import (
    add_user_precious_metals_by_name,
    delete_user_precious_metals,
    get_user_precious_metals,
)
from .user_securities import (
    add_imported_securities_to_account,
    add_user_security_by_symbol,
    get_user_securities,
    delete_user_security,
)
from .views import a_period, a_dashboard_type, get_fees, get_insights, get_loans
from .views import (
    get_checking_accounts,
    get_commodities,
    get_dashboard,
    get_fonds_euro,
    get_other_assets,
    get_portfolio,
    get_real_estates,
    get_savings_accounts,
)


def main() -> int:  # pragma: nocover
    """Main entry point."""

    args = docopt(__doc__)
    result = ""
    if args["signin"]:
        result = signin(args["MFA_CODE"])
    else:
        session = prepare_session()
        perioda = [i for i in a_period if args[i]]
        period = perioda[0] if perioda else ""
        if args["me"]:
            result = get_user_me(session)
        elif args["institution_connections"]:
            result = get_user_me_institution_connections(session)
        elif args["dashboard"]:
            type = [i for i in a_dashboard_type if args[i]]
            result = get_dashboard(session, type[0] if type else "", period)
        elif args["portfolio"]:
            result = get_portfolio(session, period)
        elif args["checking_accounts"]:
            result = get_checking_accounts(session, period)
        elif args["saving_accounts"]:
            result = get_savings_accounts(session, period)
        elif args["fonds_euro_view"]:
            result = get_fonds_euro(session, period)
        elif args["fonds_euro"]:
            result = get_user_fonds_euro(session)
        elif args["real_estates"]:
            result = get_real_estates(session, period)
        elif args["other_assets"]:
            result = get_other_assets(session, period)
        elif args["startups"]:
            result = get_user_startups(session)
        elif args["search"]:
            if args["crypto_currency"]:
                result = get_currencies(session, "crypto", args["QUERY"])
            elif args["fiat_currency"]:
                result = get_currencies(session, "fiat", args["QUERY"])
            elif args["institutions"]:
                result = get_institutions(session, args["QUERY"])
            elif args["precious_metals"]:
                result = get_precious_metals(session, args["QUERY"])
            elif args["scpis"]:
                result = get_scpis(session, args["QUERY"])
            elif args["securities"]:
                result = get_securities(session, args["QUERY"])
            else:
                print("Unknown resource for search")
                return 1
        elif args["add"]:
            if args["cryptos"]:
                result = add_user_crypto_by_code(
                    session,
                    args["<code>"],
                    args["<quantity>"],
                    args["<price>"],
                    args["<account_id>"],
                )
            elif args["generic_assets"]:
                result = add_user_generic_asset(
                    session,
                    args["<name>"],
                    args["<category>"],
                    args["<quantity>"],
                    args["<buying_price>"],
                    args["<current_price>"],
                )
            elif args["precious_metals"]:
                result = add_user_precious_metals_by_name(
                    session, args["<name>"], args["<quantity>"], args["<price>"]
                )
            elif args["holdings_accounts"]:
                if args["stocks"]:
                    result = add_holdings_account(
                        session, args["<account_name>"], "stocks"
                    )
                elif args["crypto"]:
                    result = add_holdings_account(
                        session, args["<account_name>"], "crypto"
                    )
                elif args["checking"] or args["saving"]:
                    result = add_checking_saving_account(
                        session,
                        args["<account_name>"],
                        args["<bank_name>"],
                        args["<account_type>"],
                        args["<balance>"],
                    )
            elif args["securities"]:
                result = add_user_security_by_symbol(
                    session,
                    args["<code>"],
                    args["<account_id>"],
                    args["<quantity>"],
                    args["<price>"],
                )
        elif args["update"]:
            if args["cryptos"]:
                result = update_user_crypto_by_code(
                    session,
                    args["<code>"],
                    args["<quantity>"],
                    args["<price>"],
                    args["<account_id>"],
                )
            elif args["generic_assets"]:
                result = update_user_generic_asset(
                    session,
                    args["<asset_id>"],
                    args["<name>"],
                    args["<category>"],
                    args["<quantity>"],
                    args["<buying_price>"],
                    args["<current_price>"],
                )
            elif args["holdings_accounts"]:
                result = update_holdings_account(
                    session,
                    args["<account_id>"],
                    args["<account_name>"],
                    args["<account_balance>"],
                )
        elif args["delete"]:
            if args["cryptos"]:
                result = delete_user_crypto_by_code(
                    session,
                    args["<code>"],
                    args["<account_id>"],
                )
            elif args["generic_assets"]:
                delete_user_generic_asset(session, args["<asset_id>"])
            elif args["holdings_accounts"]:
                result = delete_holdings_account(session, args["<account_id>"])
            elif args["precious_metals"]:
                delete_user_precious_metals(session, args["<commodity_id>"])
            elif args["securities"]:
                delete_user_security(session, args["<security_id>"])
        elif args["commodities"]:
            result = get_commodities(session, period)
        elif args["crypto_chains"]:
            result = get_crypto_chains(session)
        elif args["cryptos"]:
            if args["distribution"]:
                result = get_portfolio_cryptos_distribution(session)
            else:
                result = get_user_cryptos(session)
        elif args["investments"]:
            result = get_portfolio_investments(session)
        elif args["holdings_accounts"]:
            if args["<account_name>"]:
                result = get_holdings_account_per_name_or_id(
                    session, args["<account_name>"]
                )
            else:
                holdings_account_types = ["crypto", "stocks"]
                hats = [i for i in holdings_account_types if args[i]]
                holdings_account_type = hats[0] if hats else ""
                result = get_holdings_accounts(session, holdings_account_type)
        elif args["generic_asset_categories"]:
            result = get_generic_asset_categories(session)
        elif args["generic_assets"]:
            result = get_user_generic_assets(session)
        elif args["precious_metals"]:
            result = get_user_precious_metals(session)
        elif args["securities"]:
            result = get_user_securities(session)
        elif args["fees"]:
            result = get_fees(session)
        elif args["insights"]:
            result = get_insights(session)
        elif args["loans"]:
            result = get_loans(session)
        elif args["real_estates"]:
            result = get_user_real_estates(session)
        elif args["scpis"]:
            result = get_user_scpis(session)
        elif args["import"]:
            to_be_imported = {}
            crypto_import = True
            if args["cryptocom"]:
                to_be_imported = import_cc_csv(args["FILENAME"])
            elif args["crypto_csv"]:
                to_be_imported = import_crypto_generic_csv(args["FILENAME"])
            elif args["stocks_csv"]:
                to_be_imported = import_stocks_generic_csv(args["FILENAME"])
                crypto_import = False
            elif args["stocks_json"]:
                with open(args["FILENAME"], "r") as input_file:
                    to_be_imported = json.loads(input_file.read())
                crypto_import = False

            if to_be_imported:
                if crypto_import:
                    if args["--new"]:
                        account = add_holdings_account(session, args["--new"], "crypto")
                        for crypto_code in to_be_imported:
                            crypto_line = to_be_imported[crypto_code]
                            add_user_crypto_by_code(
                                session,
                                crypto_code,
                                crypto_line["quantity"],
                                crypto_line["price"],
                                account["result"]["id"],
                            )
                    elif args["--edit"]:
                        for crypto_code in to_be_imported:
                            crypto_line = to_be_imported[crypto_code]
                            update_user_crypto_by_code(
                                session,
                                crypto_code,
                                crypto_line["quantity"],
                                crypto_line["price"],
                                args["--edit"],
                            )
                    elif args["--add"]:
                        for crypto_code in to_be_imported:
                            crypto_line = to_be_imported[crypto_code]
                            add_user_crypto_by_code(
                                session,
                                crypto_code,
                                crypto_line["quantity"],
                                crypto_line["price"],
                                args["--add"],
                            )
                else:  # stocks import
                    if args["--new"]:
                        add_imported_securities_to_account(
                            session, args["--new"], to_be_imported
                        )
                    elif args["--edit"]:
                        add_imported_securities_to_account(
                            session, args["--edit"], to_be_imported, edit=True
                        )
                    elif args["--add"]:
                        add_imported_securities_to_account(
                            session, args["--add"], to_be_imported
                        )
    if result:
        print(json.dumps(result, indent=4))

    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
