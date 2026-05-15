from .models import VerificationCheck
from apps.integrations.services import service

def run_identity(customer):
    pan=service.pan_verify(customer.pan, str(customer)); aad=service.aadhaar_offline_verify(customer.aadhaar_last4, str(customer)); ckyc=service.ckyc_search(customer)
    score=round((pan['name_match_score']+aad['name_match_score']+(0.95 if ckyc['found'] else 0.75))/3,2)
    status='PASSED' if score>=0.85 and pan['valid'] else 'REVIEW'
    return VerificationCheck.objects.create(customer=customer, check_type='IDENTITY', status=status, score=score, evidence={'pan':pan,'aadhaar':aad,'ckyc':ckyc})

def run_address(customer):
    has_addr=bool(customer.current_address and len(customer.current_address)>10)
    score=0.9 if has_addr else 0.45
    status='PASSED' if score>=0.75 else 'REVIEW'
    evidence={'geo_tag':'18.5204,73.8567','method':'document+geo mock','address_length':len(customer.current_address or '')}
    return VerificationCheck.objects.create(customer=customer, check_type='ADDRESS', status=status, score=score, evidence=evidence)

def trigger_field(customer, reason='Address requires physical verification'):
    return VerificationCheck.objects.create(customer=customer, check_type='FIELD', status='PENDING', score=0, remarks=reason, evidence={'assigned':'field_agent'})
