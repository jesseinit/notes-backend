# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = var.do_token
}

# Connect heml to the created cluster
provider "helm" {
  kubernetes {
    host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
    token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
    cluster_ca_certificate = base64decode(
      digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
    )
  }
}

# Connect kubernetes to the created cluster
provider "kubernetes" {
  host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
  token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
  )
}

# Exports Cluster Config to Module Kubectl Context
provider "kubectl" {
  host  = digitalocean_kubernetes_cluster.notes_api_cluster.endpoint
  token = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].token
  cluster_ca_certificate = base64decode(
    digitalocean_kubernetes_cluster.notes_api_cluster.kube_config[0].cluster_ca_certificate
  )
  load_config_file = false
}

# Exports Cluster Config to Local Kubectl Context
resource "local_file" "kubeconfig" {
  depends_on = [digitalocean_kubernetes_cluster.notes_api_cluster]
  filename   = pathexpand("~/.kube/config")
  content    = digitalocean_kubernetes_cluster.notes_api_cluster.kube_config.0.raw_config
}



