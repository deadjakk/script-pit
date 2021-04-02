#!/bin/bash
# thnx 2 @ac3lives
echo 'script.sh <*.domain.com> <domain.com>'
openssl s_client -servername $1 -connect $2:443 | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
