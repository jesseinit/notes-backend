#!/bin/bash
# counter=$1
# # while [ $counter -le 10 ]

# # for value in $(seq 20)
# # for value in $(seq 2000000)
for value in $(seq 2000)
do
    curl --location --request POST 'https://notes.jesseinit.dev/v1/note' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEiLCJ1c2VybmFtZSI6ImJpbmdvbWFuIiwiZXhwIjoxNjcxNjQwNTczfQ.CgJtJESaTvvPZoUX7isG9yj9Uq_2e4wIDogEUSsX__0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Most of them just Envy",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris cursus mattis molestie a iaculis at erat pellentesque adipiscing"
}'
done
