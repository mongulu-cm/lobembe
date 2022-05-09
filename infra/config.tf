provider "aws" {
  region = var.region
}

resource "aws_dynamodb_table" "terraform-locks" {
  name           = "terraform-locks-lobembe"
  billing_mode   = "PROVISIONED"
  hash_key       = "LockID"
  read_capacity  = 1
  write_capacity = 1

  attribute {
    name = "LockID"
    type = "S"
  }
}

terraform {
  required_version = ">= 0.13"

  backend "s3" {
    bucket         = "terraform-state-mongulu" # should exists
    key            = "lobembe/terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "terraform-locks-lobembe"
    //encrypt = true
  }
}
