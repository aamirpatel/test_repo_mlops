FROM public.ecr.aws/lambda/python:3.10

# Set working directory inside container
WORKDIR /var/task

# Install system packages and Python dependencies
RUN yum install -y \
    git \
    curl \
    && yum clean all

# Copy requirements and installs
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all source files
COPY . .

CMD ["app.lambda_handler"]