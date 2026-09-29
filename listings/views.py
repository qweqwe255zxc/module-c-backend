from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from config.utils import success, error
from . import models, serializers

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your views here.

class ListingListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req):
        sort_param = req.query_params.get('sort')
        match sort_param:
            case 'price_desc':
                sort = '-price'
            case 'price_asc':
                sort = 'price'
            case _:
                sort = None
        qs = models.Listing.objects.all()
        if sort:
            qs = qs.order_by(sort)
        s = serializers.ListingSerializer(qs, many=True, context={'request': req})
        return success(s.data)

    def post(self, req):
        s = serializers.ListingSerializer(data=req.data, context={'request': req})
        s.is_valid(raise_exception=True)
        s.save(owner=req.user)

        async_to_sync(get_channel_layer().group_send)('listings', {
            'type': 'listing.new',
            'listing': {**s.data, "is_mine": False}
        })

        return success(s.data, 201)


class MineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        qs = models.Listing.objects.filter(owner=req.user)
        s = serializers.ListingSerializer(qs, many=True, context={'request': req})
        return success(s.data)


class ListingDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, req, pk):
        obj = get_object_or_404(models.Listing, pk=pk)
        s = serializers.ListingSerializer(obj, context={'request': req})
        return success(s.data)

    def put(self, req, pk):
        obj = get_object_or_404(models.Listing, pk=pk)
        if obj.owner != req.user:
            raise PermissionDenied()
        s = serializers.ListingSerializer(obj, data=req.data, partial=True, context={'request': req})
        s.is_valid(raise_exception=True)
        s.save()
        return success(s.data, 200)

    def delete(self, req, pk):
        obj = get_object_or_404(models.Listing, pk=pk)
        if obj.owner != req.user:
            raise PermissionDenied()
        obj.delete()
        return Response(status=204)


class ListingContactView(APIView):
    def get(self, req, pk):
        obj = get_object_or_404(models.Listing, pk=pk)
        return Response({
            'email': obj.owner.email
        }, status=200)
