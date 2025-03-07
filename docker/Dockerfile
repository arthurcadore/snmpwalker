FROM alpine:latest

RUN apk add --no-cache net-snmp-tools

WORKDIR /out

ENTRYPOINT ["/bin/sh", "-c", "snmpwalk -v$SNMP_VERSION -m $MIBS -c $COMMUNITY $HOST $OID > /out/snmpwalk.txt"]
