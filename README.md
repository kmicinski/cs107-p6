# CS 107 Project 6 -- Linked Lists and Path Finding

**Due: Mon, Nov 12, 6PM**

In this project you'll be doing two main things: building a
doubly-linked list and using that implementation to build up a
path-finding algorithm for a small tile-based game. Over the next few
projects, you'll implement various data structures and use their
implementations to build up pieces of a simple (90s-DOS-style) video
game.

On a strategic note, notice that I've given two weeks for this
project. I don't intend on extending the deadline, and I request that
you not underestimate the amount of work in Part 2: it is more
algorithmically challenging than anything you've seen so far in the
class. Specifically, **do not** wait until the second week to start
the project. Also note that there is no style-based grading on this
project.

This will be your first project towards completing HaverQuest, shown
here:

![HaverQuest Gameplay](./gameplay.png)

HaverQuest is a tile-based game, meaning that the game board is
represented as a grid composed of tiles. An individual tile can be
something like a piece of grass, a piece of a wall, etc... A map is a
big matrix of tiles with various properties: grass, walls, and so
on. HaverQuest allows maps to be loaded in a format specified by its
game engine. For example, the above map is represented as a file like
this:

```
# HaverQuest Map Level 1
# G -- Grass
# B -- Grey brick
# R -- Red brick
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGRRRRRRRGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
BBBBBGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGGGGGGGGGGGGGGGGGG
GGGRGGGGGGGGGGGGGGGG
GGGRGGGGGGGGGGGGGGGG
GGGRGGGGGGGGGGGGGGGG
GGGRGGGGGGGGGGGGGGGG
GGGRGGGGGGGGGGGGGGGG
```

The lines that start with `#` are comments, and are ignored by
HaverQuest's engine as it loads the map. The map is comprised of an
n-by-k matrix of characters, where each character stands in for the
name of an image. This configuration is also possible to change in a
file named `config.json`, which specifies the properties of various
tiles.

On top of the map sits various other tiles. For example, there's a
squirrel (the game's main character that you can move with the up,
down, left, and right keys) along with a nut. The goal of the game is
to get to the nut before running out of "fuel." You lose one fuel each
time you make a move (either up, down, left, or right).

Over the course of the next few projects we're going to add a lot of
cool stuff to the game: path finding, firing projectiles, AIs,
etc... I'm pretty excited to see where it goes, and the hope is that
the last project in the class will be to have you build an AI and
compete with other students' AI to see whose works best (but frankly,
I'm not entirely sure what form that will take quite yet).

### Setting up HaverQuest

