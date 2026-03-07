# Build stage
FROM gcc:13 AS build
WORKDIR /app
COPY . .
RUN cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build

# Run stage
FROM debian:bookworm-slim
WORKDIR /app
COPY --from=build /app/build/server .
EXPOSE 8080
CMD ["./server"]