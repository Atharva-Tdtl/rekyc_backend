from .models import WorkflowCase
def create_case_for_customer(customer, user=None):
    priority='HIGH' if customer.risk_category=='HIGH' else 'MEDIUM'
    return WorkflowCase.objects.create(customer=customer,title=f'KYC Review - {customer}',status='OPEN',priority=priority,maker=user)
