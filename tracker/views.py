from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from django.shortcuts import redirect
from tracker.models import Click, ShortURL
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
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
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    if short_url.thank_you_page:
        return redirect(short_url.thank_you_page)
    return redirect(short_url.original_url)


class ShortURLViewSet(viewsets.ModelViewSet):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

    @action(detail=True, methods=['patch'])
    def update_thank_you_page(self, request, pk=None):
        short_url = self.get_object()
        thank_you_page = request.data.get('thank_you_page')
        if thank_you_page:
            short_url.thank_you_page = thank_you_page
            short_url.save()
            return Response({'status': 'thank you page updated'})
        else:
            return Response({'error': 'thank you page not provided'}, status=status.HTTP_400_BAD_REQUEST)
