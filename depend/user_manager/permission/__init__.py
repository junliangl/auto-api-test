from .fund.funding import FundingPermissionService
from .fund.automated_withdrawal import AutomatedWithdrawalPermissionService
from .portal.agent_portal import AgentPortalPermissionService
from .portal.client_portal import ClientPortalPermissionService

funding_user_role = FundingPermissionService.user_role
funding_permission = FundingPermissionService.permission
automated_withdrawal_user_role = AutomatedWithdrawalPermissionService.user_role
automated_withdrawal_permission = AutomatedWithdrawalPermissionService.permission
agent_portal_user_role = AgentPortalPermissionService.user_role
client_portal_user_role = ClientPortalPermissionService.user_role