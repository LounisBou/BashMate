# Aliases for Symfony framework
# Created by LounisBou

# GLOBAL VARIABLES

# COMMANDS

# Symfony console shortcut command
alias sf="php bin/console $*"
# Symfony entity
alias sf-entity-create="php bin/console make:entity"
alias sf-entity-update="php bin/console make:entity --regenerate"
# Symfony controller
alias sf-controller-create="php bin/console make:controller"
# Symfony form
alias sf-form-create="php bin/console make:form"
# Symfony CRUD
alias sf-crud-create="php bin/console make:crud"
# Symfony service
alias sf-service-create="php bin/console make:service"
# Symfony repository
alias sf-repository-create="php bin/console make:repository"
# Symfony router
alias sf-router-debug="php bin/console debug:router"
# Symfony cache
alias sf-cache-clear="php bin/console cache:clear"
alias sf-cache-warmup="php bin/console cache:warmup"
alias sf-cache-pool-clear="php bin/console cache:pool:clear"
# Pest PHP test
alias sf-test="vendor/bin/pest"
alias sf-test-coverage="vendor/bin/pest --coverage --min=100"
function sf-test-coverage-html(){
    # Get current directory name
    current_directory=${PWD##*/}
    # Create directory for coverage report recursively if not exists
    mkdir -p /tmp/tests-coverage/$current_directory
    # Run test with coverage and html report
    vendor/bin/pest --coverage-html /tmp/tests-coverage/$current_directory
}
function sf-test-open-report(){
    # Get current directory name
    current_directory=${PWD##*/}
    # Open coverage report in browser
    open-chrome /tmp/tests-coverage/$current_directory/index.html
}
# PHP Code Sniffer 
alias sf-phpcs-check="vendor/bin/php-cs-fixer fix --allow-risky=yes --dry-run --diff"
alias sf-phpcs-run="vendor/bin/php-cs-fixer fix --allow-risky=yes"
function sf-phpcs-fix(){
    # PHP Code Sniffer fix
    vendor/bin/php-cs-fixer fix --allow-risky=yes
    # PHP CBF run
    vendor/bin/phpcbf --warning-severity=0
}
# PHP Stan
alias sf-phpstan-analyse="vendor/bin/phpstan"
# Doctrine database
alias sf-database-create="php bin/console doctrine:database:create"
alias sf-database-drop="php bin/console doctrine:database:drop"
alias sf-database-update="php bin/console doctrine:schema:update --force"
alias sf-database-validate="php bin/console doctrine:schema:validate"
# Doctrine migrations
alias sf-migration-diff="php bin/console doctrine:migrations:diff"
alias sf-migration-migrate="php bin/console doctrine:migrations:migrate"
alias sf-migration-status="php bin/console doctrine:migrations:status"
alias sf-migration-version="php bin/console doctrine:migrations:version"
# - Rollback migrations with number of migrations to rollback as parameter (default 1)
function sf-migration-rollback(){
    # Check number of migrations to rollback is provided
    if [ -z "$1" ]; then
        # Default value
        nb_migrations_to_rollback=1
    fi
    # Loop to rollback migrations
    for (( i=1; i<=$nb_migrations_to_rollback; i++ ))
    do
        # Rollback migration
        php bin/console doctrine:migrations:migrate prev --no-interaction
    done
}
# - Create migration files and execute them
function sf-migrate(){
    # Check migration status
    php bin/console doctrine:migrations:status
    # Ask for confirmation
    read REPLY"?Do you want to continue ? (y/n) "
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Create migration files
        php bin/console doctrine:migrations:diff
        # Execute migration on database
        php bin/console doctrine:migrations:migrate
        # Message migration done
        echo -e "${GREEN}Migration done${NC}"
    else
        echo -e "${RED}Migration cancelled${NC}"
    fi
    # Show migration status
    php bin/console doctrine:migrations:status
}
# - Execute migration with version as parameter
function sf-migration-exec() {
    php bin/console doctrine:migrations:execute $1 --up
}
# - Rollback migration with version as parameter
function sf-migration-exec-down() {
    php bin/console doctrine:migrations:execute $1 --down
}
# Symfony translation 
# - Translation update (Parameter: locale, default: en)
function sf-translation-update(){
    # Check locale is provided
    if [ -z "$1" ]; then
        # Default value
        locale="en"
    else
        # Set locale
        locale=$1
    fi
    # Update translation
    php bin/console translation:update $locale --force
}