To run HaverQuest, you'll need to have the `pygame` module
installed. To do this, please run the following command on your
computer (reach out to me if this doesn't work):

    pip3 install pygame

HaverQuest uses `pygame` to perform the work of rendering graphics to
the screen.

You should then be able to run HaverQuest by using the following
command:

    python3 game.py

You should then see the empty game board set up, allowing you to play
the game.

### Don't try to read HaverQuest right now

For this assignment, you won't need to know too much about how
HaverQuest's code works. It's decently large and fairly
complicated. In fact, I ask that you please *not* look into the
implementation too much: you will get confused, and parts of it
contain features of Python's class system which we haven't yet
covered. I will list out the relevant classes and methods down below
and describe how you should use them.

## Part 1: Implementing Doubly-Linked Lists (16 points)

This part will have you implement a *doubly* linked list. Doubly
linked lists are linked lists where each link in the list contains a
reference to both the next element and to the previous element.

This implementation will take place in the file `dllist.py`. I have
implemented `DoubleLink` for you: you should not change its
implementation. I encourage you to read over its implementation to
ensure you understand how it works: it contains three fields: `data`,
`back`, and `nxt`. The tricky thing about a doubly-linked list is that
you need to be careful to account for the back links in the list, so
be apt to that as you work on your implementation.

### **Task: The DLList class**

The methods you need to implement are:

- (2) `add(self, data)`, which adds a piece of data to the *head* of the list
- (2) `size(self)`, which reports the size of the list
- (2) `eq(self, otherList)`, which tells whether or not two lists are equal
- (2) `remove(self, data)`, which removes some piece of data from the list
- (2) `contains(self, data)`, which checks whether or not the list contains some data
- (2) `reverse(self)`, which *reverses* the list
- (2) `toArray(self)`, which converts the list to a Python array (i.e., normal python list)
- (2) `getIth(self, i)`, which returns the ith element

These eight methods comprise 16 points, 8 of which are given in the
public tests, 8 of which are given in the private tests. You will use
this class in your implementation of Part 2 of the project.

My implementation for this part is about ~50 lines, and the code is
fairly straightforward. The most complicated ones to write are
`remove` (be careful to account for what happens when you remove the
first link) and `reverse` (be careful to reset first link), which are
a bit tricky.

#### Tests for Part 1

You can run the public tests for Part 1 using:

    python3 testdlist.py

I encourage you to add your own tests. Doubly-linked lists have
nuanced invariants that you need to think through carefully.

# Part 2: Solving the Game (19 points)

In this part of the project, you will construct an algorithm that
solves a level. If the level is solvable, you will produce a path from
the starting position to the nut, otherwise you will signal that there
is no solution. 

Here's an example of an impossible level:

![Impossible Level](./impossible.png "An impossible level")

By contrast, here's an example of a solution to a level:

![Solution](./solution.png "A solution to a level")

This part of the project will be fairly open-ended, in the sense that
I will give you considerable flexibility with how you implement your
solution. I will sketch out *my* solution, but you can also create
your own as long as it fits within the parameters of the
specification. Specifically, your algorithm must always return an
answer, and must never infinite loop.

### Solving Levels: High-level Idea

Your job in this part is to figure out whether a level has a given
solution. To do this, you will need to know a few things:

- The starting coordinate as an (x,y) pair
- The ending coordinate as an (x,y) pair
- The width / height of the level
- The locations of all of the walls

The game board is a two-dimensional grid. A "move" is either up, down,
left, or right. I typically represent moves as two-tuples, e.g.,
`(1,0)` for right one, or `(0,-1)` for up one. Since our game board is
drawn starting at the top left, moving "up" one tile means subtracting
one from the y coordinate.

In this project, whenever I use the term "path", I am going to mean a
Python array such that the first element of that array is a starting
(x,y) coordinate pair and each subsequent element of the array (after
the first) is either `(1,0)` (right), `(-1, 0)` (left), `(0, -1)`
(up), or `(0, 1)` (down).

For example, here is an animation of the path from `(1,13)` to
`(5,5)`:

![HaverQuest Gameplay](./gameplay.png "A picture of gameplay")

The corresponding path looks like:

```
[(1, 13), (1, 0), (1, 0), (1, 0), (1, 0)
,(0, -1), (0, -1), (0, -1), (0, -1)
, (0, -1), (0, -1), (0, -1), (0, -1)]
```

You can see that we start at `(1, 13)` and then take one move right to
`(2,13)`, etc...

### Finding Solutions to Levels

In this section I give a sketch as to one solution for solving a
level. It is not the only solution, and I encourage you to think about
doing it in whatever way makes sense to you.

In general, path finding algorithms are a somewhat-complex topic. Our
tile-based game will be structured so that it's a bit easier than it
would be usually. I'm not going to give you a full algorithm on how to
perform path finding generally, but instead I'm going to sketch a
simple algorithm that will work for the purposes of this project.

First, consider an empty game board with a squirrel starting at (0,3)
and the nut at (2,0): 

![squirrel at (0,3) and nuts at (2,0)](./ex1.png "squirrel at (0,3) and nuts at (2,0)")

If you want to find out whether it's possible for the squirrel to get
to the nuts, you can take the following approach:

- Keep a list of "next" tiles to explore. Initially, this is just the
  initial tile (which is `(0,3)` in our example).

- Keep a matrix of "already explored" tiles.

- On each move, grab the next tile (call it `cur`) from your "next"
  pile, add it to the list of "already explored" tiles, and add any
  tiles to the up, down, left, or right of `cur` to the list of "next"
  tiles as long as (1) they haven't already been explored, and (2)
  they are possible to explore (within the bounds of the map, do not
  contain a wall).

For example, starting from (0,3), we can add `(0,2)` and `(1, 3)` to
our "next" pile, but not `(-1,3)` or `(0,4)` (since those are both
outside of the map) and also not `(1,2)` (since moves must be either
up, down, left, or right, not right and up at the same time).

This gives us a "next" set of `(0,2)` and `(1,3)` and our `explored`
matrix would contain an entry for `(0,3)` (since we just visited
that).

![After exploring (0,3)](./ex2.png "After exploring (0,3)")

Next, we could choose to visit either `(0,2)` or `(1,3)`. You should
always pull things out of the "next" list in the order in which they
were put on. For example, if we placed `(0,2)` on the "next" list
first, it is important that we pull it off the "next" list first. This
will ensure that we always find the *shortest* path to the solution
(rather than just *a* path).

Let's say that we explored `(0,2)` next, leaving our "next" list
containing only `(1,3)`. Then we would ask: where can we go from
`(1,3)`? We can't go to `(0,3)`, since that's already been explored,
but we *can* go to `(0,1)` and `(1,2)`, so let's add those to the "to
visit" list after `(1,3)` (the tile we could have explored rather than
`(0,2)`). We will also mark `(0,2)` as having been visited. Now, our
"next" tiles list contains the sequence of `[(1,3), (0,1), (1,2)]`:

