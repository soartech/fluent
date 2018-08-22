#!/usr/bin/env bash

cd "$(dirname "$0")"

SWAGGERCLI=swagger-codegen-cli.jar

if ! [ -f $SWAGGERCLI ]; then
   wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O $SWAGGERCLI
fi

java -jar $SWAGGERCLI generate -c ./SwaggerPythonClientConfig.json -i ../RecommenderUIAPI.yaml -l python -o ../clients/python/