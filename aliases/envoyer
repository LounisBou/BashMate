# Aliases definitions.
# Created by LounisBou
#

# GLOBAL VARIABLES

# COMMANDS

# List all projects from Envoyer API
function envoyer-projects(){
    # Create api url for projects
    api_url="$ENVOYER_API_URL/projects"

    # Get projects data
    response=$(curl -s -X GET "$api_url" -H "Authorization: Bearer $ENVOYER_API_TOKEN")

    # Print response parse with jq
    #echo -E "$response" | jq

    # Foreach project in response display project infos
    for row in $(echo -E "$response" | jq -r '.projects[] | @base64'); do
        # Decode project row
        _jq() {
            echo -E "${row}" | base64 --decode | jq -r ${1}
        }
        # Get project infos from response using jq
        project_id=$(_jq '.id')
        project_name=$(_jq '.name')
        project_branch=$(_jq '.branch')
        ip_address=$(_jq '.ip_address')
        port=$(_jq '.port')
        php_version=$(_jq '.php_version')

        
        # Display the extracted values
        echo "Project ID: $project_id"
        echo "Project Name: $project_name"
        echo "Project Branch: $project_branch"
        echo "IP Address: $ip_address"
        echo "Port: $port"
        echo "PHP Version: $php_version"
        echo "----------------------------------------"
    done
}
#
# .\" Manpage for envoyer-project.
# .TH man 8 "06 May 2010" "1.0" "envoyer-project man page"
# .SH NAME
# envoyer-project \- display project infos from Envoyer API
# .SH SYNOPSIS
# envoyer-project [PROJECT_ID]
# .SH DESCRIPTION
# The envoyer-project displays project infos from Envoyer API.
# .SH OPTIONS
# envoyer-project accepts the following options:
# PROJECT_ID
#     The project id from Envoyer API.
# .SH BUGS
# No known bugs.
# .SH AUTHOR
# LounisBou (lounis.bou@gmail.com)
# "
#
function envoyer-project(){
    # Create api url for projects
    api_url="$ENVOYER_API_URL/projects/$1"

    # Get project data
    response=$(curl -s -X GET "$api_url" -H "Authorization: Bearer $ENVOYER_API_TOKEN")

    # Print response parse with jq
    #echo -E "$response" | jq

    # Get project infos from response using jq
    project_name=$(echo -E "$response" | jq -r '.project.name')
    project_branch=$(echo -E "$response" | jq -r '.project.branch')
    last_deployment_status=$(echo -E "$response" | jq -r '.project.last_deployment_status')
    last_deployment_took=$(echo -E "$response" | jq -r '.project.last_deployment_took')
    deployment_date=$(echo -E "$response" | jq -r '.project.deployment_finished_at')
    last_deployed_branch=$(echo -E "$response" | jq -r '.project.last_deployed_branch')
    last_deployment_author=$(echo -E "$response" | jq -r '.project.last_deployment_author')
    last_deployment_branch=$(echo -E "$response" | jq -r '.project.last_deployment_branch')
    last_deployment_timestamp=$(echo -E "$response" | jq -r '.project.last_deployment_timestamp')
    daily_deploys=$(echo -E "$response" | jq -r '.project.daily_deploys')

    # Format deployment_at date to d/m/Y H:i:s format
    deployment_date=$(echo "$deployment_date" | awk -F "T|Z" '{split($1,date,"-"); split($2,time,":"); printf "%s/%s/%s %s:%s:%s", date[3], date[2], date[1], time[1], time[2], time[3]}')
    
    echo "-------------------------------------------------"
    echo "Project: $project_name"
    echo "-------------------------------------------------"

    # Display the extracted values
    echo "Project Name: $project_name"
    echo "Project Branch: $project_branch"
    echo "Deployment Status: $last_deployment_status"
    echo "Deployment Took: $last_deployment_took seconds"
    echo "Deployment Date: $deployment_date"
    echo "Deployed Branch: $last_deployed_branch"
    echo "Deployment Author: $last_deployment_author"
    echo "Deployment Branch: $last_deployment_branch"
    echo "Deployment Timestamp: $last_deployment_timestamp"
    echo "Daily Deploys: $daily_deploys"

    # Create api url for deployments
    api_url2="$ENVOYER_API_URL/projects/$1/deployments"

    # Get deployments data
    response2=$(curl -s -X GET "$api_url2" -H "Authorization: Bearer $ENVOYER_API_TOKEN")

    # Print response parse with jq
    #echo -E "$response2" | jq

    # Separator
    echo "-------------------------------------------------"
    echo "Deployments:"
    echo "-------------------------------------------------"

    # Foreach deployment in response display deployment infos
    for row in $(echo -E "$response2" | jq -r '.deployments[] | @base64'); do
        # Decode deployment row
        _jq() {
            echo -E "${row}" | base64 --decode | jq -r ${1}
        }
        # Get deployment infos from response using jq
        deployment_id=$(_jq '.id')
        commit_branch=$(_jq '.commit_branch')
        commit_author=$(_jq '.commit_author')
        commit_status=$(_jq '.status')
        created_at=$(_jq '.created_at')

        # Find GMT offset
        export TZ=":Europe/Paris"
        # Store GMT offset in variable
        gmt_offset=$(date +%z)
        # Convert GMT offset to int : Extract the numeric value from the GMT offset string
        numeric_offset="${gmt_offset:1:2}"
        # Convert the numeric offset to an integer
        offset_hours=$((10#$numeric_offset))

        # Format deployment_at date to d/m/Y H:i:s format
        created_date=$(echo "$created_at" | awk -F "T|Z" '{split($1,date,"-"); split($2,time,":"); printf "%s/%s/%s %s:%s:%s", date[3], date[2], date[1], time[1]+'$offset_hours', time[2], time[3]}')

        # Display the extracted values
        echo "Deployment ID: $deployment_id"
        echo "Commit Branch: $commit_branch"
        echo "Commit Author: $commit_author"
        echo "Status: $commit_status"
        echo "Created At: $created_date"
        echo "-------------------------------------------------"
    done
}
