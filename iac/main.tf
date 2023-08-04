terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.9.0"
    }
  }
}

provider "aws" {
  profile = var.profile_name
  region  = var.region
}

resource "aws_s3_bucket" "fast-resources-search" {
  bucket = var.static_site_bucket_name
  tags = {
    Name = var.static_site_bucket_name
  }
}

resource "aws_s3_bucket_website_configuration" "fast-resources-search" {
  bucket = aws_s3_bucket.fast-resources-search.id

  index_document {
    suffix = var.index_document_name
  }

  error_document {
    key = var.index_document_name
  }
}

# resource "aws_s3_bucket_acl" "fast-resources-search" {
#     bucket = aws_s3_bucket.fast-resources-search.id
#     acl = "public-read"
# }

# resource "aws_s3_bucket_policy" "fast-resources-search" {
#     bucket = aws_s3_bucket.fast-resources-search.id

#     policy = jsonencode({
#         Version = "2012-10-17"
#         Statement = [
#             {
#                 Sid = "PublicReadGetObject"
#                 Effect = "Allow"
#                 Principal = "*"
#                 Action = "s3:GetObject"
#                 Resource = [
#                     aws_s3_bucket.fast-resources-search.arn,
#                     "${aws_s3_bucket.fast-resources-search.arn}/*",
#                 ]
#             },
#         ]
#     })
# }

module "static_files" {
  source   = "hashicorp/dir/template"
  base_dir = var.base_dir
}

resource "aws_s3_object" "static_file" {
  for_each     = module.static_files.files
  bucket       = aws_s3_bucket.fast-resources-search.id
  key          = trimprefix(each.value.source_path, "${var.base_dir}/")
  source       = abspath(each.value.source_path)
  content_type = each.value.content_type
  etag         = filemd5(abspath(each.value.source_path))
}