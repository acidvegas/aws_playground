provider "aws" {
  region  = var.aws_region
}

data "aws_ami" "debian_latest_AMI" {
  most_recent = true
  owners      = ["136693071363"]
  filter {
    name   = "name"
    values = ["debian-12-amd64-*-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "instance" {
  count = var.aws_instance_count
  ami = data.aws_ami.debian_latest_AMI.id
  instance_type = var.aws_instance_type
  vpc_security_group_ids = [var.aws_security_group]
  key_name  = var.aws_key_pair_name
  user_data = "${file(var.aws_user_data_file_path)}"
  tags = {
    Name = "node-${count.index}"
  }
}