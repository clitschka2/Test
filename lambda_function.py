import json

def lambda_handler(event, context):
    """
    Función Lambda de ejemplo que procesa eventos y retorna una respuesta
    """

    # Log del evento recibido
    print(f"Evento recibido: {json.dumps(event)}")

    # Extraer información del evento
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)

    # Procesamiento de ejemplo
    message = body.get('message', 'No message provided')

    # Respuesta
    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'success',
            'message': f'Procesado: {message}',
            'timestamp': context.request_id if context else 'local'
        })
    }

    return response
