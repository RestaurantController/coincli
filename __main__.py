import argparse
import json
import requests
def main():
    parser = argparse.ArgumentParser(description="Checks Cryptocurrency Stats");
    parser.add_argument('-c', '--coin', type=str, required=False, help="Cryptocurrency Name");
    parser.add_argument('-cur', '--currency', type=str, required=False, help="Currency to convert(Default: USD)");
    parser.add_argument("-o", "--output", type=str, required=False, help="Output filename(JSON)");
    group = parser.add_argument_group();
    group.add_argument("-s", "--stats", action="store_true", help="View coin stats");
    group.add_argument("-st", "--apiStatus", action="store_true", help="Check API Status");
    group.add_argument("-q", "--quiet", action="store_true", help="Quiet mode(Disables output, Only works for --stats)");
    args = parser.parse_args();
    if(args.stats):
        if(args.coin):
            if(not args.quiet):
                print("Retrieving data, please wait....");
            currency = "USD";
            if(args.currency):
                currency = args.currency;
            r = requests.get("https://bitpay.com/api/rates/" + args.coin + "/" + currency);
            if(not r.ok):
             print("Request failed. Check the currency and the cryptocurrency name");
             exit();
            data = r.json();
            currencyname = data["name"];
            if(not args.quiet):
             print("Converting " + args.coin + " to " + currencyname);
             print("1 " + args.coin + " = " + str(data["rate"]) + " " + data["code"]);
            if(args.output):
             data["coin"] = args.coin;
             open(args.output, "w").write(json.dumps(data));
            exit();
        else:
          if(not args.quiet):
             print("Viewing 3 trend cryptocurrencies");
          currency = "USD";
          if(args.currency):
             currency = args.currency;
          trendcoins = ["BTC", "ETH", "XRP"];
          for coin in trendcoins:
             r = requests.get("https://bitpay.com/api/rates/" + coin + "/" + currency);
             if(not r.ok):
                 print("There was an error calling the API");
                 exit();
             data = r.json();
             if(not args.quiet):
                 print("1 " + coin + " = " + str(data["rate"]) + " " + data["code"]);
          if(args.output):
             if(not args.quiet):
                 print("NOTE: Output isn't supported without a specific currency!");
          exit();
    elif(args.apiStatus):
     print("Checking API status(BitPay.com)");
     r = requests.get("https://bitpay.com/api/rates");
     if(r.ok):
         print("API Status: Operational");
     else:
         print("API Status: API Down!");
    else:
     print("No command specified or command not found. Try typing -h for help.");
     exit();
if(__name__ == "main"):
    main();