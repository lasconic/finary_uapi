"""
Finary command line
Usage:
    finary_uapi signin [MFA_CODE]
    finary_uapi me
    finary_uapi institution_connections
    finary_uapi organizations
    finary_uapi timeseries <period> <type>
    finary_uapi checking_accounts transactions
    finary_uapi fonds_euro
    finary_uapi startups
    finary_uapi investments
    finary_uapi investments dividends
    finary_uapi investments transactions
    finary_uapi crowdlendings
    finary_uapi crowdlendings distribution
    finary_uapi crowdlendings add <account_name> <name> <annual_yield> <month_duration> <initial_investment> <current_price> <currency_code> <start_date>
    finary_uapi crowdlendings delete <crowdlending_id>
    finary_uapi cryptos
    finary_uapi cryptos distribution
    finary_uapi cryptos add <code> <quantity> <price> <account_id>
    finary_uapi cryptos update <code> <quantity> <price> <account_id>
    finary_uapi cryptos delete <code> <account_id>
    finary_uapi precious_metals search QUERY
    finary_uapi precious_metals
    finary_uapi precious_metals add <name> <quantity> <price>
    finary_uapi precious_metals delete <commodity_id>
    finary_uapi holdings_accounts [crypto | stocks | crowdlending | <account_name>]
    finary_uapi holdings_accounts add (crypto | stocks | crowdlending) <account_name>
    finary_uapi holdings_accounts add (checking | saving) <account_name> <bank_name> <account_type> <balance>
    finary_uapi holdings_accounts delete <account_id>
    finary_uapi holdings_accounts update <account_id> <account_name> [<account_balance>]
    finary_uapi generic_asset_categories
    finary_uapi generic_assets
    finary_uapi generic_assets add <name> <category> <quantity> <buying_price> <current_price>
    finary_uapi generic_assets update <asset_id> <name> <category> <quantity> <buying_price> <current_price>
    finary_uapi generic_assets delete <asset_id>
    finary_uapi crypto_chains
    finary_uapi crypto_currency search QUERY
    finary_uapi fiat_currency search QUERY
    finary_uapi institutions search QUERY
    finary_uapi securities search QUERY
    finary_uapi securities
    finary_uapi securities add <code> <quantity> <price> <account_id>
    finary_uapi securities delete <security_id>
    finary_uapi insights
    finary_uapi loans
    finary_uapi credit_accounts transactions
    finary_uapi real_estates
    finary_uapi real_estates add rent <address> <user_estimated_value> <description> <surface> <buying_price> <building_type> <ownership_percentage> <monthly_charges> <monthly_rent> <yearly_taxes> <rental_period> <rental_type> [<currency_code>]
    finary_uapi real_estates add <category> <address> <user_estimated_value> <description> <surface> <buying_price> <building_type> <ownership_percentage> [<currency_code>]
    finary_uapi real_estates update rent <asset_id> <user_estimated_value> <description> <buying_price> <ownership_percentage> <monthly_rent>
    finary_uapi real_estates update <category> <asset_id> <user_estimated_value> <description> <buying_price> <ownership_percentage>
    finary_uapi real_estates delete <asset_id>
    finary_uapi scpis search QUERY
    finary_uapi scpis
    finary_uapi watches search QUERY
    finary_uapi import crowdlending_csv FILENAME [-d] [-f]
    finary_uapi import cryptocom FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_uapi import nexo FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_uapi import crypto_csv FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_uapi import stocks_csv FILENAME [(--new=NAME | --edit=account_id | --add=account_id)] [-d]
    finary_uapi import stocks_json FILENAME [(--new=NAME | --edit=account_id | --add=account_id)] [-d]


Options:
  --new=NAME          Create a new account and import the lines
  --edit=account_id   Edit the line with new value if it exists, create it otherwise
  --add=account_id    If line exists, add the quantity and change the price accordingly, create it otherwise
"""  # noqa

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
from .importers.crowdlending_generic_csv import import_crowdlending_generic_csv
from .importers.cryptocom import import_cc_csv
from .importers.nexo import import_nexo_csv
from .importers.crypto_generic_csv import import_crypto_generic_csv
from .importers.stocks_generic_csv import import_stocks_generic_csv
from .institutions import get_institutions
from .user_portfolio import (
    get_portfolio_investments,
    get_portfolio_investments_dividends,
    get_portfolio_checking_accounts_transactions,
    get_portfolio_investments_transactions,
    get_portfolio_crowdlendings,
    get_portfolio_crowdlendings_distribution,
    get_portfolio_cryptos_distribution,
    get_portfolio_credit_accounts_transactions,
    get_portfolio_timeseries,
)
from .precious_metals import get_precious_metals
from .user_generic_assets import (
    add_user_generic_asset,
    delete_user_generic_asset,
    get_user_generic_assets,
    update_user_generic_asset,
)
from .user_real_estates import (
    get_user_real_estates,
    add_user_real_estates_with_currency,
    update_user_real_estates,
    delete_user_real_estates,
)
from .user_scpis import get_user_scpis
from .scpis import get_scpis
from .securities import get_securities
from .signin import signin
from .user_startups import get_user_startups
from .user_crowdlendings import (
    add_user_crowdlending_to_account,
    delete_user_crowdlending,
    add_imported_user_crowdlendings,
)
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
from .views import get_insights, get_loans
from .watches import get_watches


