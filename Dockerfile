# Use a minimal Debian-based image with Python 3.9
FROM python:3.9-slim-buster

# Set the working directory inside the container to /myportfolio
WORKDIR /myportfolio

# Copy only the requirements.txt to the container at the working directory
COPY requirements.txt .

# Install dependencies using pip3 - will only be installed again when it has changed (docker caching)
RUN pip3 install -r requirements.txt

# Copy the rest of the project files into the container at the working directory
COPY . .

# Specify the command that runs when a container is created from this image
CMD ["flask", "run", "--host=0.0.0.0"]

# Expose port 5000 from the container to the host
EXPOSE 5000