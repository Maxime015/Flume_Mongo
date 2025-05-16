FROM openjdk:8-jre
ENV FLUME_VERSION=1.9.0
ENV FLUME_HOME=/opt/flume

# Installer curl et les certificats SSL
RUN apt-get update && apt-get install -y curl ca-certificates

# Copier l’archive Flume téléchargée localement
COPY apache-flume-1.9.0-bin.tar.gz .

# Décompresser et configurer Flume
RUN tar -xzf apache-flume-1.9.0-bin.tar.gz -C /opt && \
    mv /opt/apache-flume-1.9.0-bin $FLUME_HOME && \
    rm apache-flume-1.9.0-bin.tar.gz
    
RUN apt-get update && apt-get install -y net-tools
# Ajouter Flume au PATH
ENV PATH=$PATH:$FLUME_HOME/bin

# Créer un dossier de logs
RUN mkdir -p /flume/logs
VOLUME ["/flume/log"]

# Copier ta configuration Flume
COPY flume.conf $FLUME_HOME/conf/flume.conf

# Lancer Flume à l’exécution du conteneur
CMD ["flume-ng", "agent", "--conf", "/opt/flume/conf", "--conf-file", "/opt/flume/conf/flume.conf", "--name", "agent", "-Dflume.root.logger=INFO,console"]

