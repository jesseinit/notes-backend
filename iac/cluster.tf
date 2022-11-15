resource "digitalocean_kubernetes_cluster" "notes_api_cluster" {
  name     = "notes-api-cluster"
  region   = "ams3"
  version  = "1.24.4-do.0"
  vpc_uuid = digitalocean_vpc.notes-api-vpc.id

  tags = ["prod"]

  node_pool {
    name       = "notes-api-worker-pool"
    size       = "s-4vcpu-8gb"
    node_count = 1
    tags       = ["backend"]
  }
}

