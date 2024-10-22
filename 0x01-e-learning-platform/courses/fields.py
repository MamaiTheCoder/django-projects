from django.core.exceptions import ObjectDoesNotExist
from django.db import models

class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields # Fields to filter by
        super().__init__(*args, **kwargs)
    
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # No current value, need to generate a new one
            try:
                qs = self.model.objects.all() # Queryset of all instances
                
                if self.for_fields:
                    # Filter by the fields specified in "for_fields"
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query) # Apply filters to queryset
                    # get the order of the last item
                    last_item = qs.latest(self.attname)
                    value = getattr(last_item, self.attname) + 1 # Increment the last value
                    
            except ObjectDoesNotExist:
                # Start from 0 if no existing items found
                value = 0
            setattr(model_instance, self.attname, value) # Set the new value
            
            return value # Return the new valu
        else:
            return super().pre_save(model_instance, add) # Call parent method if value exists
