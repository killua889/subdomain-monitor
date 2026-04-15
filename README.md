#  Subdomain Monitor with Telegram Alerts

Automated subdomain monitoring script for bug bounty hunters.

##  Features

* Detect new subdomains using `subfinder`
* Compare results using `anew`
* Save new subdomains in timestamped files
* Telegram alerts via `notify`
* Runs continuously with customizable intervals

##  Requirements

* Python 3
* subfinder
* anew
* notify (projectdiscovery)

##  Installation

```bash
git clone https://github.com/YOUR_USERNAME/subdomain-monitor.git
cd subdomain-monitor
```

Install tools:

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/tomnomnom/anew@latest
go install -v github.com/projectdiscovery/notify/cmd/notify@latest
```

##  Usage

```bash
python monitor.py -l domains.txt -f output -n TELEGRAM_ID
```
## Notes

* Ensure `notify` is configured with your Telegram provider
* The script compares results against your domain list using `anew`

## Arguments

| Flag                 | Description                                         |
| -------------------- | --------------------------------------------------- |
| `-l`, `--domainlist` | File containing target domains                      |
| `-f`, `--folderpath` | Output directory                                    |
| `-n`, `--notifyid`   | Notify (Telegram) provider ID                       |
| `-s`, `--sleep`      | Time between runs (seconds) *(default: 28800 = 8h)* |

##  Output

```
output/
   └── new-subs/
         ├── new-subs-2026-04-15_10-00-00.txt
```

##  Use Case

Perfect for:

* Bug bounty recon automation
* Continuous monitoring of targets
* Detecting newly exposed assets

---

##  Disclaimer

Use this tool only on authorized targets.
