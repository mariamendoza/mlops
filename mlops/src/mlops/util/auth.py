import os
from azureml.core.authentication import ServicePrincipalAuthentication

def get_service_principal():
  tenant_id = os.environ.get("TENANT_ID")
  service_principal_id = os.environ.get("SERVICE_PRINCIPAL_ID")
  service_principal_password = os.environ.get("SERVICE_PRINCIPAL_SECRET")

  return ServicePrincipalAuthentication(
    tenant_id=tenant_id,
    service_principal_id=service_principal_id,
    service_principal_password=service_principal_password)