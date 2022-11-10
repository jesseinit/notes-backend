terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}


resource "digitalocean_kubernetes_cluster" "notes_api_cluster" {
  name    = "notes-api-cluster"
  region  = "ams3"
  version = "1.24.4-do.0"

  tags = ["prod"]

  node_pool {
    name       = "notes-api-worker-pool"
    size       = "s-2vcpu-2gb"
    node_count = 1
    tags       = ["backend"]
  }
}

resource "digitalocean_container_registry" "notes-api-registry" {
  name                   = "notes-api-registry"
  subscription_tier_slug = "starter"
  region                 = "ams3"
}

resource "digitalocean_container_registry_docker_credentials" "notes-api-registry-cred" {
  registry_name = digitalocean_container_registry.notes-api-registry.name
}

provider "kubernetes" {
  host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
  token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
  )
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


resource "local_file" "kubeconfig" {
  depends_on = [digitalocean_kubernetes_cluster.notes_api_cluster]
  filename   = "./kubeconfig"
  content    = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config.0.raw_config
}
