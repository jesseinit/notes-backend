module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.4"

  cluster_name    = var.cluster_name
  cluster_version = "1.24"

  vpc_id                          = module.vpc.vpc_id
  subnet_ids                      = module.vpc.private_subnets
  cluster_endpoint_private_access = false
  cluster_endpoint_public_access  = true

  # Required for Karpenter role below
  enable_irsa = true

  node_security_group_tags = {
    # NOTE - if creating multiple security groups with this module, only tag the
    # security group that Karpenter should utilize with the following tag
    # (i.e. - at most, only one security group should have this tag in your account)
    "karpenter.sh/discovery" = var.cluster_name
  }

  node_security_group_additional_rules = {

    # Helm Install Metrics Server for this to have effect.
    ingress_cluster_metricserver = {
      description                   = "Cluster to node 4443 (Metrics Server)"
      protocol                      = "tcp"
      from_port                     = 4443
      to_port                       = 4443
      type                          = "ingress"
      source_cluster_security_group = true
    }
  }

  eks_managed_node_groups = {
    initial = {
      name = "initial-workers"

      instance_types = ["t3.medium"]

      min_size     = 1
      max_size     = 5
      desired_size = var.node_desired_size

      pre_bootstrap_user_data = <<-EOT
        #!/bin/bash
        echo "Hello Fucking Werld"
      EOT

      create_security_group = false
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

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    description = "SG Rule for RDS Access"

    cidr_blocks = [
      "10.0.0.0/8"
    ]
  }

  tags = {
    "karpenter.sh/discovery" = var.cluster_name
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


resource "helm_release" "aws_loadbalancer_controller" {
  depends_on       = [module.eks]
  namespace        = "kube-system"
  create_namespace = true

  name       = "aws-load-balancer-controller"
  repository = "https://aws.github.io/eks-charts"
  chart      = "aws-load-balancer-controller"
  version    = "1.4.6"

  set {
    name  = "clusterName"
    value = module.eks.cluster_name
  }
}

resource "null_resource" "alb_controller_crds" {
  depends_on = [module.eks]
  provisioner "local-exec" {
    on_failure  = fail
    interpreter = ["/bin/bash", "-c"]
    when        = create
    command     = <<EOT
        aws eks update-kubeconfig --region ${var.region} --profile ${var.profile} --name ${var.cluster_name}
        kubectl apply -f https://raw.githubusercontent.com/aws/eks-charts/master/stable/aws-load-balancer-controller/crds/crds.yaml
        echo "Applied ALB Controller Custom Resource Controllers"
     EOT
  }
}

resource "null_resource" "pre_cluster_deletion" {
  depends_on = [module.eks]
  provisioner "local-exec" {
    on_failure  = fail
    interpreter = ["/bin/bash", "-c"]
    when        = destroy
    command     = <<EOT
        aws eks update-kubeconfig --region eu-central-1 --profile dev01 --name notes-cluster
        kubectl delete -k ../../k8s/remote
        helm uninstall aws-load-balancer-controller
        echo "Uninstalled AWS Loadbalancer Controller"
     EOT
  }
}


