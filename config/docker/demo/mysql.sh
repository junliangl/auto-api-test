#!/bin/bash
set -e
echo `service mysql status`
service mysql start
echo `service mysql status`
mysql < demo.sql
echo `service mysql status`
mysql < privileges.sql
echo `service mysql status`
tail -f /dev/null
