APP_NAME = "Microsoft Graph CLI"
DEFAULT_AUTHORITY_HOST = "https://login.microsoftonline.com"
DEFAULT_GRAPH_HOST = "https://graph.microsoft.com"
DEFAULT_SCOPE = "https://graph.microsoft.com/.default"
DEFAULT_VERSION = "v1.0"
ENV_ACCESS_TOKEN = "MSGRAPH_ACCESS_TOKEN"

ENDPOINTS = [
    {"key": "me", "method": "GET", "path": "/me", "category": "identity", "scope": "User.Read", "description": "Signed-in user profile."},
    {"key": "users", "method": "GET", "path": "/users", "category": "identity", "scope": "User.Read.All", "description": "Tenant users."},
    {"key": "user", "method": "GET", "path": "/users/{id}", "category": "identity", "scope": "User.Read.All", "description": "Single user by object ID or UPN."},
    {"key": "groups", "method": "GET", "path": "/groups", "category": "identity", "scope": "Group.Read.All", "description": "Tenant groups."},
    {"key": "devices", "method": "GET", "path": "/devices", "category": "identity", "scope": "Device.Read.All", "description": "Entra ID devices."},
    {"key": "managed-devices", "method": "GET", "path": "/deviceManagement/managedDevices", "category": "intune", "scope": "DeviceManagementManagedDevices.Read.All", "description": "Intune managed devices."},
    {"key": "managed-device", "method": "GET", "path": "/deviceManagement/managedDevices/{id}", "category": "intune", "scope": "DeviceManagementManagedDevices.Read.All", "description": "Single Intune managed device."},
    {"key": "mobile-apps", "method": "GET", "path": "/deviceAppManagement/mobileApps", "category": "intune", "scope": "DeviceManagementApps.Read.All", "description": "Intune mobile apps."},
    {"key": "compliance-policies", "method": "GET", "path": "/deviceManagement/deviceCompliancePolicies", "category": "intune", "scope": "DeviceManagementConfiguration.Read.All", "description": "Intune compliance policies."},
    {"key": "configuration-policies", "method": "GET", "path": "/deviceManagement/deviceConfigurations", "category": "intune", "scope": "DeviceManagementConfiguration.Read.All", "description": "Intune device configuration policies."},
    {"key": "sign-ins", "method": "GET", "path": "/auditLogs/signIns", "category": "audit", "scope": "AuditLog.Read.All", "description": "Entra ID sign-in audit logs."},
    {"key": "organization", "method": "GET", "path": "/organization", "category": "tenant", "scope": "Organization.Read.All", "description": "Tenant organization metadata."},
    {"key": "subscribed-skus", "method": "GET", "path": "/subscribedSkus", "category": "tenant", "scope": "Organization.Read.All", "description": "Tenant license SKUs."},
    {"key": "service-health", "method": "GET", "path": "/admin/serviceAnnouncement/healthOverviews", "category": "health", "scope": "ServiceHealth.Read.All", "description": "Microsoft 365 service health overview."},
]

ENDPOINT_BY_KEY = {item["key"]: item for item in ENDPOINTS}
