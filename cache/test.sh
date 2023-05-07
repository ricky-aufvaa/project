#!/bin/bash

# Set the URL of the webpage to scrape
url="tmp.html"
#url="https://www.goodreads.com/book/show/17400657-khushwantnama"

# Set the ID and class of the HTML element to scrape
id="data-testid="
class="Formatted"

# Use curl to fetch the HTML content of the webpage and store it in a variable
html=$(cat $url)

# Use sed to extract the HTML content within the ID
id_content=$(echo "$html" | sed -n "/id=\"$id\"/,/\/$id/p")
echo $id_content

# Use grep to extract the content of the class within the ID
class_content=$(echo "$id_content" | grep -oP "(?<=<div class=\"$class\">)[^<]+")

# Print the content of the class
echo "$class_content"

