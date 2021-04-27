resource "aws_s3_bucket" "website" {
  bucket = var.website_bucket_name
  acl = "public-read"

  tags  = {
    Name = "Community"
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT","POST","GET"]
    allowed_origins = ["*"]
  }

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForGetBucketObjects",
      "Effect": "Allow",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${var.website_bucket_name}/*"
    }
  ]
}
EOF

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

}