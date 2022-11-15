resource "digitalocean_project" "notes-api-project" {
  name        = "notes-api-project"
  description = "Notes Api Project"
  purpose     = "Web Application"
  environment = "Development"
}
