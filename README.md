# q_learning_demo

Contribution to the coding challenge "How to use Q Learning in Video Games Easily" - https://www.youtube.com/watch?v=A5eihauRQvo

Modifications:

- a 50x50 grid layout
- 500 randomly generated walls
- 100 randomly generated red tiles
- 1 randomly generated green tile in the top right corner
- visited tiles will be colored in blue gradually
- a graph that will plot the score for each iteration (reaching the green tile will give a reward of 100 points to visualize successful iterations even better)

Screenshots:

![alt tag](https://github.com/berdy1337/q_learning_demo/blob/master/demo.png)

![alt tag](https://github.com/berdy1337/q_learning_demo/blob/master/figure_1.png)

Close to 300 iterations the bot will find the green tile.
However the bot will get stuck close to the starting tile after approx. 500 iterations. As seen in the chart, the score will then drop significantly before it will plummet to approx. -9000 points.
