#!/bin/sh

DOCKER_PROJECT_PATH=/home/robothood-user/robothood/

mkdir -p logs
chmod 777 logs

mkdir -p database
chmod 777 database

usage()
{
    echo "usage: ./run.sh [[--help | -h] | [--leftovers | -l]]"
}

SCRIPT_TO_RUN=robothood/main.py

while [ "$1" != "" ]; do
    case $1 in
        -l | --leftovers )          SCRIPT_TO_RUN=robothood/leftovers.py
                                ;;
        -h | --help )           usage
                                exit
                                ;;
    esac
    shift
done

docker run -v $ROBOTHOOD_PATH:$DOCKER_PROJECT_PATH -e BAPI_KEY="$BAPI_KEY" \
-e BAPI_SECRET="$BAPI_SECRET" -e ROBOTHOOD_PATH="$DOCKER_PROJECT_PATH" \
-e DISCORD_TOKEN="$DISCORD_TOKEN" --rm robothood $SCRIPT_TO_RUN
