module "s3-website" {
  source  = "cloudposse/s3-website/aws"
  version = "0.17.0"
  # insert the 13 required variables here

  hostname  = "blog.mongulu.cm"
  logs_enabled = false # change namespace from eg to mongulu to avoid bucket already exists
  parent_zone_name = "mongulu.cm"
}


module "cdn" {
  source  = "cloudposse/cloudfront-s3-cdn/aws"
  version = "0.82.4"

  external_aliases                  = ["blog.mongulu.cm"]
  dns_alias_enabled                 = true
  parent_zone_name                  = "mongulu.cm"
  acm_certificate_arn               = "arn:aws:acm:us-east-1:053932140667:certificate/35f51ab4-1f12-4a13-a96a-b590bbc80b7a"
  cache_policy_id                   = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad"
  cloudfront_access_logging_enabled = false
  s3_access_logging_enabled = false
  cloudfront_access_log_create_bucket = false
  website_enabled                   = true
  origin_bucket = "blog.mongulu.cm"
  name                          = "lobembe"
  stage                         = "prod"
  namespace                     = "mongulu"
  override_origin_bucket_policy = false

  depends_on = [module.s3-website]

}