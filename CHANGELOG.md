# Changelog

## 20.08

* Deprecate SSL configuration
* The `https` section has been moved to `rest_api` to be similar to other daemons.

## 19.06

* The following endpoints are now multi-tenant.

  This means that created resources will be in the same tenant as the creator or in the tenant
  specified by the Wazo-Tenant HTTP header. Listing resources will also only list the ones in the
  user's tenant unless a sub-tenant is specified using the Wazo-Tenant header. The `recurse=true`
  query string can be used to list from multiple tenants. GET, DELETE and PUT on a resource that is
  not tenant accessible will result in a 404. New readonly parameter has also been added:
  `tenant_uuid`.

  * `/agents`

## 17.05

* Add an optional `reason` field to the body of the pause resource.

  * POST `/agents/by-number/{agent_number}/pause`

## 15.19

* Token authentication is now required for all routes, i.e. it is not possible to interact with
  xivo-agentd without a wazo-auth authentication token.

## 15.18

* xivo-agentd now uses HTTPS instead of HTTP.

## 15.15

* The resources returning agent statuses, i.e.:

  * GET `/agents`
  * GET `/agents/by-id/{agent_id}`
  * GET `/agents/by-number/{agent_number}`

  are now returning an additional argument named "state_interface", which is "the interface (e.g.
  SIP/alice) that is used to determine if an agent is in use or not".
