FROM node:20-slim

# Instal Python dan dependensi sistem yang diperlukan
RUN apt-get update && apt-get install -y python3 python3-pip git curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Salin package dependencies
COPY package*.json ./
RUN npm install

# Instal global CLI kart dan binance-agentic-wallet
RUN npm install -g @binance/agentic-wallet agent-cards

# Salin seluruh file proyek ke dalam container
COPY . .

# Ekspos port untuk web service / express
EXPOSE 3000

# Perintah untuk menjalankan server WhatsApp
CMD ["node", "server.js"]