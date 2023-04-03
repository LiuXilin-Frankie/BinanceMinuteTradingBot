# Cryptocurrency trading signals

## Disclaimer
This software is not for real-world use, it is intended for educational use.
The trading strategy it uses to send signals, is not effective alone, real world trading requires deep understanding of multiple market indicators!
THE AUTHOR AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.

If you want to get into trading, DO NOT risk money which you are afraid to lose and ALWAYS do your own research.

## Supported Exchange marketplaces

- [X] [Binance](https://www.binance.com/)

## Features

- [x] **Based on Python 3.8**
- [x] **It's using Bollinger Bands as a trading strategy**
- [x] **It will log "BUY" messages into the terminal when BTC price is at the lower bollinger band & "SELL" messages when BTC price is at the upper bollinger bands, otherwise it will print "WAIT"**

## Quick start
***
** NOTE ** : **This section assumes docker & python3.8+ is already installed**

* Clone the repository into a folder using command:
```<Language>

git clone https://github.com/ungureanudaniel/crypto-signals.git

```
* cd into the crypto-signals directory
* Build the docker image & run it, using command:
```<Language>

docker build -t crypto-signals . && docker run crypto-signals

```

---

## Technologies & Libraries
***
A list of technologies used within the project:
* [python](https://www.python.org/downloads/release/python-380/): Version 3.8
* [docker](https://docs.docker.com/): Version 20.10.16
* [python-binance](https://python-binance.readthedocs.io/en/latest/): Version 1.0.16
* [numpy](https://numpy.org/): Version 1.22
* [pandas](https://pandas.pydata.org/): Version 1.4.2
* [pandas-datareader](https://pandas-datareader.readthedocs.io/en/latest/): Version 0.10
* [matplotlib](https://matplotlib.org/): Version 1.0.16
* [loguru](https://loguru.readthedocs.io/en/stable/): Version 0.6
* [pytest](https://docs.pytest.org/en/6.2.x/assert.html): Version 7.1.2
