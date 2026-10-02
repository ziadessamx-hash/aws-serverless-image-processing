provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "source" {
  bucket = "s3-source-image-uploads"
}

resource "aws_s3_bucket" "destination" {
  bucket = "s3-processed-images-output"
}

resource "aws_sqs_queue" "image_queue" {
  name                       = "s3-event-notification-queue"
  delay_seconds              = 0
  message_retention_seconds  = 86400
}

resource "aws_dynamodb_table" "metadata" {
  name         = "ImageMetadataTable"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ImageId"

  attribute {
    name = "ImageId"
    type = "S"
  }
}