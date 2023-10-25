#!/bin/bash
FROM amd64/mysql:5.7.32

ENV MYSQL_ALLOW_EMPTY_PASSWORD yes

COPY config/docker/demo/mysql.sh setup.sh
COPY config/docker/my.cnf /etc/mysql/conf.d/my.cnf

COPY config/db/ddl/demo.sql demo.sql

COPY config/db/ddl/privileges.sql privileges.sql

EXPOSE 3306

CMD ["bash", "setup.sh"]