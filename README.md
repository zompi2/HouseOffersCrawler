# House Buy Crawler

This is my little tool for crawling through pages with houses to buy.

It will filter all offers to get the one I'm interested with. It will search only for the newest offerst (not the one I've already seen) and removed offers that contains any keyword described in blacklist.

Currently it supports crawling through OLX and Otodom services, but maybe will be extended in the future.

It supports only those filters I needed. This is a script for my purposes only, but you can use this code however you want.

It is controller by config.json file, where specific filters can be modified.

It can send results to a mail, but it requires running smtp server, like postfix.
