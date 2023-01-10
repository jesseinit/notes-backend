module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.4"

  cluster_name    = var.cluster_name
  cluster_version = "1.24"

  vpc_id                          = module.vpc.vpc_id
  subnet_ids                      = module.vpc.private_subnets
  cluster_endpoint_private_access = false
  cluster_endpoint_public_access  = true

  tags = {
    "k8s.io/cluster-autoscaler/${var.cluster_name}" = "owned",
    "k8s.io/cluster-autoscaler/enabled"             = true
  }

  # # Required for Karpenter role below
  # enable_irsa = true

  eks_managed_node_groups = {
    base_workers = {
      name = "base_workers"

      instance_types = ["t3.medium"]

      min_size     = 2
      max_size     = 4
      desired_size = 2

      pre_bootstrap_user_data = <<-EOT
        #!/bin/bash
        echo "Hello Fucking Werld"
      EOT

      vpc_security_group_ids = [
        aws_security_group.node_sg.id
      ]
      labels = {
        "environment"   = "prod"
        "instance-type" = "t3.medium"
      }
    }
  }
}

# Added to allow cluster to be able to provision volumes
resource "aws_eks_addon" "ebs-csi-driver" {
  cluster_name  = module.eks.cluster_name
  addon_name    = "aws-ebs-csi-driver"
  addon_version = "v1.13.0-eksbuild.3"
}

resource "aws_security_group" "node_sg" {
  name_prefix = "workers-sg"
  description = "Security Group for the Nodes"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "10.0.0.0/8"
    ]
  }
}

data "http" "aws-lb-controller-policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.0/docs/install/iam_policy.json"

  request_headers = {
    Accept = "application/json"
  }
}

resource "aws_iam_policy" "load-balancer-policy" {
  name        = "AWSLoadBalancerControllerIAMPolicy"
  description = "AWS LoadBalancer Controller IAM Policy"
  policy      = data.http.aws-lb-controller-policy.response_body
}

resource "aws_iam_role_policy_attachment" "load-balancer-policy-attachment" {
  depends_on = [
    aws_iam_policy.load-balancer-policy
  ]
  policy_arn = aws_iam_policy.load-balancer-policy.arn
  for_each   = module.eks.eks_managed_node_groups
  role       = each.value["iam_role_name"]
}

#Allows EC2 Instances to be able to Create EBS Volumes
resource "aws_iam_role_policy_attachment" "AmazonEBSCSIDriverPolicyAttachetment" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
  for_each   = module.eks.eks_managed_node_groups
  role       = each.value["iam_role_name"]
}


resource "null_resource" "post-policy" {
  depends_on = [module.eks]
  provisioner "local-exec" {
    on_failure  = fail
    interpreter = ["/bin/bash", "-c"]
    when        = create
    command     = <<EOT
        aws eks update-kubeconfig --region ${var.region} --profile ${var.profile} --name ${var.cluster_name}
        helm repo add eks https://aws.github.io/eks-charts
        kubectl apply -f https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
        helm install aws-load-balancer-controller eks/aws-load-balancer-controller --set clusterName=${var.cluster_name} -n kube-system
        echo "Done"
     EOT
  }
}
