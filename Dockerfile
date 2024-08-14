# Use the required version of the Playwright image
FROM mcr.microsoft.com/playwright:v1.46.0-focal

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Set the entry point to the start.sh script
ENTRYPOINT ["./start.sh"]