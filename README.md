
## About application
This application allows you to import data into IRIS from various sources in a simple way.
Using this application, you can: 
 - Import JSON data into IRIS globals.
 - Transfer data from the MongoDB collections to the IRIS globals. 
 
  The data structure of the input data is reproduced in the IRIS global.
 

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

| path                                | value                  |
|-------------------------------------|------------------------|
| ^collection_name(0,"name")          | "John"                 |
| ^collection_name(0,"info","age")    | 25                     |
| ^collection_name(0,"info","gender") | "male"                 |
| ^collection_name(0,"emails", 0)     | "john.1@example.email" |
| ^collection_name(0,"emails", 1)     | "john.2@example.email" |
| ^collection_name(0,"emails", 2)     | "john.3@example.email" |


JSON import is similar.

This application uses nativeAPI to work with IRIS.
## How to use it
It is very simple. To start the application, clone project:
 ```
$ git clone https://github.com/danoleg/mongo-to-iris-migration
```
And run the commands:
```
$ cd client
$ npm install
$ cd ..
$ docker-compose up -d
```

By url http://127.0.0.1:8080 will open a demo page with list of MongoDB collections. 

To open collection import manager click button on collection card. On this page, you can migrate data or clear IRIS.
To start migration click on button and wait few seconds. After finishing the page will reload with updated information.

![image](https://user-images.githubusercontent.com/31770269/171503435-b8761391-6a22-4e25-8070-4515c54b742c.png)

In sidebar you can switch to the JSON importer. It's also very easy to use. Just put your JSON to the textarea and click on the import button.

![image](https://user-images.githubusercontent.com/31770269/171499785-32cd33d8-3cc6-451f-92ab-ecbd5d784630.png)

In the settings, you can connect a remote databases to use the application as a tool.

![image](https://user-images.githubusercontent.com/31770269/171499479-865b88dd-88db-42c8-be84-2630308d1e52.png)