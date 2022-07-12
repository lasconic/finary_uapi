
A simple command line tool to interact with your Finary account.

Finary is a real time portfolio & stocks tracker. It supports precious metal, cryptos, stocks and a lot more.
If you don't already have an account, here is a referral link to sign up: https://finary.com/referral/7a49bf74c6d9cb3fca2a

:warning: Use at your own risk. I'm not responsible if you trash your account. :warning:

## Project goals

* Provide a command line tool to do a large part of what you can do on Finary website
* Automate some requested features not yet implemented by finary like CSV import/export

## Quick start 

1. Install requirements. `pip install -r requirements.txt`.
2. Copy paste the `credentials.json.tpl` file to `credentials.json` and file your username and password.
3. Run `python -m finary_api signin`
4. You are good to go and can explore the API. Run `python -m finary_api` for available commands.
5. Try `python -m finary_api me` or `python -m finary_api investments`. 
6. If you get errors about being unauthorized, you need to signin again.

## Usage

Run ``python -m finary_api` for an up to date version.

```
Usage:
    finary_api signin
    finary_api me
    finary_api institution_connections
    finary_api dashboard net [all | 1w | 1m | ytd | 1y]
    finary_api dashboard gross [all | 1w | 1m | ytd | 1y]
    finary_api dashboard finary [all | 1w | 1m | ytd | 1y]
    finary_api portfolio [all | 1w | 1m | ytd | 1y]
    finary_api commodities [all | 1w | 1m | ytd | 1y]
    finary_api checking_accounts [all | 1w | 1m | ytd | 1y]
    finary_api fonds_euro [all | 1w | 1m | ytd | 1y]
    finary_api other_assets [all | 1w | 1m | ytd | 1y]
    finary_api saving_accounts [all | 1w | 1m | ytd | 1y]
    finary_api real_estates [all | 1w | 1m | ytd | 1y]
    finary_api startups
    finary_api investments
    finary_api cryptos
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
    finary_api crypto_currency search QUERY
    finary_api fiat_currency search QUERY
    finary_api institutions search QUERY
    finary_api securities search QUERY
    finary_api securities
    finary_api securities add <code> <quantity> <price> <account_id>
    finary_api securities delete <security_id>
    finary_api import cryptocom FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_api import crypto_csv FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_api import stocks_csv FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
    finary_api import stocks_json FILENAME [(--new=NAME | --edit=account_id | --add=account_id)]
```

## Examples

* List crypto accounts, and display id and name
```
python -m finary_api holdings_accounts crypto | jq '.result[] | {id: .id, name: .name}'
```

* List investment accounts, and display id and name
```
python -m finary_api holdings_accounts stocks | jq '.result[] | {id: .id, name: .name}'
```

* Import a CSV file from crypto.com in a new crypto account on Finary. Replace the filename and the account name
```
python -m finary_api import cryptocom crypto_transactions_record.csv --new Crypto.com
```

* Import a generic CSV file (see tests directory for a sample) in a new crypto account on Finary. 
Replace the filename and the account name.
```
python -m finary_api import crypto_csv cryptodump.csv --new MyLovelyExchange
```

* Create a "Compte d'épargne' with a 1000€ balance at BNP Paribas
```
python -m finary_api holdings_accounts add checking testchecking "BNP Paribas" "Compte d'épargne" 1000
```

* Print gross wealth
```
python -m finary_api dashboard gross all | jq '.result["total"]["amount"]'
```


## TODO
* See [Issues](https://github.com/lasconic/finary/issues)
* Tests :smile:
* More typing hints
* CSV export. Use pandas ?
* Write, update, delete for Loans, Real estates, SCPIs are entirely TODO
* Precious metal update
* Interactive command line (it would make automation less fun, but manual use easier)

### Remarks for finary devs
* Delete responses should be normalized, sometimes we get json back sometimes nothing but the 204 HTTP code.

