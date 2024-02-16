# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

rate = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
}


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)


        # Category and product type -> upper case to lower case

        category = adapter.get('category')
        adapter['category'] = category.lower()

        type = adapter.get('product_type')
        adapter['product_type'] = type.lower()

        # Price -> convert string to float
        keys = ['price_excl_tax','price_incl_tax','tax','price']
        for key in keys:
            value = adapter.get(key)
            value = value.replace('£','')
            adapter[key] = float(value)

        # Availability -> extract number of books in stock
        # In stock (19 available)
        availability = adapter.get('availability')
        split = availability.split('(')
        if len(split) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        stars = adapter.get('stars')
        split = stars.split(' ')
        value = split[1].lower()
        adapter['stars'] = rate[value]



        # Reviews -> convert string to number
        reviews = adapter.get('num_reviews')
        adapter['num_reviews'] = int(reviews)

        return item
