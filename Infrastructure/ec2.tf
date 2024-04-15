data "aws_ami" "amzlinux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-gp2"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

data "aws_iam_instance_profile" "instance_profile" {
  name = "LabInstanceProfile"
}

resource "aws_instance" "jupiter_notebook" {
  ami           = data.aws_ami.amzlinux.id
  instance_type = "t2.micro"
  user_data       = file("jupiter.sh")
  associate_public_ip_address = true
  subnet_id                   = aws_subnet.public_subnet[0].id
  vpc_security_group_ids      = [aws_security_group.allow_jupiter.id]
  iam_instance_profile        = data.aws_iam_instance_profile.instance_profile.name

  tags = {
    Name = "${local.project_name}-jupiter-notebook"
  }
}
