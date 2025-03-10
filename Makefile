all: stop build start

stop:
	docker compose down || true

build:
	docker compose build --no-cache

start:
	docker compose up &

clean: stop
	docker ps -a -q | xargs -r docker stop
	docker ps -a -q | xargs -r docker rm
	docker images -q | xargs -r docker rmi -f
	docker volume ls -q | xargs -r docker volume rm

formatter:
	docker compose run --rm formatter

netdump: build
	@NETWORK=10.100.73; \
	OUTPUT_DIR=$(PWD)/out; \
	IMAGE_NAME=snmpdump-appliance-snmpwalker; \
	mkdir -p $$OUTPUT_DIR; \
	for i in $$(seq 60 254); do \
		HOST=$$NETWORK.$$i; \
		OUTPUT_FILE=/out/snmpwalk-$$HOST.txt; \
		echo "Scanning $$HOST..."; \
		docker run --rm -d --name snmpwalker_$$i \
			-v $$OUTPUT_DIR:/out \
			-v $(PWD)/libs:/usr/share/snmp/mibs \
			-e SNMP_VERSION=2c \
			-e MIBS=ALL \
			-e COMMUNITY=intelbras123 \
			-e HOST=$$HOST \
			-e VENDORID=SNMPv2-SMI::enterprises.26138 \
			-e OUTPUT_FILE=$$OUTPUT_FILE \
			$$IMAGE_NAME; \
	done
