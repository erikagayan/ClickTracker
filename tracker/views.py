from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from django.shortcuts import redirect
from tracker.models import Click, ShortURL
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from tracker.serializers import ClickSerializer, ShortURLSerializer
from django.shortcuts import get_object_or_404, redirect


class ClickViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer

    def create(self, request, *args, **kwargs):
        ip_address = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")
        project_id = request.data.get("project_id", "")
        thank_you_page = request.data.get("thank_you_page", "http://example.com/thank-you")

        click = Click.objects.create(
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=timezone.now(),
            project_id=project_id,
            thank_you_page=thank_you_page
        )
        click.save()

        return Response(status=status.HTTP_201_CREATED)

    def redirect(self, request, pk=None):
        try:
            click = Click.objects.get(pk=pk)
        except Click.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return redirect(click.thank_you_page)


def redirect_to_original(request, short_code):
    try:
        short_url = ShortURL.objects.get(short_code=short_code)
        print(f"Redirecting to {short_url.original_url}")
        return redirect(short_url.original_url)
    except ShortURL.DoesNotExist:
        return HttpResponse('Short URL not found', status=404)


class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
