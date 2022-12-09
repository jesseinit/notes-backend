resource "aws_ecr_repository" "foo" {
  name                 = var.registry_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}
