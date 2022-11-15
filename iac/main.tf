terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }

    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }

  }
}

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

provider "helm" {
  # Several Kubernetes authentication methods are possible: https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs#authentication
  kubernetes {
    host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
    token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
    cluster_ca_certificate = base64decode(
      digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
    )
  }
}

provider "kubernetes" {
  host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
  token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
  )
}

provider "kubectl" {
  host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
  token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
  )
  load_config_file = false
}


resource "local_file" "kubeconfig" {
  depends_on = [digitalocean_kubernetes_cluster.notes_api_cluster]
  filename   = pathexpand("~/.kube/config")
  content    = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config.0.raw_config
}



