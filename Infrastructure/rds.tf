# resource "aws_db_subnet_group" "public_subnet_group" {       # vamos utilizar o banco na propria ec2
#   name       = "main" 
#   subnet_ids = [aws_subnet.public_subnet[0].id,aws_subnet.public_subnet[1].id]

#   tags = {
#     Name = "${local.project_name}_subnet_group"
#   }
# }

# resource "aws_db_instance" "rds_instance" {        # vamos utilizar o banco na propria ec2
#   engine                 = "mysql"
#   db_name                = "tcc_2024"
#   identifier             = "${local.project_name}-rds"
#   instance_class         = "db.t3.micro"
#   allocated_storage      = 10
#   publicly_accessible    = true
#   username               = var.db_username
#   password               = var.db_password
#   vpc_security_group_ids = [aws_security_group.allow_rds.id]
#   db_subnet_group_name   = aws_db_subnet_group.public_subnet_group.id
#   skip_final_snapshot    = true

#   tags = {
#     Name = "${local.project_name}-rds"
#   }
# }
