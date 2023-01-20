resource "aws_db_instance" "rds" {
  # Replace with your desired database engine (e.g. mysql, postgres)
  engine = "postgres"

  # Configure the instance size and storage capacity
  instance_class    = var.rds_database["instance_class"]
  allocated_storage = var.rds_database["allocated_storage"]
  engine_version    = var.rds_database["engine_version"]

  vpc_security_group_ids = [aws_security_group.rds_admin_sg.id, aws_security_group.node_sg.id]
  db_subnet_group_name   = module.vpc.database_subnet_group_name

  # Replace with your desired username and password
  username = var.rds_database["rds_user"]
  password = var.rds_database["rds_password"]

  # Replace with your desired database name
  db_name = var.rds_database["db_name"]

  skip_final_snapshot = true
  publicly_accessible = true
  identifier          = "notes-db"
}

resource "aws_security_group" "rds_admin_sg" {
  name   = "notes-db-admin-sg"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    description = "SG Rule to allow Admin"
    cidr_blocks = [
      "${chomp(data.http.my_ip.response_body)}/32",
    ]
  }
  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = [
      "0.0.0.0/0",
    ]
  }
}


resource "kubernetes_secret" "rds" {
  metadata {
    name = "rds-credentials"
  }

  data = {
    DATABASE_HOST : aws_db_instance.rds.address
    DATABASE_PORT : aws_db_instance.rds.port
    DATABASE_PASSWORD : aws_db_instance.rds.password
    DATABASE_USERNAME : aws_db_instance.rds.username
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
