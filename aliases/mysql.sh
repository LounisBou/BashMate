# Aliases for MySQL
# Created by LounisBou

# ----------------------------------
# ! IMPORTANT
# 
# Some of the folowing commands may need mycli package to be installed.
# To install it, run the following command on Mac OS:
# $ brew install mycli
# For more information, visit: https://www.mycli.net/
# ----------------------------------

# GLOBAL VARIABLES

# COMMANDS

# Connect to MySQL
alias mysql-connect="mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -P $MYSQL_PORT $MYSQL_DATABASE $*"
# Connect to MySQL using mycli
alias mycli-connect="mycli -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -P $MYSQL_PORT $MYSQL_DATABASE $*"

# Execute a query
function mysql-query() {
    echo "mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -P $MYSQL_PORT $MYSQL_DATABASE -e \"$*;\""
    mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -P $MYSQL_PORT $MYSQL_DATABASE -e "$*;"
}
# Execute a query using mycli
function mycli-query() {
    echo "mycli -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -P $MYSQL_PORT $MYSQL_DATABASE -e \"$*;\""
    mycli -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -P $MYSQL_PORT $MYSQL_DATABASE -e "$*;"
}

# Show all databases
alias mysql-show-databases="mysql-query 'SHOW DATABASES;'"
# Show all databases using mycli
alias mycli-show-databases="mycli-query 'SHOW DATABASES;'"

# Show all tables
alias mysql-show-tables="mysql-query 'SHOW TABLES;'"
# Show all tables using mycli
alias mycli-show-tables="mycli-query 'SHOW TABLES;'"

# Show all columns of a table
function mysql-show-columns() {
    mysql-query "SHOW COLUMNS FROM $1;"
}
# Show all columns of a table using mycli
function mycli-show-columns() {
    mycli-query "SHOW COLUMNS FROM $1;"
}




