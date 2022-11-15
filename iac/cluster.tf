resource "digitalocean_kubernetes_cluster" "notes_api_cluster" {
  depends_on = [digitalocean_vpc.notes-api-vpc]
  name       = "notes-api-cluster"
  region     = "ams3"
  version    = "1.24.4-do.0"
  vpc_uuid   = digitalocean_vpc.notes-api-vpc.id

  tags = ["prod"]

  node_pool {
    # auto_scale = true
    # min_nodes  = 1
    # max_nodes  = 4
    name       = "notes-api-worker-pool"
    size       = "s-2vcpu-2gb"
    node_count = 1
    tags       = ["backend"]
  }
}

