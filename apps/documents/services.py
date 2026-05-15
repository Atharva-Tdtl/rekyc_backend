from django.utils import timezone
def mock_ocr_extract(doc):
    name=f'{doc.customer.first_name} {doc.customer.last_name}'.upper()
    base={'name':name,'address':doc.customer.current_address,'confidence':0.92}
    if doc.doc_type=='PAN': base.update({'pan':doc.customer.pan or 'ABCDE1234F','document_number':doc.customer.pan or 'ABCDE1234F'})
    elif doc.doc_type=='AADHAAR': base.update({'aadhaar_last4':doc.customer.aadhaar_last4 or '1234','document_number':'XXXX-XXXX-'+(doc.customer.aadhaar_last4 or '1234')})
    elif doc.doc_type=='BANK_STATEMENT': base.update({'avg_balance':125000,'salary_credits':6,'emi_bounces':0})
    else: base.update({'document_number':f'{doc.doc_type}-MOCK-001'})
    doc.extracted_data=base; doc.confidence=base['confidence']; doc.status='PROCESSED'; doc.processed_at=timezone.now(); doc.save()
    return base
