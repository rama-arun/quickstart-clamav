FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y

RUN python -m pip install --upgrade pip

RUN yum install amazon-linux-extras -y

# why the hell following is not working? AWS Bug!! Python3 doesn't recognize this package. https://forums.aws.amazon.com/thread.jspa?messageID=930259
RUN PYTHON=python2 amazon-linux-extras install epel -y

RUN yum install -y gcc gcc-c++ clamav clamd clamav-update 

RUN freshclam
    
COPY *.py ${LAMBDA_TASK_ROOT}/

COPY ./requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

RUN cd ${LAMBDA_TASK_ROOT}

RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt -t .

CMD [ "virus-scanner.lambda_handler" ]