![After exploring (0,2)](./ex3.png "After exploring (0,2)")

Next, let's visit `(1,3)`. This time we can add `(1,2)` to the next
list (even though it's already there) along with `(2,3)`, and then
mark `(1,3)` as visited:

![After exploring (1,3)](./ex4.png "After exploring (1,3)")

We can keep going and going, until eventually either (a) we reach the
nut or (b) we run out of "next" tiles to explore. Whenever we visit
the nut, we know we've won the game. If instead we get to a point
where we *haven't* reached the nut but there are no more "next" tiles
to explore, we know there is no solution.

#### Accounting for walls

Note that accounting for walls is extremely straightforward: similar
to how you decide not to visit a node outside of the boundaries of the
map, you can decide simply not to visit any node with a wall. This
will be implemented in code as the `canMoveTo` method.

### From solutions to paths

The above method tells you how to check if a solution *exists*. But if
we want to find a *path* to the solution there is a simple tweak: the
"visited" matrix can be modified not just to hold a boolean indicating
whether the tile has been visited, but so that it instead holds a
partial path. Then, when you finally get to the nut you'll have the
entire path that got you there.

![Lists as paths](./ex5.png "Lists as paths")

In this case, the `visited` matrix will contain *either* False (to say
that the coordinate has not yet been explored) *or* a path (which I
suggest you implement as a `DLList`).

## **Task**: The `PathFinder` class

For this part of the project, you will be extending the `PathFinder`
class in `pathfinder.py`. The class contains a few different fields:

- `board`: A reference to an underlying game board. This class is
  defined in `gameboard.py`. Please do not try to read too much of its
  implementation: you won't need to use it to complete the assignment,
  and if you find yourself using it you are doing something wrong.
- `player`: The object representing the squirrel (main character). You
  should not need to touch this at all, but it is useful for the
  beginning coordinates.
- `startX`: The beginning x coordinate of the squirrel
- `startY`: The beginning y coordinate of the squirrel
- `width` / `height`: The width / height of the game board
- `visited`: A width-by-height matrix initially containing False that
  you can use to implement the algorithm

I have implemented one utility method for you, which will check for
the existence of a wall at a given coordinate:

- `wallAt(self,x,y)`: returns `True` if there is a wall at `(x,y)`
  (which are assumed to be within the boundaries of the map)

#### Task 2.1: `canMoveTo(self,x,y)` (2 points)

- Returns `True` if it is possible to visit `(x,y)`. I.e., `(x,y)` is
  within the bounds of the map and doesn't contain a wall.

#### Task 2.2: `checkValidPath` (2 points)

- `validPath(self,path)`: returns `True` if and only if `path` is a
  "valid" path. A path is a Python array whose first element is a
  starting coordinate (which is assumed to be within the boundaries of
  the map and to not contain a wall). Each subsequent element of
  `path` is a tuple representing the direction: `(1,0)` (right),
  `(-1,0)` (left), `(0,-1)` (up), or `(0,1)` (down).

This method returns true whenever the path is "valid:" i.e., it
represents a walk from the starting coordinate to some other point
(not necessarily the nut) without (a) going outside of the map or (b)
walking into a wall.

#### Task 2.3: `canSolve(self, toCoordinate)` (9 points)

- Returns `True` if it is possible to solve the level with a valid
  path from the starting coordinate to `toCoordinate` (an (x,y) tuple
  representing the ending point). If no valid path from the starting
  coordinate to `toCoordinate` exists, returns false.

You will receive no points if your solution "times out" (i.e., runs
forever).

#### Task 2.4: `findPath(self,toCoordinate)` (6 points)

- Returns either `False` or a *valid* path from the starting
  coordinate to `toCoordinate`.

You will receive no points if your solution "times out" (i.e., runs
forever).

### Tests for Part 2

The tests for Part 2 allow you to configure basically every aspect of
the project, and do not require you to run a physical game. To run the
tests do:

    python3 testpathfinder.py

### Visualizing the output

I have modified the game engine so that if you call it like this it
will solve the level and present you with the output as a series of
arrows starting from the (x,y) coordinate:

    python3 game.py solve startX startY endX endY

All of the parameters must be specified, otherwise the game will
complain and exit. If you just use `python3 game.py`, the values of
(startX,startY) and (endX,endY) will be loaded from a configuration
file. This is a fun way to actually see what you've produced, and I
really encourage you to play around with it.

For example, with my solution I get:

    python3 game.py solve 1 1 17 13

![Solving example](./solvingit.png "Solving the level")

### Strategic advice on this part

This part of the project is probably the toughest thing in the course
so far, algorithmically speaking. I suggest that you really sit down
for a long while and sketch out a solution on a piece of paper before
you start coding things up. Remember, coding around hoping to find a
solution when you don't even understand the basic premise of the
project is always a bad idea.

Next, I strongly recommend using elements from your linked-list class
to implement this part of the project. Things like `contains`,
`remove`, and `reverse` will likely be helpful, depending on how you
implement things. Remember that you should always be writing your own
tests. Start with small examples and make sure you understand what
your code is doing before moving on to larger levels.

Last, note that `canSolve` is only superficially different than
`findPath`. In fact, here's my implementation of `canSolve`:

```
    def canSolve(self, toCoordinate):
        return (self.findPath(toCoordinate) != None)
```

The trick is that `findPath` requires a bit more effort than checking
if a solution merely *exists*: it requires actually keeping track of
the path.

I would recommend that you implement `canSolve` first, getting the
basic ideas right, before then moving on to `findPath`

## Scoring Breakdown

- Part 1 (`DLList`):
  - Public tests: X/8
  - Secret tests: X/8
- Part 2 (Level solving):
  - `canMoveTo`
    - Public tests: X/1
    - Secret tests: X/1
  - `checkValidPath`
    - Public tests: X/1
    - Secret tests: X/1
  - `canSolve`
    - Public tests: X/4
    - Secret tests: X/5
  - `findPath`
    - Public tests: X/3
    - Secret tests: X/3
- Total: X/35
