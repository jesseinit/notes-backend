provider "aws" {
  profile = "default"
  region  = var.region
}

provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--region", var.region, "--cluster-name", module.eks.cluster_name]
  }
}

# Exports Cluster Config to Module Kubectl Context
# provider "kubectl" {
#   host                   = data.aws_eks_cluster.cluster.endpoint
#   cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
# #   token                  = data.aws_eks_cluster_auth.cluster.token
#   load_config_file       = false
# }


locals {
  kubeconfig = <<KUBECONFIG
apiVersion: v1
clusters:
    - cluster:
        server: ${module.eks.cluster_endpoint}
        certificate-authority-data: ${module.eks.cluster_certificate_authority_data}
      name: arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}
contexts:
    - context:
        cluster: arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}
        user: arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}
current-context: arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}
kind: Config
preferences: {}
users:
    - name: arn:aws:eks:${var.region}:${var.account_id}:cluster/${var.cluster_name}
user:
    exec:
    apiVersion: client.authentication.k8s.io/v1alpha1
    command: aws
    args:
        - --region
        - ${var.region}
        - eks
        - get-token
        - --cluster-name
        - notes-api-cluster
        - "${var.cluster_name}"
KUBECONFIG
}


# Exports Cluster Config to Local Kubectl Context
resource "local_file" "kubeconfig" {
  filename = pathexpand("~/.kube/config")
  content  = local.kubeconfig
}

data "aws_availability_zones" "available" {}
