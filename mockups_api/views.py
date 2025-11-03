from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from customic.settings import REST_FRAMEWORK

from rest_framework.permissions import IsAuthenticated


from .serializer import MockupTaskGenerateBodySerializer
from .serializer import MockupTaskGenerateResponseSerializer
from .serializer import MockupTaskGetResponseSerializer
from .serializer import MockupGetSerializer

from .models import MockupTask, Mockup

from .tasks import make_mockup_image


class MockupTaskGenerateView(APIView):
    @extend_schema(
        request=MockupTaskGenerateBodySerializer,
        responses={201: MockupTaskGenerateResponseSerializer},
        description="Making new mockup",
    )
    def post(self, request):
        body_serializer = MockupTaskGenerateBodySerializer(data=request.data)
        if body_serializer.is_valid():
            task = body_serializer.save(
                status="PENDING",  # TODO: Fix Magic string
                message="ساخت تصویر آغاز شد",  # TODO: Fix magic string
            )
            make_mockup_image.delay(task.task_id)
            response_serializer = MockupTaskGenerateResponseSerializer(task)
            return Response(response_serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class MockupTaskDetailView(RetrieveAPIView):
    queryset = MockupTask.objects.all()
    serializer_class = MockupTaskGetResponseSerializer
    lookup_field = "task_id"


# This is for removing extra data from GET /api/mockups/ Response.
class MakePagination(PageNumberPagination):
    page_size = REST_FRAMEWORK["PAGATION_PAGE_SIZE"]

    def get_paginated_response(self, data):
        return Response(data)


class MockupListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Mockup.objects.all().order_by("-created_at")
    serializer_class = MockupGetSerializer
    filter_backends = [SearchFilter]
    # simple search
    search_fields = ["text", "font", "shirt_color"]
    # pagination_class = PageNumberPagination
    pagination_class = MakePagination
