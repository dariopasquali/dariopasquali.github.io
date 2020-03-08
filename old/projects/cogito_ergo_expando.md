## Cogito Ergo Expando
<img src="../images/cogito.jpg" width="100%"/>

Group project for the [Artificial Intelligence](http://lia.disi.unibo.it/Courses/AI/fundamentalsAI2018-19/) course in collaboration with [Federico Ruggeri](https://www.linkedin.com/in/federico-ruggeri-a87647145/) e [Sara Bevilaqua](https://www.linkedin.com/in/sara-bevilacqua-00319113a/).

Cogito Ergo Expando is an AI player for Nine Men's Morris boardgame we developed for interal Unibo competition.

### Key Features

#### Internal State
* Internal state representation as an integer array
* Hashing to partially recognize symmetries and rotations.

#### Heuristic Function
* Inspired to [Petcu-Holban](http://www.dasconference.ro/papers/2008/B7.**pdf**) heuristic function

#### Search Algoritm
* Tail recursive search
* Negamax Algorithm
* Alpa-Beta pruning
* Transposition table based on the partiallty symmetric hashcode
