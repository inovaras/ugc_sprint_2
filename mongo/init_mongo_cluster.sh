#!/bin/bash

echo "Starting MongoDB Cluster Initialization..."

# Функция для проверки готовности MongoDB узла
wait_for_mongo() {
  local host=$1
  local port=$2
  echo "Waiting for MongoDB at $host:$port..."
  until mongosh --quiet --host "$host" --port "$port" --eval "db.adminCommand({ ping: 1 })" > /dev/null 2>&1; do
    sleep 2
  done
  echo "MongoDB at $host:$port is ready."
}

# Инициализация репликационного набора для шарда
init_shard_replica_set() {
  local replSetName=$1
  local nodes=$2
  echo "Initializing Replica Set: $replSetName with nodes: $nodes..."
  mongosh --quiet --host "$(echo $nodes | cut -d, -f1)" --eval "
    rs.initiate({
      _id: '$replSetName',
      members: [
        $(echo $nodes | awk -F, '{for (i=1; i<=NF; i++) printf "{ _id: %d, host: \"%s\" },", i-1, $i}' | sed 's/,$//')
      ]
    });
    while (rs.status().ok !== 1) { sleep(100); }
  "
  echo "Replica Set $replSetName initialized."
}

# Инициализация конфигурационного репликационного набора
init_config_replica_set() {
  local nodes=$1
  echo "Initializing Config Server Replica Set..."
  mongosh --quiet --host "$(echo $nodes | cut -d, -f1)" --eval "
    rs.initiate({
      _id: 'mongors1conf',
      configsvr: true,
      members: [
        $(echo $nodes | awk -F, '{for (i=1; i<=NF; i++) printf "{ _id: %d, host: \"%s\" },", i-1, $i}' | sed 's/,$//')
      ]
    });
    while (rs.status().ok !== 1) { sleep(100); }
  "
  echo "Config Server Replica Set initialized."
}

# Конфигурация маршрутизаторов
configure_shards() {
  local mongos_host=$1
  echo "Adding shards to the cluster..."
  mongosh --quiet --host "$mongos_host" --eval "
    sh.addShard('mongors1/mongors1n1:27017,mongors1n2:27017,mongors1n3:27017');
    sh.addShard('mongors2/mongors2n1:27017,mongors2n2:27017,mongors2n3:27017');
    sh.status();
  "
  echo "Shards added to the cluster."
}

# Создание коллекций
create_collections() {
  local mongos_host=$1
  local db=$2
  shift 2
  local collections=("$@")

  echo "Creating database $db and collections: ${collections[*]}..."
  
  # Генерация и выполнение команды для создания каждой коллекции
  for collection in "${collections[@]}"; do
    mongosh --quiet --host "$mongos_host" --eval "
      use $db;
      db.createCollection('$collection');
    " || {
      echo "Error: Failed to create collection $collection in database $db."
      exit 1
    }
    echo "Collection $collection created in database $db."
  done

  echo "Database $db created with collections: ${collections[*]}."
}

shard_database() {
  local mongos_host=$1
  local db=$2
  local collection=$3
  local shard_key=$4
  local shard_type=$5
  echo "Enabling sharding for database $db and collection $collection..."
  mongosh --quiet --host "$mongos_host" --eval "
    sh.enableSharding('$db');
    sh.shardCollection('$db.$collection', { $shard_key: $shard_type });
  " || {
    echo "Error: Failed to enable sharding for $db.$collection."
    exit 1
  }
  echo "Sharding enabled for $db.$collection."
}

# Ожидание готовности всех узлов
wait_for_mongo mongors1n1 27017
wait_for_mongo mongors1n2 27017
wait_for_mongo mongors1n3 27017
wait_for_mongo mongors2n1 27017
wait_for_mongo mongors2n2 27017
wait_for_mongo mongors2n3 27017
wait_for_mongo mongocfg1 27017
wait_for_mongo mongocfg2 27017
wait_for_mongo mongocfg3 27017

# Инициализация репликационных наборов
init_shard_replica_set "mongors1" "mongors1n1:27017,mongors1n2:27017,mongors1n3:27017"
init_shard_replica_set "mongors2" "mongors2n1:27017,mongors2n2:27017,mongors2n3:27017"

# Инициализация конфигурационного сервера
init_config_replica_set "mongocfg1:27017,mongocfg2:27017,mongocfg3:27017"

# Конфигурация маршрутизаторов
wait_for_mongo mongos1 27017
configure_shards "mongos1:27017"

# Создание базы данных
create_collections "mongos1:27017" "ugc" "users" "movies" "ratings"

# Включение шардинга для базы данных
shard_database "mongos1:27017" "ugc" "users" "_id" "'hashed'"
shard_database "mongos1:27017" "ugc" "movies" "_id" "'hashed'"
shard_database "mongos1:27017" "ugc" "ratings" "movie_id" "1"

echo "MongoDB Cluster Configuration Complete!"