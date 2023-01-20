data "aws_partition" "current" {}

data "aws_availability_zones" "available" {}


data "aws_ecrpublic_authorization_token" "token" {
  provider = aws.virginia
}

data "http" "my_ip" {
  url = "https://icanhazip.com"
}

data "http" "aws-lb-controller-policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.4.0/docs/install/iam_policy.json"

  request_headers = {
    Accept = "application/json"
  }
}
