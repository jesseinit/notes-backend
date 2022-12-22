resource "aws_db_instance" "rds" {
  # Replace with your desired database engine (e.g. mysql, postgres)
  engine = "postgres"
  # Configure the instance size and storage capacity
  instance_class    = "db.t4g.xlarge"
  allocated_storage = 50
  engine_version    = "12"

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  #   vpc_security_group_ids = [aws_security_group.node_sg.id]

  # Replace with your desired username and password
  username = "bigman2023"
  password = "bigman2023"

  # Replace with your desired database name
  db_name = "mydatabase"
}

resource "aws_subnet" "rds-sn-1" {
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.7.0/24"
  availability_zone = data.aws_availability_zones.available.names[0]

  tags = {
    Name = "aws_subnet.rds-sn-1.id"
  }
}

resource "aws_subnet" "rds-sn-2" {
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.8.0/24"
  availability_zone = data.aws_availability_zones.available.names[1]

  tags = {
    Name = "aws_subnet.rds-sn-2.id"
  }
}

resource "aws_db_subnet_group" "rds" {
  name = "rds-subnet"
  #   subnet_ids = [aws_subnet.frontend.id, aws_subnet.backend.id]
  #   subnet_ids = [module.vpc.public_subnets.*.id]
  subnet_ids = [aws_subnet.rds-sn-1.id, aws_subnet.rds-sn-2.id]
  # "azs  = slice(data.aws_availability_zones.available.names, 0, 2)"


  tags = {
    Name = "My DB subnet group"
  }
}

resource "aws_security_group" "rds" {
  name   = "rds-security-group"
  vpc_id = module.vpc.vpc_id



  # Allow traffic from the IP address or network that your Kubernetes cluster is running on
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
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
