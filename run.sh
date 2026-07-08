#/usr/bin/env bash
set -vx

source $(pwd)/.env

podman run \
	-p 127.0.0.1:${KC_PORT}:${KC_PORT} \
	-e KC_BOOTSTRAP_ADMIN_USERNAME=${KC_BOOTSTRAP_ADMIN_USERNAME} \
	-e KC_BOOTSTRAP_ADMIN_PASSWORD=${KC_BOOTSTRAP_ADMIN_PASSWORD} \
	quay.io/keycloak/keycloak:26.6.4 start-dev
