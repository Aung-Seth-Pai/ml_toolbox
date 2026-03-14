# Use Node.js 24 image based on Alpine Linux as the base image for the container
FROM node:24-alpine
# Set the working directory in the container to /app
WORKDIR /app

# Copy the package.json file to the working directory
COPY package.json ./

# Install the dependencies specified in package.json, but only the production dependencies
RUN npm install --only=production

# Copy the source code from the local src directory to the working directory in the container
COPY src/ .

# Expose port 3000 to allow external access to the application running inside the container
EXPOSE 3000

# Set the default command to run the application using npm start, which will execute the start script defined in package.json
CMD ["node", "server.js"]