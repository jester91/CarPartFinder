variable "environment" {
  description = "The name of the environment, mostly used as a suffix."
  type        = string
}

variable "location" {
  description = "The Azure Region in which all resources will be created."
  type        = string
  default     = "westeurope"
}

variable "resource_group_name" {
  description = "The resource group UserGW is deployed in"
}

variable "TFFAppServiceSkuSize" {
  description = "SKU size of App service plan"
}


variable "TFFAppServiceSkuTier" {
  description = "SKU tier of App service plan"
}

