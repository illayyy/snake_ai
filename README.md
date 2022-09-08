# Snake AI
An algorithm for the game of snake which utilizes Prim's Minimum Spanning Tree algorithm and Hamiltonian Cycles in order to find an optimal path around the game grid,
while avoiding crashing into itself.

## Prim's Algorithm
Prim's algorithm is a greedy algorithm that finds a Minimum Spanning Tree (MST) in a weighted undirected graph. However in this instance, we use randomized weights
in order to generate an MST that is half the dimensions of our desired game grid, using the tiles of the grid as nodes in the tree.<br/>
It should be noted that due to the fact that the MST needs to be half the dimensions of the game grid, the dimensions of the game grid cannot be odd.

The process of generating the tree is as follows:

1. Choose a random vertex on the graph to be the origin of the tree.
2. Find all vertices that currently border the tree. We will refer to these nodes as the "frontier".
3. Randomly choose a vertex from within the frontier to connect to a vertex on the tree. If there are multiple tree vertices that border the frontier vertex, randomly
pick one of the tree vertices to connect to the frontier vertex.<br/>
(This step simulates the randomized edge weights of the tree)
4. Repeat steps 2 and 3 until tree includes all vertices on the graph.

Finally, we should be left with something that looks a little bit like this:

<p align="center"><img src="https://user-images.githubusercontent.com/104640033/189132481-d4baa011-121e-4b82-8ecf-34a59fa72769.jpg" width="500" height="500"></p>

## Hamiltonian Cycle
A Hamiltonian Cycle is a path in a graph that visits each vertex exactly once, and ends at the same vertex that it begins at.

It's quite simple to visualize how, using Hamiltonian Cycles, we are essentially guaranteed to beat game of snake, every time.<br/>
We simply need to generate a Hamiltonian Cycle for the given game grid, and follow it for the entirety of the game. This way the snake visits each tile exactly once in each "cycle" until it has grown to the
size of the entire game grid, and has hit its' own tail.

However, generating a Hamiltonian Cycle for a given graph has a staggering time complexity of O((2^n)*(n^2)).<br/>
For this reason, we have opted to use a shortcut which takes advantage of our previously generated Minimum Spanning Tree.<br/>

All we need in order to transform our MST into a Hamiltonian Cycle with double the dimensions, is to follow the tree's path like the walls of a maze, making sure to
stick to the same wall for the entire process.
This process can be visualized like this:

<p align="center"><img src="https://user-images.githubusercontent.com/104640033/189141344-2b0e06e9-499b-40a0-a412-cbfe953b2bc6.jpg" width="500" height="500"></p>

## Shortcuts
At this point we should already be set to finish the game of snake.<br/>
However, the approach of following the Hamiltonian Cycle throughout, is extremely boring and makes completing the game take ages, due to the fact that on average, 
it would take the snake half a cycle to eat a single piece of food.<br/>

The solution to this problem is to take shortcuts that bring us closer to the food, without ruining the safety net that is the Hamiltonian Cycle.<br/>

To achieve this, we first have to make one key realization:<br/>
By playing the game using the Hamiltonian Cycle, we have essentially reduced the game of Snake from a 2D game, to a 1D game. Where the one dimension is the one
dimensional array of coordinates on the game grid, ordered using our Hamiltonian Cycle.

<p align="center"><img src="https://user-images.githubusercontent.com/104640033/189149516-56afcb1e-7950-45f4-8e2e-06f2678fca97.jpg"></p>

Using this realization we can also infer that as long as our snake's body remains "ordered" (tail>body>head), within the 1D array of coordinates, it would never
crash into itself.<br/>
This allows us to begin skipping parts of the cycle which do not contribute to us getting closer to the food.

<p align="center"><img src="https://user-images.githubusercontent.com/104640033/189165113-78ef025b-547d-40f2-9dbb-bf77cabe61f6.jpg"></p>

At long last, we can start taking shortcuts around the game grid, seeing as our only restriction now is for our snake to remain ordered.<br/>

To find the optimal shortcut we will first look at all adjacent tiles to the tile that contains the snake's head.<br/>

We will then check which of these adjacent tiles will allow or snake to remain ordered, if we were to move into them. We will refer to these tiles as "legal".<br/>

Finally, for each of these "legal" tiles we will calculate their distance to the food in the Hamiltonian Cycle's 1D array. In other words, how many steps it would take
us if we were to follow the Hamiltonian Cycle from that tile until we arrive at the food.<br/>

And at last, we can pick the "legal" tile that is closest in the cycle to the food, and use it as a shortcut.<br/>

<p align="center"><img src="https://user-images.githubusercontent.com/104640033/189177230-18b1db14-a54d-4a31-abc1-a4a71bc39f0a.jpg"></p>

In the example above, our next tile in the Hamiltonian Cycle is tile #5, which will result in us arriving at the food in 5 additional moves.<br/>
However, tile #9 is also a "legal" tile, since it allows our snake to remain ordered. Furthermore, moving to tile #9 will result in us arriving at the food in 1
additional move.<br/>
Therefore, our algorithm will pick tile #9 as the next move.

It is important to note that this is a algorithm search, as we are not checking every possible path to the food, but only the first available move towards it. 
Therefore it won't always take the most efficient path to the food.<br/>

Finally, the algorithm doesn't take into consideration the fact that eating food extends the snake's body, which can lead the snake to occasionally crash into
itself in the later stages of the game.<br/>

Because of that, we would want the snake to stop taking shortcuts once it has achieved a certain length, which I have chosen to set at 85% of the game's grid
size. Beyond this certain length, the snake will simply follow the Hamiltonian Cycle.<br/>
Keep in mind that even with this bound the snake may on very rare occasions crash into itself, however these events are few and far in between, and occur even
less frequently the larger the game grid is.<br/>

And at long last, we have our Snake AI:

https://user-images.githubusercontent.com/104640033/189197758-2fffa388-61e8-44d2-86ab-e0eab7864ceb.mp4


