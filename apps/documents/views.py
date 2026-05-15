from rest_framework import viewsets, decorators, response
from .models import KYCDocument
from .serializers import KYCDocumentSerializer
from .services import mock_ocr_extract
from apps.audit.services import log_action
class KYCDocumentViewSet(viewsets.ModelViewSet):
    queryset=KYCDocument.objects.select_related('customer').all().order_by('-uploaded_at'); serializer_class=KYCDocumentSerializer
    def perform_create(self, serializer):
        obj=serializer.save(file_name=getattr(serializer.validated_data.get('file'),'name',''))
        log_action('DOCUMENT_UPLOADED', obj, self.request.user, after=KYCDocumentSerializer(obj).data, request=self.request)
    @decorators.action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        doc=self.get_object(); data=mock_ocr_extract(doc); log_action('DOCUMENT_PROCESSED', doc, request.user, after=data, request=request)
        return response.Response({'status':doc.status,'extracted_data':data,'confidence':doc.confidence})
