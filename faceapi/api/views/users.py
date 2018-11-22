from rest_framework import response
from rest_framework.generics import CreateAPIView

from ..serialisers import UsersLabelSerializer
from ..models import (
    FacebookLabel,
    FacebookPage,
)
from utils import (
    create_label,
    label_users,
)


__all__ = (
    'LabelUsersView',
)


class LabelUsersView(CreateAPIView):

    serializer_class = UsersLabelSerializer

    http_method_names = ['post', 'options']

    def post(self, request, *args, **kwargs):
        """
        Set user's labels
        """
        page_id = kwargs['page_id']
        page = FacebookPage.objects.filter(id=page_id).first()
        if page is None:
            return response.Response(
                {'error': f'Cannot get page with id {page_id}'},
                status=404
            )
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request}
        )
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=403)
        data = serializer.data
        users = data['user_ids']
        label = data['label']
        stored_label = FacebookLabel.objects.filter(label=label).first()
        if stored_label is None:
            label_id = create_label(page.access_token, label)
            if label_id is None:
                return response.Response(
                    {'error': f'Cannot create custom label {label}'},
                    status=400
                )
            FacebookLabel.objects.create(
                label_id=label_id,
                label=label,
                page=page,
            )
        else:
            label_id = stored_label.label_id
        responses = list(label_users(
            access_token=page.access_token,
            label_id=label_id,
            *users,
        ))
        return response.Response({'results': responses}, status=200)
