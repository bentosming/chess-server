# chess-server

## Memsource evaluation assignment

Python Backend Developer

### General requirements
- Don’t spend more than 8 hours on the assignment
- Inform us about the amount of time it took you to finish
- Resulting code should be available in a publicly accessible Git repository (e.g. Github)
- Provide instruction on how to compile (if needed) and run
- Use only freely available tools, libraries and resources

### Assignment
Create a server that
- accepts requests in JSON format and returns responses also in JSON format
- can handle parallel requests
- can be installed using a package manager
- has the code reasonably documented and tested
The task is to solve the problem of placing N chess figures on a chessboard of size NxN. The
result is the number of possible solutions. A solution is a placement of N chess pieces on a NxN
chessboard without any of them being attacked by another piece. It does not matter how you
deal with symmetrical solutions, you can count each of them or consider them identical and
therefore all of them contribute only once. The number of solutions only has to be consistent for
every N.
Just to be clear:
- result for placing queens and N=1 is 1
- result for placing queens and N=2 is 0
The requests will have the form {“n”:4, “chessPiece”: “queen”}, where the chessPiece can be
one of “queen”, “bishop”, “knight” or “rook”. N is greater than 0 and less than 9. The server
response should have the form {“solutionsCount”: 4}.
The time and space complexity is not part of the exercise - the call has to return a number
eventually, but can take a long time.


## WBS
- přečtení zadnání -> třeba zastropovat řešení, aby vedlo k dokončení, ne k perfekcionalismu (zvládnutelné pod 8h)  - 30 min
- logika kolem rozmístění figurek - 30 minut na problém? (test driven) - 2h
- finální dokumentace puštění a pod - 30 minut rezerva
- vybrání frameworku pro rest api - max 30 minut
- naučení se s frameworkem + jak se v něm má testovat - 1h
- napsání "serveru" + testy - 2h
- rezerva 1,5h (skoro 20%) 

## Logika kolem figurek 
- brutforce - univerzální řešení, stačí nakonfigurovat chování figurek
- využití kombinatoriky a triků - víc mentální práce, lepší výsledek, horší rozšiřitelnost - po krátkém průzkumu - pro královny není vzorec známý podle náhodné mff diplomky -> brutforce/zapamatování známých výsledků
- figurky: 
    - queen: královna (horizontálně, vertikálně, a obě diagonály)
        - https://kdm.karlin.mff.cuni.cz/diplomky/lucie_chybova_dp/sachove-ulohy.pdf - str 21: pro n=2 a 3 neexistuje řešení, pro ostatní N ano (Tabulka 3.1: 4:2 5:10 6:4 7:40 8:92 9:352)
    - bishop: střelec (diagonály)
    - knight: kůn (elka)
    - rook: věž (horizontálně a vertikálně)
    