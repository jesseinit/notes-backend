variable "region" {
  default     = "eu-central-1"
  description = "Where to deploy the resources"
}

variable "profile" {
  default     = "default" #or init-1
  description = "AWS Credentials profile to be used"
}

variable "cluster_name" {
  default = "notes-api-cluster"
}

variable "account_id" {
  default = "450543847015"
}

variable "vpc_name" {
  default = "notes-api-vpc"
}

variable "registry_name" {
  default = "notes-api"
}

variable "node_desired_size" {
  default = 3
}
