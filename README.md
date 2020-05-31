
## About application
Using this application, you can transfer data from the MongoDB collections to the IRIS globals. When data is migrated, a global of the same name is created. The data structure of the collection is reproduced in the IRIS global.

For example, if the first MongoDB document is like this:

```json
{
    "name": "John",
    "info": {
        "age": 25,
        "gender": "male" 
    },
    "emails": [
        "john.1@example.email",
        "john.2@example.email",
        "john.3@example.email"
    ]
}
```

In IRIS it will be:

| path                                | value                |
|-------------------------------------|----------------------|
| ^collection_name(0,"name")          | John                 |
| ^collection_name(0,"info","age")    | 25                   |
| ^collection_name(0,"info","gender") | male                 |
| ^collection_name(0,"emails", 0)     | john.1@example.email |
| ^collection_name(0,"emails", 1)     | john.2@example.email |
| ^collection_name(0,"emails", 2)     | john.3@example.email |

This application uses nativeAPI to work with IRIS.
## How to use it
It is very simple. To start the application, clone project and run the command:
```
$ docker-compose up -d
```

By url http://127.0.0.1:8011/restaurants will open a demo page with a collection of restaurants. 

On this page, you can migrate data or clear IRIS.
To start migration click on button and wait few seconds. After finishing the page reload with updated information.

The demo presents only one collection, but in order to open management of another collection, just change its name in the url path.