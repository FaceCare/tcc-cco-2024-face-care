data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-*"]
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
  # ami                         = "ami-04b70fa74e45c3917"
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3a.small"
  # user_data                   = file("jupiter.sh")
  associate_public_ip_address = true
  subnet_id                   = aws_subnet.public_subnet[0].id
  vpc_security_group_ids      = [aws_security_group.allow_jupiter.id]
  iam_instance_profile        = data.aws_iam_instance_profile.instance_profile.name

  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }
  tags = {
    Name = "${local.project_name}-server"
  }
}
