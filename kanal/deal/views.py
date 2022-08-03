from rest_framework import generics
from deal.models import Deal
from deal.serialaizers import DealSerializer


class DealListView(generics.ListAPIView):
    queryset = Deal.objects.all().order_by('table_id')
    serializer_class = DealSerializer
