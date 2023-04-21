from google.cloud import datastore

# Create a new datastore client
client = datastore.Client()

# Create a new entity
new_entity = datastore.Entity(key=client.key('my-kind'))
new_entity.update({'foo': 'bar'})

# Save the entity to the datastore
client.put(new_entity)

# Retrieve the id of the newly created entity
new_id = new_entity.id

print('New entity created with KEY>ID:', new_entity.key.id)
print('New entity created with ID:', new_entity.id)
