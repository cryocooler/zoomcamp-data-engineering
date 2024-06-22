variable "credentials" {
    description = "my credentials"
    default = "./keys/my-creds.json"
}

variable "project" {
    description = "Project"
    default = "piscine-427120"
}

variable "region" {
    description = "Region"
    default = "europe-north1-a"
}


variable "location" {
  description = "Project location"
  default     = "EU"

}

variable "bq_dataset_name" {
  description = "BigQuery Dataset name"
  default     = "demo_dataset"

}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "gcs_bucket_name" {
  description = "My storage bucket name"
  default     = "piscine-427120-terra-bucket"
}