#!/bin/bash
counter=$1
# while [ $counter -le 10 ]

# for value in $(seq 20)
for value in $(seq 2000000)
do
    curl --location --request POST 'http://localhost:8023/v1/note' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZmU4Yjg2LWU5NjctNDdmZS1iNDg4LTk2ZWIyNDMwMzFjNyIsInVzZXJuYW1lIjoiYmluZ29tYW4iLCJleHAiOjE2Njg4NjUxMDV9.jsN97d9KPuwfL6eV-taT2aOWd53aoiQIImJXCtc9Vqc' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Most of them just Envy",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mauris cursus mattis molestie a iaculis at erat pellentesque adipiscing. Tortor consequat id porta nibh venenatis cras sed. Urna id volutpat lacus laoreet non curabitur gravida arcu. Fermentum leo vel orci porta non pulvinar neque. Viverra tellus in hac habitasse platea dictumst vestibulum. Pulvinar sapien et ligula ullamcorper malesuada. Est pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus."
}'
done

