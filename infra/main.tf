terraform {

  backend "azurerm" {}

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.34.0"
    }
  }
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}
locals {
  tags = {
    Env             = var.environment
    ApplicationName = "tff${var.environment}"
    ResourceGroup   = var.resource_group_name
    Service         = "Infra${var.environment}"
  }
}

