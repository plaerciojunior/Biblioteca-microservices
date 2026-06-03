# Stage 1: Build Tailwind CSS
FROM node:20-slim AS tailwind-build
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npx tailwindcss -i ./wwwroot/css/app.css -o ./wwwroot/css/tailwind.css

# Stage 2: Build Blazor App
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ["BibliotecaMicroservice.csproj", "./"]
RUN dotnet restore "BibliotecaMicroservice.csproj"
COPY . .
COPY --from=tailwind-build /app/wwwroot/css/tailwind.css ./wwwroot/css/tailwind.css
RUN dotnet build "BibliotecaMicroservice.csproj" -c Release -o /app/build

# Stage 3: Publish
FROM build AS publish
RUN dotnet publish "BibliotecaMicroservice.csproj" -c Release -o /app/publish

# Stage 4: Serve with Nginx
FROM nginx:alpine AS final
WORKDIR /usr/share/nginx/html
COPY --from=publish /app/publish/wwwroot .
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80