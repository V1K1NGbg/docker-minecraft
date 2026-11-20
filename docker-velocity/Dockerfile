FROM eclipse-temurin:25-jdk as build

RUN apt-get update -y && apt-get upgrade -y && apt-get install git wget jq -y
RUN git config --global core.autocrlf input

ARG version=3.1.1
ARG build

ENV version=$version
ENV build=$build

RUN wget -qO- "https://fill.papermc.io/v3/projects/velocity/versions/${version}/builds/${build}" \
    | jq -r '.downloads["server:default"].url' \
    | xargs wget -O "/velocity.jar"

######################################################################################

FROM eclipse-temurin:25-jdk

RUN apt-get update -y && apt-get upgrade -y

COPY --from=build /velocity.jar /

RUN mkdir -p /data \
    && mkdir -p /plugins \
    && adduser --disabled-password --gecos "" --home /home/minecraft minecraft \
    && chown -R minecraft /data /plugins /home/minecraft \
    && chmod -R 755 /data /home/minecraft

VOLUME ["/data","/plugins"]

WORKDIR /data

USER minecraft

ARG flags=""

ENV min=1 \
    max=2 \
    JAVA_FLAGS="$flags" \
    SERVER_START="-jar /velocity.jar" \
    SERVER_ARGS=""

COPY start.sh /start.sh

CMD ["/start.sh"]

EXPOSE 25577
