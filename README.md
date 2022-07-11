# chess-server

Exercise project combining assignments from multiple companies. The **Assignment 1** is considered the main one - the
domain of the project is "chess combinatorics problems" (corresponds to `chess/`). There are two servers implemented,
one is simplier and matches interface of **Assignment 1**. Second server is a bit more complex as it mimics microservice
architecture (uses messiging queue and database). The second solution is docker-ised.

Both servers lack in tests, validation and overall architecture - which seems quite obvious given the time budget, one
cannot really exhibit how to do things right.

## `chess/`

I spent about 5 hours on the bruteforce solution of the chess problems (implementation + light profiling) and some time
beforehand figuring out if bruteforce is neccesary of if it can be solved by some formula (see on the very bottom of
this file). More tests or more effective execution was not in the time budget. I would also probably change the
architecture to fully separate objects containing logic and data.

The solution includes all rotations/symmetries.

## `server/main.py` - Assignment 1

A simple server that matches the interface proposed in **Assignment 1**. Can be executed (tested on Windows python 3.7,
I attempted to remove all windows-specific code, but not tested) by `pip requirements.txt` and
running `python server/main.py` (slight modification might be necessary like `python3` instead of `python`...)

The server solves the tasks in subprocesses. That way, the server is available for receiving new requests, but (
depending on the tasks) it might take a long time to respond. Which is how I understood the assignment (and also it made
it quite easy to implement given only 2 hours were left in the budget) but it feels like a bit of an anti-pattern (a
rest api that takes long to respond). The second server addresses this issue.

There is a naive caching of results implemented. In the second solution, it morphs into database.

You can explore the api with swagger http://localhost:8000/docs .

## `server/main_mq.py` - Assignment 2

How to run:

- have docker compose on your machine
- Navigate to the project folder
- build the project: `docker-compose build`
- start it: `docker-compose up -d`
- you can use swagger http://localhost:8000/docs#
- or use curl

``` 
  # (tested on windows so `"` instead of `'`, check your systems' curl specifics)
  # create task 
  curl -X "POST"   "http://localhost:8000/chessboard_piece_placer/"   -H "accept: application/json"   -H "Content-Type: application/json"   -d "{ \"piece\": \"bishop\", \"n\": 5}"
  # other valid values for piece: queen, bishop, rook, knight 
  # n should be int 1..9 and get
  # get result
  curl -v http://localhost:8000/chessboard_piece_placer/id_you_recieved_in_post
  ```

What it does: the server (api container) is a fastapi app that receives `POST` requests for creating new "chess tasks" (
read **Assignment 1** if you want to know what the task is) and returns id of the tasks (similar concept to the pdf
tasks in **Assignment 2**). Using a `GET` request you can check on the task (done/processing/unprocessed), if done, the solution is filled.

When the server receives a new task, it creates a corresponding record in the database (postgres container). It uses
mapping of fast api and sqlalchemy models. It also adds the task into rabbitmq where it gets processed by a worker (
workers container).

There is plenty of technical debt (**I am aware of it**).

- credential management
- both python containers contain the same venv (even though each could have a smaller environment)
- tests
- fast api models should be moved from the main script
- this documentation is hard to follow as it describes two projects at once
- many more

> ### Assignment 1
> 
> Create a server that
> 
> - accepts requests in JSON format and returns responses also in JSON format
> - can handle parallel requests
> - can be installed using a package manager
> - has the code reasonably documented and tested The task is to solve the problem of placing N chess figures on a
>   chessboard of size NxN. The result is the number of possible solutions. A solution is a placement of N chess pieces on
>   a NxN chessboard without any of them being attacked by another piece. It does not matter how you deal with symmetrical
>   solutions, you can count each of them or consider them identical and therefore all of them contribute only once. The
>   number of solutions only has to be consistent for every N. Just to be clear:
>   - result for placing queens and N=1 is 1
>   - result for placing queens and N=2 is 0 The requests will have the form {“n”:4, “chessPiece”: “queen”}, where the
>     chessPiece can be one of “queen”, “bishop”, “knight” or “rook”. N is greater than 0 and less than 9. The server
>     response should have the form {“solutionsCount”: 4}. The time and space complexity is not part of the exercise - the
>     call has to return a number eventually, but can take a long time.
> 
> #### General requirements
> 
> - Don’t spend more than 8 hours on the assignment
> - Inform us about the amount of time it took you to finish
> - Resulting code should be available in a publicly accessible Git repository (e.g. Github)
> - Provide instruction on how to compile (if needed) and run
> - Use only freely available tools, libraries and resources

> ### Assignment 2
> 
> Create a service that accepts PDF files containing one or more pages. These pages should be rendered to “normalized png”
> files: they should fit into a 1200x1600 pixels rectangle. 
> 
> The service is accessible through a REST API and offloads all
> file processing to asynchronous tasks (e.g. using dramatiq library), so that it is easy to scale. 
> 
> REST API endpoints:
> - POST /documents 
>   - uploads a file
>   - returns JSON { “id”: “<DOCUMENT_ID>? } 
> - GET /documents/<DOCUMENT_ID>
>   - returns JSON { “status”: “processing|done”, “n_pages”: NUMBER } 
> - GET /documents/<DOCUMENT_ID>/pages/<NUMBER>
>   - return rendered image png
> 
> Implementation 
> ● Python 3, Flask/Django, possibly database (e.g. sqlite, PostgreSQL), message queue
> (e.g. rabbitmq), we recommend dramatiq or similar library ● Should include a simple Dockerfile and docker-compose.yml to
> enable easy testing ○ Feel free to use a template
> 
> Notes 
> ● API should use common practices, e.g. return proper status codes, content-type, etc. ● Consider software
> development best practices ● Include a short README.md that describes how to build the service and how to run example
> conversion using e.g. curl or wget.

## WBS (assignment 1 only)

I created time estimation for tasks of the project, now I can reflect that I underestimated my ability to not care
about the performance (from assignment:  **"The time and space complexity is not part of the exercise"**) and spend
about two hours I did not budget for trying to figure out if there is some way of making the chess part run faster (
utilizing rotations, better code, whatever honestly) - I ended up reducing the amount of object initialization.

The optimization caused that I write this readme after the 8 hours provided (but it did not make sense to ommit this
part).

## Chess Logic

- bruteforce - universal, each piece defines its behaviour, ineffective
- combinatorics - more mental intensive, faster results, not easily extendable for new pieces - short research later: no
  formula have been formulated for the queen -> bruteforce
- pieces:
    - queen: královna (horizontal, vertical and both diagonals)
        - https://kdm.karlin.mff.cuni.cz/diplomky/lucie_chybova_dp/sachove-ulohy.pdf - str 21: pro n=2 a 3 neexistuje
          řešení, pro ostatní N ano (Tabulka 3.1: 4:2 5:10 6:4 7:40 8:92 9:352)
    - bishop: střelec (both diagonals)
    - knight: kůn (L's)
    - rook: věž (horizontal and vertical)
    