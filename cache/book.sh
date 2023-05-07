#!/bin/bash

# Get the title of the book from the user
read -p "Enter the title of the book: " title

# URL encode the book title
encoded_title=$(echo "$title" | sed 's/ /%20/g')

# Scrape the review of the book from Goodreads
review=$(curl -s "https://www.goodreads.com/search?q=$encoded_title" | grep -oP '(?<=<span class="minirating">\n\s+)[^<]+')

# Check if the review was found
if [[ -n "$review" ]]; then
    echo "Review of \"$title\":"
    echo "$review"
else
    echo "Review not found for \"$title\""
fi

