from djapian      import space, Indexer, CompositeIndexer
from candy.models import Category, Product

class CategoryIndexer(Indexer):
	fields = [('title', 2), ('description', 2)]

class ProductIndexer(Indexer):
	fields = [('title', 10), ('description', 1)]
	
space.add_index(Category, CategoryIndexer, attach_as='indexer')
space.add_index(Product , ProductIndexer, attach_as='indexer')

complete_indexer = CompositeIndexer(Category.indexer, Product.indexer)
