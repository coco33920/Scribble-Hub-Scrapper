<h1 align="center">Welcome to Scribble Hub Scrapper 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.01-blue.svg?cacheSeconds=2592000" />
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/coco33920" target="_blank">
    <img alt="Twitter: coco33920" src="https://img.shields.io/twitter/follow/coco33920.svg?style=social" />
  </a>
</p>

> Little scrapper to use instead of a real API for Scribble Hub very WIP!!

## Currently implemented

### Book API
The book API is WIP, currently there is some informations and stats, usage:
```python
    import scribblehubapi as api

    book = api.Book(id) #the id must be an integer and is the id of the book
    book.name() #return the name of the book
    book.extract_infos() #return the informations ok the books, namely : author name, author profil page link
    #the permalink of the book, the title of the book, the status (ongoing,etc.)
    #the tag list, genre list, views, reader, favorites, chapters and chapters/week
    
    book.extract_stats() #return basic stats of the books, namely : average views, average words
    #pages, total views (All), total views (Chapters), and word count

```

### Todo
* Expand the book API (chapters list etc.)
* Add an author API
* Trending ? Search ?
* Implementing the API in a flask app and/or discord bot


## Author

👤 **Charlotte T.**

* Twitter: [@coco33920](https://twitter.com/coco33920)
* Github: [@coco33920](https://github.com/coco33920)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_