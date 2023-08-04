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

resource "aws_api_gateway_rest_api" "fast_resources_search_api" {
  name = "FAST-Resources_Reverse-Index-API"
}

resource "aws_api_gateway_resource" "reverse_index" {
  rest_api_id = aws_api_gateway_rest_api.fast_resources_search_api.id
  parent_id   = aws_api_gateway_rest_api.fast_resources_search_api.root_resource_id
  path_part   = "FAST-Resources_Reverse-Index"
}

resource "aws_api_gateway_method" "reverse_index_GET" {
  rest_api_id      = aws_api_gateway_rest_api.fast_resources_search_api.id
  resource_id      = aws_api_gateway_resource.reverse_index.id
  http_method      = "GET"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method" "reverse_index_OPTIONS" {
  rest_api_id   = aws_api_gateway_rest_api.fast_resources_search_api.id
  resource_id   = aws_api_gateway_resource.reverse_index.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "reverse_index_search_cloudwatch_policy_document" {
  statement {
    effect    = "Allow"
    actions   = ["logs:CreateLogGroup"]
    resources = ["arn:aws:logs:eu-west-1:816859564208:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:eu-west-1:816859564208:log-group:/aws/lambda/FAST-Resources_Reverse-Index:*"]
  }
}

resource "aws_iam_policy" "reverse_index_search_cloudwatch_policy" {
  name        = "ReverseIndexSearchCloudWatchPolicy"
  path        = "/service-role/"
  description = "IAM policy for cloudwatch log group of reverse_index_search"
  policy      = data.aws_iam_policy_document.reverse_index_search_cloudwatch_policy_document.json
}

data "aws_iam_policy_document" "reverse_index_search_dynamodb_policy" {
  statement {
    effect    = "Allow"
    resources = ["arn:aws:dynamodb:eu-west-1:816859564208:table/*"]

    actions = [
      "dynamodb:PutItem",
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:Scan",
      "dynamodb:UpdateItem",
    ]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:dynamodb:eu-west-1:816859564208:table/FAST*"]
    actions   = ["dynamodb:Query"]
  }
}

resource "aws_iam_policy" "reverse_index_search_dynamodb_policy" {
  name        = "ReverseIndexSearchDynamoDBPolicy"
  path        = "/service-role/"
  description = "IAM policy for DynamoDB of reverse_index_search"
  policy      = data.aws_iam_policy_document.reverse_index_search_dynamodb_policy.json
}

resource "aws_iam_role" "reverse_index_search_role" {
  name               = "FAST-Resources_Reverse-Index_Search_Role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  path               = "/service-role/"
  managed_policy_arns = [
    aws_iam_policy.reverse_index_search_cloudwatch_policy.arn,
    aws_iam_policy.reverse_index_search_dynamodb_policy.arn
  ]
}

data "archive_file" "fast_resources_search_archive" {
  type        = "zip"
  source_file = "${path.module}/../search_lambda/lambda_function.py"
  output_path = "${path.module}/fast_resources_reverse_index_search.zip"
}

resource "aws_lambda_function" "fast_resources_search_lambda" {
  filename         = data.archive_file.fast_resources_search_archive.output_path
  function_name    = "FAST-Resources_Reverse-Index"
  description      = "A simple backend (read/write to DynamoDB) with a RESTful API endpoint using Amazon API Gateway."
  role             = aws_iam_role.reverse_index_search_role.arn
  handler          = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.fast_resources_search_archive.output_base64sha256
  runtime          = "python3.7"
  memory_size      = 512
  timeout          = 10
}

resource "aws_api_gateway_integration" "fast_resources_search_integration_GET" {
  rest_api_id             = aws_api_gateway_rest_api.fast_resources_search_api.id
  resource_id             = aws_api_gateway_resource.reverse_index.id
  http_method             = aws_api_gateway_method.reverse_index_GET.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.fast_resources_search_lambda.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
}

resource "aws_api_gateway_integration" "fast_resources_search_integration_OPTIONS" {
  rest_api_id = aws_api_gateway_rest_api.fast_resources_search_api.id
  resource_id = aws_api_gateway_resource.reverse_index.id
  http_method = aws_api_gateway_method.reverse_index_OPTIONS.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = jsonencode(
      {
        statusCode = 200
      }
    )
  }
}

resource "aws_api_gateway_resource" "reverse_index_trigger" {
  rest_api_id = aws_api_gateway_rest_api.fast_resources_search_api.id
  parent_id   = aws_api_gateway_rest_api.fast_resources_search_api.root_resource_id
  path_part   = "FAST_Resources_Reverse_Index_Trigger"
}

resource "aws_api_gateway_method" "reverse_index_trigger_ANY" {
  rest_api_id      = aws_api_gateway_rest_api.fast_resources_search_api.id
  resource_id      = aws_api_gateway_resource.reverse_index_trigger.id
  http_method      = "ANY"
  authorization    = "NONE"
  api_key_required = true
}

resource "aws_api_gateway_method" "reverse_index_trigger_OPTIONS" {
  rest_api_id   = aws_api_gateway_rest_api.fast_resources_search_api.id
  resource_id   = aws_api_gateway_resource.reverse_index_trigger.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}


resource "aws_api_gateway_deployment" "fast_resources_search_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.fast_resources_search_api.id

  triggers = {
    redeployment = data.archive_file.fast_resources_search_archive.output_base64sha256
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "fast_resources_search_api_default_stage" {
  deployment_id = aws_api_gateway_deployment.fast_resources_search_api_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.fast_resources_search_api.id
  stage_name    = "default"
}

resource "null_resource" "reverse_index_search_archive_delete" {
  depends_on = [aws_lambda_function.fast_resources_search_lambda]
  triggers = {
    file_hash = data.archive_file.fast_resources_search_archive.output_base64sha256
  }
  provisioner "local-exec" {
    command = <<EOT
      rm -rf fast_resources_reverse_index_search.zip
    EOT
  }
}
