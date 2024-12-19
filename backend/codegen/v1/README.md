## To generate the schema:
- go to /swagger/?format=openapi
- copy the schema
- paste into a json file like openapi.json
- compile using:
```sh
openapi-generator-cli generate -i ./openapi.json -g typescript-axios -o ./typescript/out
```