resource "aws_subnet" "lb_subnets_1" {
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.9.0/24"
  availability_zone = data.aws_availability_zones.available.names[0]
}

resource "aws_subnet" "lb_subnets_2" {
  vpc_id            = module.vpc.vpc_id
  cidr_block        = "10.0.10.0/24"
  availability_zone = data.aws_availability_zones.available.names[2]
}

resource "aws_lb" "notes_lb" {
  name               = "notes-lb"
  internal           = false
  load_balancer_type = "application"

  subnets = [aws_subnet.lb_subnets_1.id, aws_subnet.lb_subnets_2.id]

  enable_deletion_protection = false
}
