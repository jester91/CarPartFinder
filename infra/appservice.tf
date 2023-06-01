locals {
  workers = 1
}
resource "azurerm_app_service_plan" "app_service_plan" {
  name                = "CarPartFinderPlan${var.environment}"
  location            = var.location
  resource_group_name = var.resource_group_name
  kind                = "Linux"
  reserved            = true

  sku {
    tier     = var.TFFAppServiceSkuTier
    size     = var.TFFAppServiceSkuSize
    capacity = 1
  }
  maximum_elastic_worker_count = local.workers
}

resource "azurerm_app_service" "CarPartFinder" {
  name                    = "CarPartFinder${var.environment}"
  location                = var.location
  resource_group_name     = var.resource_group_name
  app_service_plan_id     = azurerm_app_service_plan.app_service_plan.id
  client_affinity_enabled = true

  site_config {
    always_on                            = "true"
    health_check_path                    = "/actuator/health"
    acr_use_managed_identity_credentials = true
    linux_fx_version                     = "DOCKER|tffcr.azurecr.io/carpartfinder:latest"

  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_container_registry" "acr" {
  name                = "TFFCR"
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "Basic"
  admin_enabled       = true

}
