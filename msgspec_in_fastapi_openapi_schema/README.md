In an attempt to speed up my [FastAPI](https://fastapi.tiangolo.com/) application, 
I decided to use [msgspec](https://jcristharif.com/msgspec/) for request and response models. 

Here I suggest an example code to automatically create OpenAPI documentation for handlers with such models.

Run the example:
```
uvicorn example_app:app
```
And open http://127.0.0.1:8000/docs
