Finary Unofficial API wrapper

A simple command line tool to interact with your Finary account.

Finary is a real time portfolio & stocks tracker. It supports precious metal, cryptos, stocks and a lot more.
If you don't already have an account, here is a referral link to sign up: https://finary.com/referral/7a49bf74c6d9cb3fca2a

:warning: Use at your own risk. I'm not responsible if you trash your account. :warning:

## Project goals

* Provide a command line tool to do a large part of what you can do on Finary website
* Automate some requested features not yet implemented by finary like CSV import/export

## Quick start 

1. Install requirements. `pip install finary_uapi`.
2. Copy paste the `credentials.json.tpl` file to `credentials.json` and file your username and password.
3. Run `python -m finary_uapi signin`
4. You are good to go and can explore the API. Run `python -m finary_uapi` for available commands.
5. Try `python -m finary_uapi me` or `python -m finary_uapi investments`. 
6. If you get errors about being unauthorized, you need to signin again.

## Usage

Run ``python -m finary_uapi` for an up to date version.

```
Usage:
    finary_uapi signin [MFA_CODE]
    finary_uapi me
    finary_uapi institution_connections
    finary_uapi organizations
    finary_uapi timeseries <period> <type>
    finary_uapi checking_accounts transactions [--page=<page>] [--perpage=<perpage>] [--account=<account_ids>] [--institution=<institution_ids>] [--query=<query>]
    finary_uapi fonds_euro
    finary_uapi startups
    finary_uapi investments
    finary_uapi investments dividends
    finary_uapi investments transactions [--page=<page>] [--perpage=<perpage>] [--account=<account_ids>] [--institution=<institution_ids>] [--query=<query>]
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
    finary_uapi credit_accounts transactions [--page=<page>] [--perpage=<perpage>] [--account=<account_ids>] [--institution=<institution_ids>] [--query=<query>]
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
```

## Examples

* List crypto accounts, and display id and name
```
python -m finary_uapi holdings_accounts crypto | jq '.result[] | {id: .id, name: .name}'
```

* List investment accounts, and display id and name
```
python -m finary_uapi holdings_accounts stocks | jq '.result[] | {id: .id, name: .name}'
```

* Import a CSV file from crypto.com in a new crypto account on Finary. Replace the filename and the account name
```
python -m finary_uapi import cryptocom crypto_transactions_record.csv --new Crypto.com
```

* Import a generic CSV file (see tests directory for a sample) in a new crypto account on Finary. 
Replace the filename and the account name.
```
python -m finary_uapi import crypto_csv cryptodump.csv --new MyLovelyExchange
```

* Create a "Compte d'épargne' with a 1000€ balance at BNP Paribas
```
python -m finary_uapi holdings_accounts add checking testchecking "BNP Paribas" "Compte d'épargne" 1000
```

* Print gross wealth
```
python -m finary_uapi dashboard gross all | jq '.result["total"]["amount"]'
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



## Contributors ✨

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

Thanks go to these people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="16.66%"><a href="http://lasconic.com"><img src="https://avatars.githubusercontent.com/u/234271?v=4?s=100" width="100px;" alt="Nicolas Froment"/><br /><sub><b>Nicolas Froment</b></sub></a><br /><a href="#projectManagement-lasconic" title="Project Management">📆</a> <a href="#promotion-lasconic" title="Promotion">📣</a> <a href="https://github.com/lasconic/finary_uapi/commits?author=lasconic" title="Code">💻</a> <a href="https://github.com/lasconic/finary_uapi/issues?q=author%3Alasconic" title="Bug reports">🐛</a> <a href="#ideas-lasconic" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/lasconic/finary_uapi/commits?author=lasconic" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="16.66%"><a href="http://varal7.fr"><img src="https://avatars.githubusercontent.com/u/8019486?v=4?s=100" width="100px;" alt="Victor Quach"/><br /><sub><b>Victor Quach</b></sub></a><br /><a href="https://github.com/lasconic/finary_uapi/commits?author=Varal7" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/nmathey"><img src="https://avatars.githubusercontent.com/u/20896232?v=4?s=100" width="100px;" alt="NickFR"/><br /><sub><b>NickFR</b></sub></a><br /><a href="https://github.com/lasconic/finary_uapi/commits?author=nmathey" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/clemlesne"><img src="https://avatars.githubusercontent.com/u/10001945?v=4?s=100" width="100px;" alt="Clémence Lesné"/><br /><sub><b>Clémence Lesné</b></sub></a><br /><a href="https://github.com/lasconic/finary_uapi/commits?author=clemlesne" title="Code">💻</a></td>
      <td align="center" valign="top" width="16.66%"><a href="https://github.com/OxyFlax"><img src="https://avatars.githubusercontent.com/u/14943003?v=4?s=100" width="100px;" alt="OxyFlax"/><br /><sub><b>OxyFlax</b></sub></a><br /><a href="https://github.com/lasconic/finary_uapi/commits?author=OxyFlax" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->


This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
