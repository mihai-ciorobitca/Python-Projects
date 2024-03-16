# CSS selectors

next_page = response.css('a[aria-label=Next]::attr(href)').get()
products = response.css('div.card-v2-wrapper.js-section-wrapper')
description = response.css('a.card-v2-title.semibold.mrg-btm-xxs.js-product-url::text').get()
price = response.css('p.product-new-price::text').get()
link = response.css('a.card-v2-title.semibold.mrg-btm-xxs.js-product-url::attr(href)').get()

