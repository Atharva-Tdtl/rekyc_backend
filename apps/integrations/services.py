import random

class MockGovIntegrationService:
    def pan_verify(self, pan, name=''):
        valid=bool(pan) and len(pan)>=10
        return {'provider':'PAN_API','pan':pan,'name_match_score':round(random.uniform(0.82,0.99),2),'valid':valid}
    def aadhaar_offline_verify(self, aadhaar_last4, name=''):
        return {'provider':'AADHAAR_OFFLINE_XML','aadhaar_last4':aadhaar_last4,'name_match_score':round(random.uniform(0.80,0.98),2),'valid':bool(aadhaar_last4)}
    def ckyc_search(self, customer):
        return {'provider':'CKYC','ckyc_number':f'CKYC{customer.id:08d}','found': customer.id % 2 == 0,'status':'ACTIVE'}
    def digilocker_fetch(self, customer):
        return {'provider':'DIGILOCKER','documents':['AADHAAR','PAN'] if customer.pan else ['AADHAAR'],'consent':'MOCK_GRANTED'}
service=MockGovIntegrationService()
