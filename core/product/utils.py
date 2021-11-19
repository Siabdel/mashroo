
# Il faudra cependant vous assurez que l'item product_item a bien été sauvegardé en base auparavant:

product_item.save()
product_item.attributes.add(attribute1)

i1 = ProductItem.objects.get(pk=1)
# Tshirt [5046]
a1 = ProductAttributeValue.objects.get(pk=1)
# bleu [couleur]

ProductAttributeValue.objects.all()
# [<ProductAttributeValue: bleu [couleur]>, <ProductAttributeValue: jaune [couleur]>, <ProductAttributeValue: brun [couleur]>]

a1.product_item.all()
# [<ProductItem: Tshirt [5046]>]

ProductAttributeValue.objects.filter(product_item=i1)
# [<ProductAttributeValue: bleu [couleur]>, <ProductAttributeValue: brun [couleur]>]

ProductAttributeValue.objects.filter(product_item__id=1)
# [<ProductAttributeValue: bleu [couleur]>, <ProductAttributeValue: brun [couleur]>]

# Supprimer une relation many-to-many
# Vous pouvez supprimer un item avec la méthode remove :

i1.attributes.remove(a1)
# Ou dans l'autre sens:

a1.product_item.remove(i1)
# Si vous voulez vider tous les attributs:

a1.product_item.clear()
# Cette syntaxe fonctionne aussi:

a1.product_item = []
