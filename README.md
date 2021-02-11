# abett-vendors-and-clients-challenge

### Assignments

[Task instructions](https://github.com/kellischeuble/abett-vendors-and-clients-challenge/blob/main/CodingDesignChallenge2.pdf)

### Install

create virtual environment with pipenv

`pip install pipenv`  
`pipenv install -r requirements.txt`  
`pipenv shell`

or from your own virtual environment with Python 3.8 using

`pip install -r requirements.txt`

### Usage

`Connect Neo4j Graph:`

- Download Neo4j Desktop [here](https://neo4j.com/download/)
- Create a new project
- Add a Local DBMS 
- Set a password 
- Click start to activate DBMS
- Click open to see connection information
- In api.py, edit the user, uri, and password variables to match yours

Inside of root folder (same one as Pipfile):

`export PYTHONPATH=./`  
`uvicorn src.api:app --reload`

Go to 
`http://127.0.0.1:800/docs` to play with the swagger documentation!

### Assumptions Made
```
I thought that using a graph datastore would be the easiest way to go about this problem
based on the types of connections between vendors and clients. 
I have never used a graph datastore before and thought Neo4j would be a more simple one
to implement. 
```

### Future Considerations
```
- Make code more DRY
- Error handeling - right now this code assumes that the user
    will be interacting with the api perfectly 
- Testing - test all endpoints, all logic (especially the queries)
- Logging
```

### Test plan
```

```
