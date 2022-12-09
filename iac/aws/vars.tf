variable "region" {
  default     = "eu-central-1"
  description = "Where to deploy the resources"
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
  default = "notes-api-registry"
}
