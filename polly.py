import main
import time
import boto3
import time
import yaml
from boto3.session import Session

with open(r'aws_key.yaml') as file_aws:
    lista_aws = yaml.full_load(file_aws)
    file_aws.close()

def cliente():
    polly_client = boto3.Session(
        aws_access_key_id=lista_aws["access_key_id"],
        aws_secret_access_key=lista_aws["secret_access_key"],
        region_name='us-east-1').client("polly")
    return polly_client


def sessionS3():
    session = Session(aws_access_key_id=lista_aws["access_key_id"],
                      aws_secret_access_key=lista_aws["secret_access_key"],
                      region_name='us-east-1')
    s3 = session.resource('s3')
    return s3

def delete(my_bucket, name_file):
    respuesta = my_bucket.delete_objects(Bucket=lista_aws["buckets"],
                                        Delete={'Objects': [{'Key': name_file}]})
    return respuesta

def descargar(taskId, word):    
    s3 = sessionS3()
    my_bucket = s3.Bucket(lista_aws["buckets"])

    print("Descargando elemento...")

    my_bucket.download_file(taskId, "{}{}".format(
        lista_aws["root"], word))
    print("Descarga completada")

def status(taskId, word):
    statu = {'scheduled': "en peticion", 'inProgress': "en proceso",
                    'completed': "generado", 'failed': "fallido"}

    generado = statu["completed"]      
    estado   = statu["scheduled"]   
    while estado != generado:
        try:
            polly_client = cliente()
            task_status = polly_client.get_speech_synthesis_task(TaskId=taskId)
            s = task_status["SynthesisTask"]["TaskStatus"]
            estado =  statu[s]
            print("Espera el audio se está {}, puede tomar unos segundos".format(estado))
            print("Audio " + estado)
            time.sleep(5)

        except:
            polly_tarea(word)
    
    if generado:
        s3 = sessionS3()
        my_bucket = s3.Bucket(lista_aws["buckets"])
        descargar(taskId + ".mp3", word)
        delete(my_bucket, taskId + ".mp3")

def polly_tarea(word):
    polly_client = cliente()

    response = polly_client.start_speech_synthesis_task(
        Engine='neural',
        LanguageCode='en-US',
        OutputS3BucketName=lista_aws["buckets"],
        OutputFormat='mp3',
        SampleRate='24000',
        VoiceId='Salli',
        Text=word)

    taskId = response['SynthesisTask']['TaskId']
    print("Task id is {} ".format(taskId))
    status(taskId, word)

def generate_sound(word):
    polly_tarea(word)


