read query
#query=$(printf "%s" "$*")
  if [[ $query == 1.jpg ]]; then
    echo "Scanning the book cover..."
  curl "https://www.goodreads.com/book/show/17400657-khushwantnama" > ./tmp.html
  echo "Here's a brief summary of this book:-"
  elif [[ $query == 2.jpg ]]; then
    echo "Scanning the book cover..."
  curl "https://www.goodreads.com/en/book/show/109250" > ./tmp.html
  echo "Here's a brief summary of this book:-"

  elif [[ $query == 3.jpg ]]; then
    echo "Scanning the book cover..."
   curl "https://www.goodreads.com/en/book/show/23395995" > ./tmp.html
  echo "Here's a brief summary of this book:-"
  fi
page="/$HOME/project/cache/tmp.html"
summary=$(cat $page |grep -Eo '<div data-testid="description" class="BookPageMetadataSection__description"><div class="TruncatedContent" tabindex="-1"><div class="TruncatedContent__text TruncatedContent__text--large" tabindex="-1" data-testid="contentContainer"><div class="DetailsLayoutRightParagraph"><div class="DetailsLayoutRightParagraph__widthConstrained"><span class="Formatted">.*</span></div></div></div><div class=""></div></div></div><div data-testid="genresList"' |sed 's/Formatted"/ /g'|sed 's/</ /g'|grep -Eo '" >.*/span'|tr -d '>'|sed 's/\///g'|sed 's/span//g')

echo $summary


