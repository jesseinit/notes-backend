resource "aws_db_instance" "rds" {
  # Replace with your desired database engine (e.g. mysql, postgres)
  engine = "postgres"

  # Configure the instance size and storage capacity
  instance_class    = var.rds_database["instance_class"]
  allocated_storage = var.rds_database["allocated_storage"]
  engine_version    = var.rds_database["engine_version"]

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.rds_sng.name

  # Replace with your desired username and password
  username = var.rds_database["rds_user"]
  password = var.rds_database["rds_password"]

  # Replace with your desired database name
  db_name = var.rds_database["db_name"]

  skip_final_snapshot = true
}

resource "aws_subnet" "rds_subnets_1" {
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.7.0/24"
  availability_zone = data.aws_availability_zones.available.names[0]
}

resource "aws_subnet" "rds_subnets_2" {
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.8.0/24"
  availability_zone = data.aws_availability_zones.available.names[2]
}

resource "aws_db_subnet_group" "rds_sng" {
  name       = "rds-subnet"
  subnet_ids = [aws_subnet.rds_subnets_1.id, aws_subnet.rds_subnets_2.id]
}

resource "aws_security_group" "rds_sg" {
  name   = "notes-db-sg"
  vpc_id = module.vpc.vpc_id
}

resource "aws_security_group_rule" "rds_allow_k8s_nodes" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.rds_sg.id
  source_security_group_id = aws_security_group.node_sg.id
}

resource "kubernetes_secret" "rds" {
  metadata {
    name = "rds-credentials"
  }

  data = {
    DATABASE_HOST : aws_db_instance.rds.address
    DATABASE_PORT : aws_db_instance.rds.port
    DATABASE_URL : "postgresql://${aws_db_instance.rds.username}:${aws_db_instance.rds.password}@${aws_db_instance.rds.endpoint}/${aws_db_instance.rds.db_name}"
  }
}


output "rds-details" {
  value = {
    DATABASE_HOST : aws_db_instance.rds.address
    DATABASE_PORT : aws_db_instance.rds.port
    DATABASE_URL : "postgresql://${aws_db_instance.rds.username}:${aws_db_instance.rds.password}@${aws_db_instance.rds.endpoint}/${aws_db_instance.rds.db_name}"
  }
  sensitive = true
}
