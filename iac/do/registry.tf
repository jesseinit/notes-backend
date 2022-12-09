resource "digitalocean_container_registry" "notes-api-registry" {
  name                   = "notes-api-registry"
  subscription_tier_slug = "starter"
  region                 = "ams3"

  provisioner "local-exec" {
    command     = "doctl registry login && make push"
    working_dir = "../"
  }
}

resource "digitalocean_container_registry_docker_credentials" "notes-api-registry-cred" {
  registry_name = digitalocean_container_registry.notes-api-registry.name
}

resource "kubernetes_secret" "notes-api-regisry-secret" {
  metadata {
    name = digitalocean_container_registry.notes-api-registry.name
  }

  data = {
    ".dockerconfigjson" = digitalocean_container_registry_docker_credentials.notes-api-registry-cred.docker_credentials
  }

  type = "kubernetes.io/dockerconfigjson"
}
