variable "region" {
  default     = "eu-central-1"
  description = "Where to deploy the resources"
}

variable "profile" {
  default     = "default" #or init-1
  description = "AWS Credentials profile to be used"
}

variable "cluster_name" {
  default = "notes-cluster"
}

variable "account_id" {
  default = "866389174338" # 450543847015
}

variable "vpc_name" {
  default = "notes-vpc"
}

variable "registry_name" {
  default = "notes-registry"
}

variable "node_desired_size" {
  default = 2
}

variable "rds_database" {
  type = map(string)
  default = {
    "rds_user"          = "bigman2023"
    "rds_password"      = "bigman2023"
    "allocated_storage" = "20"
    "engine_version"    = "12"
    "db_name"           = "notes_db"
    "instance_class"    = "db.t3.micro"
  }
}
