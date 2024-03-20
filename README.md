# atlas-post-install
Container image for automating post-installation steps in Aurelius Atlas

## Environment variables
To configure the job you have to specify the following environment variables:
| variable | description | default |
| NAMESPACE | Kubernetes release namespace | demo |
| ELASTIC_URL | base url of the elastic cluster | default: `http://elastic-search-es-http.$NAMESPACE.svc.cluster.local:9200/` |
| ENTERPRISE_SEARCH_URL | base url of the enterprise search | `http://enterprise-search-ent-http.$NAMESPACE.svc.cluster.local:3002/` |
| ELASTIC_USERNAME | elastic username for authentication | `elastic`|
| ELASTIC_PASSWORD | elastic password for authentication | `elastic`|
| KEYCLOAK_ATLAS_USERNAME | atlas username for for authentication | `atlas` |
| KEYCLOAK_ATLAS_PASSWORD | atlas password for authentication | `atlas` |
| ATLAS_URL | base url of the Apache Atlas API | `http://atlas.$NAMESPACE.svc.cluster.local:21000/api/atlas` |
| KEYCLOAK_URL | base url of the Keycloak server | `http://keycloak.$NAMESPACE.svc.cluster.local:8080/auth/` |
