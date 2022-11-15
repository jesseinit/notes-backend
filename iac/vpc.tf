resource "digitalocean_vpc" "notes-api-vpc" {
  name       = "notes-api-vpc"
  region     = "ams3"
  depends_on = [digitalocean_project.notes-api-project]
}
