
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
* Add better currency support in checking/saving accounts. See TODO there
* Tests :)
* More typing hints
* CSV export. Use pandas ?
* Use logging everywhere. Output only the last result for further processing with jq or others
* Loans, Real estates are entirely TODO
* Timeseries, Insights, and Finary+ features are entirely TODO
* Precious metal update
* Interactive command line (it would make automation less fun, but manual use easier)

### Remarks for finary devs
* Delete responses should be normalize, sometimes we get json back sometimes nothing but the 204 HTTP code.

