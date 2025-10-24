# AWS Lambda + GitHub Actions Pipeline

Este proyecto demuestra cómo desplegar una función Lambda de AWS usando GitHub Actions.

## 📋 Requisitos Previos

1. **Cuenta de AWS** con permisos para Lambda
2. **Función Lambda creada** en AWS (puedes crearla desde la consola)
3. **Credenciales de AWS** configuradas en GitHub Secrets

## 🔧 Configuración

### 1. Crear la función Lambda en AWS

Puedes usar el siguiente comando de AWS CLI o crear desde la consola:

```bash
aws lambda create-function \
  --function-name my-example-lambda \
  --runtime python3.11 \
  --role arn:aws:iam::TU_ACCOUNT_ID:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://lambda-deployment.zip
```

### 2. Configurar GitHub Secrets

Ve a tu repositorio → Settings → Secrets and variables → Actions y agrega:

- `AWS_ACCESS_KEY_ID`: Tu Access Key ID de AWS
- `AWS_SECRET_ACCESS_KEY`: Tu Secret Access Key de AWS
- `DATADOG_API_KEY`: Tu API Key de Datadog (para enviar DORA metrics)

### 3. Ajustar variables en el workflow

Edita [.github/workflows/deploy-lambda.yml](.github/workflows/deploy-lambda.yml):

```yaml
env:
  AWS_REGION: us-east-1  # Cambia a tu región
  LAMBDA_FUNCTION_NAME: my-example-lambda  # Cambia al nombre de tu función
  DATADOG_SITE: datadoghq.com  # Cambia si usas otro sitio (datadoghq.eu, etc)
```

## 🚀 Cómo Funciona

### Pipeline CI/CD

1. **Test Job**
   - Se ejecuta en cada push y PR
   - Instala dependencias
   - Ejecuta pruebas (puedes agregar pytest)

2. **Deploy Job**
   - Solo se ejecuta en push a `main`
   - Crea el paquete de deployment
   - Configura credenciales de AWS
   - Despliega a Lambda
   - Publica nueva versión
   - Envía métricas DORA a Datadog

### Trigger Manual

Puedes ejecutar el workflow manualmente:
1. Ve a Actions → Deploy to AWS Lambda
2. Click en "Run workflow"

## 📦 Estructura del Proyecto

```
.
├── lambda_function.py          # Código de la función Lambda
├── requirements.txt            # Dependencias Python
├── .github/
│   └── workflows/
│       └── deploy-lambda.yml  # Workflow de GitHub Actions
└── README-Lambda.md           # Esta documentación
```

## 🧪 Probar la Función Lambda

Después del deployment, prueba la función:

```bash
aws lambda invoke \
  --function-name my-example-lambda \
  --payload '{"body": "{\"message\": \"Hello Lambda\"}"}' \
  response.json

cat response.json
```

O desde la consola de AWS:
1. Ve a Lambda → Funciones → my-example-lambda
2. Tab "Test"
3. Crea un evento de prueba con:
```json
{
  "body": "{\"message\": \"Hello from AWS Console\"}"
}
```

## 🔒 Permisos IAM Necesarios

El rol de ejecución de Lambda necesita:
- `AWSLambdaBasicExecutionRole` (logs de CloudWatch)

El usuario de GitHub Actions necesita:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:UpdateFunctionCode",
        "lambda:PublishVersion",
        "lambda:GetFunction"
      ],
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:my-example-lambda"
    }
  ]
}
```

## 📝 Personalización

### Agregar Tests

Crea `tests/test_lambda.py`:

```python
import json
from lambda_function import lambda_handler

def test_lambda_handler():
    event = {'body': '{"message": "test"}'}
    context = None
    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['status'] == 'success'
```

Descomenta la línea de pytest en [deploy-lambda.yml](.github/workflows/deploy-lambda.yml#L34)

### Agregar más dependencias

Edita [requirements.txt](requirements.txt) y agrega las librerías que necesites.

## 🎯 Flujo de Trabajo

1. Haz cambios en `lambda_function.py`
2. Commit y push a una rama
3. Crea un Pull Request → Se ejecutan los tests
4. Merge a `main` → Se despliega automáticamente a Lambda
5. La nueva versión está disponible en AWS
6. Las métricas DORA se envían automáticamente a Datadog

## 📊 DORA Metrics en Datadog

El workflow envía automáticamente eventos de deployment a Datadog que se usan para calcular las métricas DORA:

- **Deployment Frequency**: Frecuencia de despliegues
- **Lead Time for Changes**: Tiempo desde commit hasta producción
- **Change Failure Rate**: Porcentaje de deployments que fallan
- **Mean Time to Recovery**: Tiempo promedio de recuperación

### Configuración de Datadog

1. Obtén tu API Key desde Datadog → Organization Settings → API Keys
2. Agrega el secret `DATADOG_API_KEY` en GitHub
3. Los deployments aparecerán en Datadog → Service Management → Deployments

### Personalizar el evento

Puedes modificar en [deploy-lambda.yml](.github/workflows/deploy-lambda.yml#L109):

```bash
datadog-ci dora deployment \
  --service ${{ env.LAMBDA_FUNCTION_NAME }} \
  --env production \  # Cambia el environment si necesitas
  --version ${{ steps.publish-version.outputs.version }}
```

## 🐛 Troubleshooting

- **Error de credenciales AWS**: Verifica que los secrets de AWS estén configurados
- **Error de credenciales Datadog**: Verifica que `DATADOG_API_KEY` esté configurado
- **Error de permisos**: Revisa que el usuario IAM tenga los permisos correctos
- **Función no existe**: Asegúrate de crear la función Lambda primero
- **Timeout**: Aumenta el timeout en la configuración de Lambda
- **Datadog-ci no envía métricas**: Verifica que `DATADOG_SITE` sea correcto para tu región

## 📚 Referencias

- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [AWS CLI Lambda Commands](https://docs.aws.amazon.com/cli/latest/reference/lambda/)
- [Datadog DORA Metrics](https://docs.datadoghq.com/dora_metrics/)
- [Datadog CI Documentation](https://github.com/DataDog/datadog-ci)
