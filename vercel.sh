cp main.go ./dist/api/index.go
sed -i 's/package main/package handler/g' ./dist/api/index.go
cp ./static/* ./dist/