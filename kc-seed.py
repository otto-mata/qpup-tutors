# /usr/bin/env python

import os
import dotenv
from keycloak import KeycloakAdmin

dotenv.load_dotenv("./.env")

admin = KeycloakAdmin(
    server_url="http://localhost:8080/",
    username=f"{os.environ.get('KC_BOOTSTRAP_ADMIN_USERNAME')}",
    password=f"{os.environ.get('KC_BOOTSTRAP_ADMIN_PASSWORD')}",
    realm_name="master",
    pool_maxsize=20,
)

new_user_id = admin.create_user(  # type: ignore
    {
        "email": "tutor@42paris.fr",
        "username": "tutor",
        "enabled": True,
        "firstName": "Jean",
        "lastName": "Doe",
        "credentials": [
            {
                "value": "secret",
                "type": "password",
                "temporary": False,
            }
        ],
    },
    exist_ok=True,
)

print(admin.get_user(new_user_id))

new_client_id = admin.create_client(  # type: ignore
    {
        "clientId": "auth",
        "name": "",
        "description": "",
        "rootUrl": "",
        "adminUrl": "",
        "baseUrl": "",
        "surrogateAuthRequired": False,
        "enabled": True,
        "alwaysDisplayInConsole": False,
        "clientAuthenticatorType": "client-secret",
        "redirectUris": ["http://localhost:3000/auth"],
        "webOrigins": ["http://localhost:3000"],
        "notBefore": 0,
        "bearerOnly": False,
        "consentRequired": False,
        "standardFlowEnabled": True,
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False,
        "serviceAccountsEnabled": False,
        "publicClient": True,
        "frontchannelLogout": True,
        "protocol": "openid-connect",
        "attributes": {
            "realm_client": "false",
            "logout.confirmation.enabled": "false",
            "oidc.ciba.grant.enabled": "false",
            "backchannel.logout.session.required": "true",
            "standard.token.exchange.enabled": "false",
            "oauth2.jwt.authorization.grant.enabled": "false",
            "frontchannel.logout.session.required": "true",
            "oauth2.device.authorization.grant.enabled": "false",
            "display.on.consent.screen": "false",
            "backchannel.logout.revoke.offline.tokens": "false",
            "dpop.bound.access.tokens": "false",
        },
        "authenticationFlowBindingOverrides": {},
        "fullScopeAllowed": True,
        "nodeReRegistrationTimeout": -1,
        "defaultClientScopes": [
            "web-origins",
            "acr",
            "roles",
            "profile",
            "basic",
            "email",
        ],
        "optionalClientScopes": [
            "address",
            "phone",
            "offline_access",
            "organization",
            "microprofile-jwt",
        ],
        "access": {"view": True, "configure": True, "manage": True},
    },
    skip_exists=True,
)

print(admin.get_client(new_client_id))
