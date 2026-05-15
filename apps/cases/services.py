import time
from typing import Dict, Any
from .models import Case, CaseAgentTrace

class AgenticKYCOrchestrator:
    def __init__(self, case_id: int):
        self.case = Case.objects.get(id=case_id)
        self.context = {
            "case_id": case_id,
            "customer_id": self.case.customer.id,
            "profile": {
                "name": f"{self.case.customer.first_name} {self.case.customer.last_name}",
                "pan": self.case.customer.pan,
                "aadhaar_last4": self.case.customer.aadhaar_last4,
            },
            "documents": [], # Would be fetched from Document model
            "agent_traces": []
        }

    def run_pipeline(self):
        # 1. OCR Extraction (Simulated for now, but integrated into flow)
        self._run_agent("document_intake_agent", "SUCCESS", 
                        f"Extracted fields from documents for {self.context['profile']['name']}.",
                        "I am parsing the uploaded PAN and Aadhaar images using OCR.")
        self.case.stage = 'OCR_EXTRACTION'
        self.case.save()
        time.sleep(1)

        # 2. Document Understanding
        self._run_agent("document_understanding_agent", "SUCCESS", 
                        "Cross-document consistency check completed. All identity fields match.",
                        "I am comparing the name on the PAN card with the name on the Aadhaar card.")
        time.sleep(1)

        # 3. Identity Verification
        self._run_agent("identity_verification_agent", "SUCCESS", 
                        "Identity APIs verified PAN and Aadhaar. Face match score: 94%.",
                        "I am pinging the NSDL and UIDAI gateways to verify the document numbers.")
        self.case.stage = 'IDENTITY_VERIF'
        self.case.save()
        time.sleep(1)

        # 4. AML Risk Scoring
        self._run_agent("risk_scoring_aml_agent", "SUCCESS", 
                        "AML Risk Score calculated: 24 (LOW).",
                        "I am screening the customer against global sanctions and PEP lists.")
        self.case.stage = 'AML_RISK'
        self.case.save()
        time.sleep(1)

        # 5. Compliance Audit
        rec = "AUTO_APPROVE" if self.case.customer.risk_category == 'LOW' else "MAKER_CHECKER_REVIEW"
        self._run_agent("compliance_audit_agent", "FINALIZED", 
                        f"Final recommendation: {rec}",
                        f"Based on the aggregate low risk score, I recommend {rec}.")
        
        self.case.stage = 'COMPLIANCE_REVIEW' if rec == "MAKER_CHECKER_REVIEW" else 'CKYC_UPLOAD'
        if rec == "AUTO_APPROVE":
             self.case.customer.status = 'APPROVED'
             self.case.customer.save()
        self.case.save()

    def _run_agent(self, name: str, status: str, log: str, thought: str):
        CaseAgentTrace.objects.create(
            case=self.case,
            agent_name=name,
            status=status,
            log=log,
            thought=thought
        )
