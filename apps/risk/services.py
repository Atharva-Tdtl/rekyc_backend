from .models import RiskAssessment, WatchlistHit

def calculate_risk(customer):
    factors={}
    base=15
    if customer.customer_type=='NRI': base+=20; factors['nri_customer']=20
    if customer.income_monthly and customer.income_monthly>500000: base+=10; factors['high_income']=10
    if not customer.pan: base+=25; factors['missing_pan']=25
    docs=customer.documents.count();
    if docs<2: base+=20; factors['insufficient_documents']=20
    failed=customer.verification_checks.filter(status__in=['FAILED','REVIEW']).count()
    base+=failed*10; factors['verification_exceptions']=failed*10
    aml=min(base,100); fraud=min(10+failed*15+(0 if customer.pan else 30),100); overall=round((aml*0.55)+(fraud*0.45))
    category='LOW' if overall<35 else 'MEDIUM' if overall<70 else 'HIGH'
    if 'RISK' in (customer.last_name or '').upper(): WatchlistHit.objects.create(customer=customer,list_type='ADVERSE_MEDIA',matched_name=str(customer),confidence=0.82)
    customer.risk_score=overall; customer.risk_category=category; customer.save(update_fields=['risk_score','risk_category','updated_at'])
    return RiskAssessment.objects.create(customer=customer, aml_score=aml, fraud_score=fraud, overall_score=overall, category=category, factors=factors)

def fraud_detection(customer):
    flags=[]
    pans=list(type(customer).objects.filter(pan=customer.pan).exclude(id=customer.id).values_list('id',flat=True)) if customer.pan else []
    if pans: flags.append({'type':'DUPLICATE_PAN','severity':'HIGH','linked_customer_ids':pans})
    if customer.documents.filter(confidence__lt=0.75).exists(): flags.append({'type':'LOW_OCR_CONFIDENCE','severity':'MEDIUM'})
    if not flags: flags.append({'type':'NO_CRITICAL_FRAUD_SIGNAL','severity':'LOW'})
    return {'customer_id':customer.id,'flags':flags,'recommendation':'EDD_REQUIRED' if any(f['severity']=='HIGH' for f in flags) else 'STANDARD_REVIEW'}
