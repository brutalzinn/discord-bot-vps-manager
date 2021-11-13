DATA=$(date '+%d-%m-%Y %H:%M:%S') &&
CONTENT="O deploy do boberto foi um sucesso. $DATA" &&
URL=https://discord.com/api/webhooks/909208092166725743/VRYl-EIn2BE2Fq6iCT1B_VTIlid3HILjlAj8dHCiU5KVU9U85wHLpjPWJRsVaX7j_JtK &&
curl -X POST -H 'Content-Type: application/json' -d '{"content":"'"$CONTENT"'"}' $URL