def main() -> int:  # pragma: nocover
    """Main entry point."""
    import logging

    logging.basicConfig(level=logging.INFO)

    args = docopt(__doc__)
    result = ""
    if args["signin"]:
        result = signin(args["MFA_CODE"])
    else:
        session = prepare_session()
        if args["me"]:
            result = get_user_me(session)
        elif args["institution_connections"]:
            result = get_user_me_institution_connections(session)
        elif args["checking_accounts"]:
            if args["transactions"]:
                result = get_portfolio_checking_accounts_transactions(session)
        elif args["fonds_euro"]:
            result = get_user_fonds_euro(session)
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
            elif args["watches"]:
                result = get_watches(session, args["QUERY"])
            else:
                print("Unknown resource for search")
                return 1
        elif args["add"]:
            if args["crowdlendings"]:
                result = add_user_crowdlending_to_account(
                    session,
                    args["<account_name>"],
                    args["<annual_yield>"],
                    args["<currency_code>"],
                    args["<current_price>"],
                    args["<initial_investment>"],
                    args["<month_duration>"],
                    args["<name>"],
                    args["<start_date>"],
                )
            elif args["cryptos"]:
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
            elif args["real_estates"]:
                result = add_user_real_estates_with_currency(
                    session,
                    "rent" if args["rent"] else args["<category>"],
                    args["<address>"],
                    args["<currency_code>"],
                    args["<user_estimated_value>"],
                    args["<description>"],
                    args["<surface>"],
                    args["<buying_price>"],
                    args["<building_type>"],
                    args["<ownership_percentage>"],
                    args["<monthly_charges>"],
                    args["<monthly_rent>"],
                    args["<yearly_taxes>"],
                    args["<rental_period>"],
                    args["<rental_type>"],
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
            elif args["real_estates"]:
                result = update_user_real_estates(
                    session,
                    "rent" if args["rent"] else args["<category>"],
                    args["<asset_id>"],
                    args["<user_estimated_value>"],
                    args["<description>"],
                    args["<buying_price>"],
                    args["<ownership_percentage>"],
                    args["<monthly_rent>"],
                )
            elif args["holdings_accounts"]:
                result = update_holdings_account(
                    session,
                    args["<account_id>"],
                    args["<account_name>"],
                    args["<account_balance>"],
                )
        elif args["delete"]:
            if args["crowdlendings"]:
                result = delete_user_crowdlending(session, args["<crowdlending_id>"])
            elif args["cryptos"]:
                result = delete_user_crypto_by_code(
                    session,
                    args["<code>"],
                    args["<account_id>"],
                )
            elif args["generic_assets"]:
                delete_user_generic_asset(session, args["<asset_id>"])
            elif args["real_estates"]:
                delete_user_real_estates(session, args["<asset_id>"])
            elif args["holdings_accounts"]:
                result = delete_holdings_account(session, args["<account_id>"])
            elif args["precious_metals"]:
                delete_user_precious_metals(session, args["<commodity_id>"])
            elif args["securities"]:
                delete_user_security(session, args["<security_id>"])
        elif args["crowdlendings"]:
            if args["distribution"]:
                result = get_portfolio_crowdlendings_distribution(session)
            else:
                result = get_portfolio_crowdlendings(session)
        elif args["crypto_chains"]:
            result = get_crypto_chains(session)
        elif args["cryptos"]:
            if args["distribution"]:
                result = get_portfolio_cryptos_distribution(session)
            else:
                result = get_user_cryptos(session)
        elif args["investments"]:
            if args["dividends"]:
                result = get_portfolio_investments_dividends(session)
            elif args["transactions"]:
                result = get_portfolio_investments_transactions(session)
            else:
                result = get_portfolio_investments(session)
        elif args["timeseries"]:
            result = get_portfolio_timeseries(session, args["<period>"], args["<type>"])
        elif args["holdings_accounts"]:
            if args["<account_name>"]:
                result = get_holdings_account_per_name_or_id(
                    session, args["<account_name>"]
                )
            else:
                holdings_account_types = ["crypto", "stocks", "crowdlending"]
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
        elif args["insights"]:
            result = get_insights(session)
        elif args["loans"]:
            result = get_loans(session)
        elif args["credit_accounts"]:
            if args["transactions"]:
                result = get_portfolio_credit_accounts_transactions(session)
        elif args["real_estates"]:
            result = get_user_real_estates(session)
        elif args["scpis"]:
            result = get_user_scpis(session)
        elif args["import"]:
            to_be_imported = []
            if args["crowdlending_csv"]:
                to_be_imported = import_crowdlending_generic_csv(args["FILENAME"])
            elif args["cryptocom"]:
                to_be_imported = import_cc_csv(args["FILENAME"])
            elif args["nexo"]:
                to_be_imported = import_nexo_csv(
                    args["FILENAME"] or "nexo_transactions.csv"
                )
            elif args["crypto_csv"]:
                to_be_imported = import_crypto_generic_csv(args["FILENAME"])
            elif args["stocks_csv"]:
                to_be_imported = import_stocks_generic_csv(args["FILENAME"])
            elif args["stocks_json"]:
                with open(args["FILENAME"], "r") as input_file:
                    to_be_imported = json.loads(input_file.read())

            if to_be_imported:
                if args["cryptocom"] or args["nexo"] or args["crypto_csv"]:
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
                elif args["stocks_csv"] or args["stocks_json"]:  # stocks import
                    if args["--new"]:
                        add_imported_securities_to_account(
                            session, args["--new"], to_be_imported, dry_run=args["-d"]
                        )
                    elif args["--edit"]:
                        add_imported_securities_to_account(
                            session,
                            args["--edit"],
                            to_be_imported,
                            edit=True,
                            dry_run=args["-d"],
                        )
                    elif args["--add"]:
                        add_imported_securities_to_account(
                            session, args["--add"], to_be_imported, dry_run=args["-d"]
                        )
                else:  # crowdlending
                    add_imported_user_crowdlendings(
                        session, to_be_imported, dry_run=args["-d"], clean=args["-f"]
                    )
    if result:
        print(json.dumps(result, indent=4))

    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
