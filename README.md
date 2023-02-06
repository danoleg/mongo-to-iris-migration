
## About application
This application allows you to import data into IRIS from various sources in a simple way.
Using this application, you can: 
 - Import JSON data into IRIS globals.
 - Export IRIS globals to json files.
 - Transfer data from the MongoDB collections to the IRIS globals. 
 - Transfer data from the PostgreSQL tables to the IRIS globals. 
 
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
```

To run application as a tool, without demo databases.
```
$ docker-compose up -d
```

To run demo:
```
$ docker-compose -f docker-compose.demo.yml up -d
```

By url http://127.0.0.1:8080 will open a demo page with list of MongoDB collections. 

To open collection import manager click button on collection card. On this page, you can migrate data or clear IRIS.
To start migration click on button and wait few seconds. After finishing the page will reload with updated information.

![image](https://user-images.githubusercontent.com/31770269/216854586-b92c12e4-d392-4fe4-972f-5ea37530b579.png)


Importing data from PostgreSQL is similar to MongoDB, only tables instead of collections:

![image](https://user-images.githubusercontent.com/31770269/216854753-433ae03a-a3b9-4b75-a826-d416980c1800.png)


In sidebar you can switch to the JSON importer. It's also very easy to use. Just put your JSON to the textarea and click on the import button.

![image](https://user-images.githubusercontent.com/31770269/216854418-1404fb0d-9abe-4ba3-94e9-37df28841d98.png)


Also you can download IRIS global in json file just in one click.

![image](https://user-images.githubusercontent.com/31770269/216854511-d8ae1c07-51d6-4c75-ac53-dcae687f0d95.png)


In the settings, you can connect remote databases to use the application as a tool.

![image](https://user-images.githubusercontent.com/31770269/216854363-b7190946-2b23-4151-8e6e-ff2c61e1e738.png)
