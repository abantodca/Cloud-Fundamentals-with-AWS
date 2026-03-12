import boto3
import os

# Initialize the SNS client
sns_client = boto3.client(
    'sns',
    region_name=os.getenv('AWS_REGION')  # Optional, depending on your region
)

# SNS Topic ARN (replace with your actual SNS Topic ARN)
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')

# Ensure that SNS_TOPIC_ARN is set
if not SNS_TOPIC_ARN:
    raise ValueError("SNS_TOPIC_ARN is not set or is invalid.")

def send_sns_notification(user_name, user_position, resume_url, user_experience, user_ctc, user_expected_ctc, user_phone_number):
    """
    Sends a notification to an SNS Topic with the provided user details.
    """
    # Construct the SNS message body
    sns_message_body = (
        f"🔔 Nueva notificacion de aplicacion recibida\n"
        f"{'='*45}\n\n"
        f"Se ha enviado una nueva solicitud de empleo a traves del portal de Careers.\n\n"
        f"👤 Datos del candidato:\n"
        f"  - Nombre:        {user_name}\n"
        f"  - Posicion:      {user_position}\n"
        f"  - Experiencia:   {user_experience} años\n"
        f"  - CTC actual:    {user_ctc}\n"
        f"  - CTC esperado:  {user_expected_ctc}\n"
        f"  - Telefono:      {user_phone_number}\n\n"
        f"📄 Curriculum vitae:\n"
        f"  {resume_url}\n\n"
        f"{'='*45}\n"
        f"Este mensaje fue generado automaticamente por el sistema de Careers."
    )

    # Construct the SNS message subject
    sns_subject = f"[Careers] Nueva aplicacion de {user_name} para {user_position}"

    # Publish the message to SNS (raises exception on failure)
    response = sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=sns_message_body,
        Subject=sns_subject
    )
    message_id = response.get('MessageId')
    print(f"Notification sent to SNS for {user_name} applying for {user_position}. MessageId: {message_id}")
    return message_id