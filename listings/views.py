import django_filters
from rest_framework import generics, serializers, filters, pagination, response
from models import House
from collections import OrderedDict

'''
Paginate in a GeoJSON compatible format
'''
class FeatureCollectionPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return response.Response(
            OrderedDict(
                [
                    ('type', 'FeatureCollection'),
                    ('count', self.page.paginator.count),
                    ('next', self.get_next_link()),
                    ('previous', self.get_previous_link()),
                    ('features', data)
                ]
            )
        )

'''
Serialize house info in a GeoJSON compatible format
'''
class FeatureSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        return OrderedDict(
            [
                ('type', 'Feature'),
                ('geometry', {
                    'type': 'Point',
                    'coordinates': [
                        obj.lat,
                        obj.lng,
                    ]
                }),
                ('properties', {
                    'id': obj.id,
                    'street': obj.street,
                    'status': obj.status,
                    'price': obj.price,
                    'bedrooms': obj.bedrooms,
                    'bathrooms': obj.bathrooms,
                    'sq_ft': obj.sq_ft,
                })
            ]
        )

'''
Filter house info based on parameters provided in URL
'''
class HouseFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(name="price", lookup_type='gte')
    max_price = django_filters.NumberFilter(name="price", lookup_type='lte')
    min_bed = django_filters.NumberFilter(name="bedrooms", lookup_type='gte')
    max_bed = django_filters.NumberFilter(name="bedrooms", lookup_type='lte')
    min_bath = django_filters.NumberFilter(name="bathrooms", lookup_type='gte')
    max_bath = django_filters.NumberFilter(name="bathrooms", lookup_type='lte')
    class Meta:
        model = House
        fields = [
            'min_price',
            'max_price',
            'min_bed',
            'max_bed',
            'min_bath',
            'max_bath'
        ]

'''
API endpoint to query house info based on parameters provided in URL, and
return them in a GeoJSON compatible format
'''
class HouseList(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = FeatureSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = HouseFilter
    pagination_class = FeatureCollectionPagination
