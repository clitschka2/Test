import json
from datadog_lambda.wrapper import datadog_lambda_wrapper
from datadog_lambda.metric import lambda_metric

@datadog_lambda_wrapper
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

    # Enviar métrica personalizada a Datadog (opcional)
    lambda_metric(
        metric_name="custom.lambda.invocations",
        value=1,
        tags=["environment:production", f"message_length:{len(message)}"]
    )

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
