resource "aws_ecr_repository" "ecr" {
  name                 = var.registry_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true
}

# Build and push an image to the ECR repository
resource "null_resource" "build_and_push_image" {
  provisioner "local-exec" {
    command = <<EOF
      # Build the Docker image
      # cd ../.. && docker build -t ${aws_ecr_repository.ecr.repository_url}:latest .
      cd ../.. && docker buildx build --platform linux/amd64 -t ${aws_ecr_repository.ecr.repository_url}:latest .

      # Log in to the ECR registry
      aws ecr get-login-password --region ${var.region} | docker login --username AWS --password-stdin ${var.account_id}.dkr.ecr.${var.region}.amazonaws.com

      # Push the image to the ECR registry
      docker push ${aws_ecr_repository.ecr.repository_url}:latest
    EOF
  }
}

output "ecr-repository" {
  description = "ECR Repository URL"
  value       = aws_ecr_repository.ecr.repository_url
}
