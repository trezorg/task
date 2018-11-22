import json
import logging
from typing import (
    Optional,
    Dict,
    Iterable
)

import requests

logger = logging.getLogger(__name__)


VERSION = '3.2'


__all__ = (
    'create_label',
    'batch_request',
    'label_users',
)


def create_label(access_token: str, label: str) -> Optional[str]:
    session = requests.Session()
    headers = {'Content-Type': 'application/json'}
    url = (f'https://graph.facebook.com/v{VERSION}/me/'
           f'custom_labels?access_token={access_token}')
    response = session.post(
        url,
        headers=headers,
        data={'name': label}
    )
    if response.status_code >= 400:
        logging.error(
            f'Cannot add custom label. '
            f'Status code: {response.status_code} '
            f'Response: {response.content}'
        )
        return
    data = response.json()
    return data['id']


def batch_request(access_token: str, *reqs: Dict) -> Iterable[Dict]:
    session = requests.Session()
    batch = {'batch': [req for req in reqs]}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'access_token': access_token, **batch}
    response = session.post(
        'https://graph.facebook.com',
        headers=headers,
        data=data
    )
    if response.status_code >= 400:
        logging.error(
            f'Cannot make bulk request. '
            f'Status code: {response.status_code} '
            f'Response: {response.content}'
        )
        yield from ()
        return
    data = response.json()
    return (
        json.loads(resp['body']) if resp['status'] == 200 else None
        for resp in data
    )


def label_users(access_token: str, label_id: str, *user_id: str):
    relative_url = f'{VERSION}/{label_id}/label?access_token={access_token}'
    yield from batch_request(
        access_token=access_token,
        *(
            {
                'method': 'POST',
                'relative_url': relative_url,
                'body': json.dumps({'user': u_id}),
            } for u_id in user_id
        )
    )
