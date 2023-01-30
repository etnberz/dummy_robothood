
ARG PROJECT_NAME=robothood
ARG PROJECT_SLUG=robothood

ARG UID_AND_GID=10001
ARG USERNAME=${PROJECT_NAME}-user
ARG GROUPNAME=${PROJECT_NAME}-group
ARG USER_HOME_PATH=/home/${USERNAME}
ARG USER_LOCAL_PATH=${USER_HOME_PATH}/.local
ARG CONFIG_FILE_NAME=log_config.json

ARG PROJECT_PATH=${USER_HOME_PATH}/${PROJECT_NAME}
ARG LOG_PATH=${PROJECT_PATH}/logs
ARG DB_PATH=${PROJECT_PATH}/database

# ===================================== Build Image ===============================================

# This Dockerfile skeleton comes from https://github.com/hexops/dockerfile
FROM python:3.8 as build-image

ARG VAR_PIP_INDEX_URL
ARG PROJECT_PATH
ARG UID_AND_GID
ARG GROUPNAME
ARG USERNAME
ARG USER_HOME_PATH
ARG USER_LOCAL_PATH

# Non-root user for security purposes.
#
# UIDs below 10,000 are a security risk, as a container breakout could result
# in the container being ran as a more privileged user on the host kernel with
# the same UID.
#
# Static GID/UID is also useful for chown'ing files outside the container where
# such a user does not exist.
RUN addgroup --gid=$UID_AND_GID $GROUPNAME
RUN useradd -d $USER_HOME_PATH -m --system --uid=$UID_AND_GID -g $GROUPNAME  $USERNAME

# Project folder creation
COPY ./ $PROJECT_PATH
RUN chown -R $USERNAME:$GROUPNAME $PROJECT_PATH

# Use the non-root user to run our application
USER $USERNAME


# Dependencies installation. The path manipulation is to silence path warnings with clis
ENV PATH=${USER_LOCAL_PATH}/bin:${PATH}
RUN if [ -z "${VAR_PIP_INDEX_URL}" ] ; \
      then >&2 echo "VAR_PIP_INDEX_URL was not provided as a build arg, using internal packages will fail." ; \
    fi
RUN if [ -z "${VAR_PIP_INDEX_URL}" ] ; \
      then pip install --user $PROJECT_PATH ; else pip install --user $PROJECT_PATH --index-url=${VAR_PIP_INDEX_URL} ; \
    fi

# ===================================== Run Image =================================================
FROM python:3.8 as run-image

ARG PROJECT_PATH
ARG UID_AND_GID
ARG GROUPNAME
ARG USERNAME
ARG USER_HOME_PATH
ARG USER_LOCAL_PATH
ARG CONFIG_FILE_NAME
ARG PROJECT_SLUG
ARG LOG_PATH
ARG DB_PATH

# Add eventual other apt-get packages you would need here
RUN apt-get update && \
    apt-get install tini && \
    apt-get clean autoclean && \
    apt-get autoremove --yes

RUN addgroup --gid=$UID_AND_GID $GROUPNAME
RUN useradd -d $USER_HOME_PATH -m --system --uid=$UID_AND_GID -g $GROUPNAME  $USERNAME


# Making sure its bin folder exists
RUN mkdir -p ${USER_LOCAL_PATH}/bin
RUN mkdir -p ${LOG_PATH}
RUN chown $USERNAME $LOG_PATH
RUN mkdir -p ${DB_PATH}
RUN chown $USERNAME $DB_PATH

COPY --from=build-image $USER_LOCAL_PATH $USER_LOCAL_PATH
COPY --from=build-image $PROJECT_PATH $PROJECT_PATH
WORKDIR $PROJECT_PATH
ENV PATH=${USER_LOCAL_PATH}/bin:${PATH}
ENV LOG_CONFIG_PATH=$PROJECT_PATH/$PROJECT_SLUG/config/$CONFIG_FILE_NAME

# Copy and prepare the entrypoint script
COPY entrypoint.sh ${USER_LOCAL_PATH}/bin
RUN chmod +x ${USER_LOCAL_PATH}/bin/entrypoint.sh

# setup the robothood folder
RUN chown $USERNAME $PROJECT_PATH

# Use the non-root user to run our application
USER $USERNAME

ENV PATH=${USER_LOCAL_PATH}/bin:${PATH}

# Tini allows us to avoid several Docker edge cases, see https://github.com/krallin/tini.
ENTRYPOINT ["entrypoint.sh"]
# Add the proper way to run your app in the entrypoint above

# Default arguments for your app (remove if you have none):
CMD ["robothood/main.py"]
