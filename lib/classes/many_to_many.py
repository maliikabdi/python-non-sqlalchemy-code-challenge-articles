class Article:
    all = []  # Class-level attribute to store all articles

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string and between 5 and 50 characters inclusive.")
        self.author = author  # Use property to validate type
        self.magazine = magazine  # Use property to validate type
        self._title = title
        Article.all.append(self)

        # Automatically update author and magazine
        author._articles.append(self)
        magazine._articles.append(self)

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise AttributeError("The title is immutable and cannot be modified.")

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise ValueError("Author must be an instance of the Author class.")
        self._author = value

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("The author's name is immutable and cannot be changed.")

    def articles(self):
        return self._articles

    def magazines(self):
        return list({article.magazine for article in self._articles})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        return list({article.magazine.category for article in self._articles}) or None


class Magazine:
    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category must be a non-empty string.")
        self._name = name
        self._category = category
        self._articles = []

        if not hasattr(Magazine, '_all_magazines'):
            Magazine._all_magazines = []
        Magazine._all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def articles(self):
        return self._articles

    def contributors(self):
        return list({article.author for article in self._articles})

    def article_titles(self):
        titles = [article.title for article in self._articles]
        return titles if titles else None

    def contributing_authors(self):
        author_count = {}
        for article in self._articles:
            author_count[article.author] = author_count.get(article.author, 0) + 1
        return [author for author, count in author_count.items() if count > 2] or None

    @classmethod
    def top_publisher(cls):
        return max(cls._all_magazines, key=lambda mag: len(mag._articles), default=None)


# Create authors
author1 = Author("Maliik salal")
author2 = Author("Ashow kamau")

# Create magazines
mag1 = Magazine("TechMag", "Technology")
mag2 = Magazine("HealthDigest", "Health")

# Create articles
article1 = Article(author1, mag1, "The Future of AI")
article2 = Article(author1, mag1, "The Impact of Quantum Computing")
article3 = Article(author2, mag2, "Healthy Living in 2024")
article4 = Article(author1, mag2, "Nutrition Facts 101")
article5 = Article(author2, mag1, "Robots in Surgery")

# Test methods
print("Author 1 Articles:", [article.title for article in author1.articles()])
print("Author 1 Magazines:", [mag.name for mag in author1.magazines()])
print("Author 1 Topic Areas:", author1.topic_areas())

print("Magazine 1 Articles:", [article.title for article in mag1.articles()])
print("Magazine 1 Contributors:", [author.name for author in mag1.contributors()])
print("Magazine 1 Article Titles:", mag1.article_titles())
print("Magazine 1 Contributing Authors:", [author.name for author in (mag1.contributing_authors() or [])])

print("Top Publisher:", Magazine.top_publisher().name if Magazine.top_publisher() else None)
