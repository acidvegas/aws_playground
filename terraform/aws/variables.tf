variable "aws_region" {
  description = "The AWS region in which resources will be created."
  type        = string
}

variable "aws_security_group" {
  description = "The ID of the security group."
  type        = string
}

variable "aws_instance_type" {
  description = "The type of EC2 instance to create."
  type        = string
}

variable "aws_key_pair_name" {
  description = "The name of the AWS key pair."
  type        = string
}

variable "aws_user_data_file_path" {
  description = "Path to the user data script."
  type        = string
}

variable "aws_instance_count" {
  description = "Number of instances to create."
  type        = number
}
