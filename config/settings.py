# settings.py

SOURCE_LANG = 'fr'
TARGET_LANG = 'th'

DO_NOT_TRANSLATE_KEYS = [
    "ListItem_schema", "author", "brand", "dateCreated", "datePublished",
    "dateModified", "imageUrl", "copyrightNotice", "acquireLicensePage",
    "license", "creditText", "url", "foundingDate", "productID",
    "googleClientId", "twitterId"
    # ลบ "full_href" ออกจากรายการนี้
]
