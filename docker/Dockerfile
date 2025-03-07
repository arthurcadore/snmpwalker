FROM alpine:latest

RUN apk add --no-cache net-snmp-tools

WORKDIR /out

ENTRYPOINT ["/bin/sh", "-c", "snmpwalk -v$SNMP_VERSION -m $MIBS -c $COMMUNITY $HOST $VENDORID -O q | awk '{cmd=\"snmptranslate -On \"$1; cmd | getline oid; close(cmd); print oid, $0}' | tee /out/snmpwalk.txt"]
