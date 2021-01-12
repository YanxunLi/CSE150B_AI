Assignment 1: Grid World
=========

DO NOT FORK THIS REPO 
-----
Clone it and work on it locally and never push commits anywhere public.

The task is to find paths from the start (yellow node) to the goal (orange node). Once you load it up and press `enter` you will see what that means. In class I briefly explained the meaning of the different colors of the nodes (green is "grass" that incurs high cost, blue is "puddle" that the agent can not pass through). Check slides, lecture recording, and read the code to figure things out. 

Implement the following search strategies in `algorithms.py`:

- BFS
- Uniform Cost Search
- A\* Search using the Manhattan Distance as the heuristic

You can see the obvious function definitions in the file. Feel free to add more auxiliary functions if needed. You can use other standard Python libraries such as math etc. but they are not really needed. 

Make sure that after you find a path with UCS and A\*, the final cost of the path is passed to the `final_cost` variable in the `Agent` class. Look at Line 60 of `main.py` to see how this value will be used for grading. 

The code for DFS is given to make it easy for you to understand the code. (Expect to spend much more time on reading the code in future assignments.) 

Submission
----
You only need to submit the `algorithms.py` file on Gradescope for grading. 

If you have changed other files, make sure that your implementation works properly with the given `main.py` and `maps.py`, which we will use for grading. 

Usage
----
First, install the Pygame library, it will be used for all assignments in this class. 

Simple run `python main.py` and you will see the grid world window. By pressing `enter` you see how DFS finds a path. Pressing 2, 3, or 4 should run BFS, UCS, A\* in a similay way, which you will implement (and right now it does nothing). 

In the `maps.py` file shows a few test case examples. The `Maps` list contains several input maps and the `Ans` stores the corresponding cost of the optimal path from the start to the goal. To load these maps, pass the following options to the `main.py` file. You can do `python main.py -m 1 -l 0`, which loads the first map `Maps[0]`, or `python main.py -m 1 -l 2` loads `Maps[2]`. Of course it will compain if the index is out of range. You can also do `python main.py -m 2` which autogrades the algorithms with respect to the correct optimal costs. 

The `demo.mov` file shows how the four different search algorithms should roughly behave, in turn. Note that the A\* algorithm shown in the video is very fast and greedy and does not find the optimal path. Your A\* implementation is supposed to use the Manhattan distance, which is a consistent heuristic and will take more steps to find the final path that is guaranteed to be optimal, and it will be faster than UCS. 


Due date
-----
Apr-12 5pm Pacific Time.

Grading
-----
We will have a different set of test cases similar to those in `maps.py` and check if the path your algorithms compute return the right cost values. Of course, we will also run your code and see if your algorithms behave correctly. For instance, if you simply copy the UCS code to A\*, it will still pass the autograder because the optimal cost is the same, but we can easily spot that. 

There are four possible scores, as explained in the first lecture.

- Full (15 points): Everything is correct, passing all tests and implementing the right algorithms.
- Almost (13 points): There are minor mistakes that led to failure of some tests. 
- Half (8 points): Major problems, such as not implementing some of the algorithms, but are in the right direction. 
- Hello (1 point): Almost no attempt but at least you sent something in. 

Note
------
- If you encounter difficulty loading things after installing Pygame, this post https://stackoverflow.com/questions/52718921/problems-getting-pygame-to-show-anything-but-a-blank-screen-on-macos-mojave (in particular, the second answer by "Rafael") may likely help you. 
- You can click mouse to put down more puddles when search is not running.
