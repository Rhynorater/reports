Hello! I've discovered an XSS vulnerability in the following endpoint: `$0`. Bounty Plz. 

My IP address is: {$ curl ipinfo.io/ip }

You can see that it is injected on line $1 of the vulnerable page: `{$ curl -s $0 | head -n $1 | tail -n 1 }`

