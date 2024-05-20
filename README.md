# Project report: **Optimal placement of the maximum number of dominoes on a square chessboard**

Automated Reasoning Course

**Tam Gabriele 153262**

University of Udine

## Problem Definition

The focus of my project has been the optimal placement of domino tiles on a square chessboard of size n × n. The challenge is to arrange a given set of tiles, each occupying three consecutive cells, without any overlapping or extending beyond the borders of the chessboard. The goal is to maximize the number of placed tiles, ensuring that each tile is adjacent only to tiles with the same value in contiguous cells. Moreover, the range of values for the tiles exceeds the traditional limit of 0 to 6, reaching up to a maximum value k, variable depending on the instance. To address this complexity, I have developed two models: one using MiniZinc, based on constraint programming, and the other through ASP Clingo.

### How the Problem Was Addressed

The approach adopted to tackle the problem was to explore the space of possible solutions, evaluating tile placement configurations and trying to respect the following limits:

- Tiles must not exceed the borders of the chessboard.
- Overlapping of tiles must not occur.
- Adjacent tiles must share the same value in contiguous cells.
- Each tile must be uniquely identifiable and can be placed on the chessboard or not.
- Tiles can be positioned in their original or mirrored version.
- It is possible to place tiles vertically or horizontally.

The objective is to select the configuration that allows maximizing the number of inserted tiles, using the models’ capacity to navigate effectively through the entire solution space.

### Description of Tests

To evaluate the performance of the MiniZinc and Clingo models, I randomly generated 10 batches of 10 problem instances each. To do this, I used a Python script called **create\_input.py** which places inside the **/input** directory 10 ".txt" files, each containing 10 problem instances variable by identifier, difficulty level (easy, medium, hard), set of tiles, and chessboard size. Inside each file, we find:

- Four easy instances that serve to test the models’ capabilities with basic configurations and small-sized chessboards.
- Four medium instances that increase complexity, both in the number of tiles and in the size of the chessboard, requiring a more in-depth exploration of the solution space.
- Two difficult instances, with a high number of tiles and larger chessboards, testing the models’ efficiency in processing complex problems.

Each instance is defined in an input file structured as follows: **id**, **difficulty** , **tiles** , **n**, where **id** is the identifier of the instance, the **difficulty** indicates the level of complexity, the tiles are listed in an array representing the set available for the problem, and **n** denotes the size of the chessboard.

## Minizinc

The first approach tried was with the use of Minizinc. To pass instances to the various models, a well-defined syntax was used, which allowed to transfer each instance to the program, avoiding the need for multiple versions of the code. The structure adopted to communicate the instances to MiniZinc includes:

- **numTiles = m** : Indicates the total number of tiles available.
- **k = a** : Establishes the maximum value present on the tiles, expanding the traditional range.
- **TilesIndex = 1..m** : Defines a set of indices for the tiles.
- **tiles = array2d(TilesIndex, 1..3, [...])** : A two-dimensional array that details the tiles with their respective figures.
- **n = b** : Determines the size of the board, specifying the length of the side of an n x n square matrix.

To facilitate the management and execution of the different problem instances without having to manually adapt the program for each specific configuration, the MiniZinc command with a time limit for execution was employed:

```bash
minizinc –time-limit 300000 program.mzn input.dzn
```

This command runs the MiniZinc model **program.mzn** using the data specified in **input.dzn** , imposing a time limit of 300 seconds (5 minutes) on the search for a solution. The time limit serves to prevent prolonged executions on instances of particular complexity.

To further optimize the workflow, I developed a Python script, **solve\_minizinc.py** , that automates the conversion of problems described in textual format (contained in the files **input.txt** ) into instances directly usable by MiniZinc. This script not only facilitates the preparation of the input instances but also enriches the post-processing analysis through various functions:

- Storing MiniZinc outputs in textual format.
- Collecting solutions from different instances into a CSV file, ready for further analysis.
- Generating a visual representation of the solutions, creating images of the board with the tiles positioned.

## Tile Representation

To represent the placement of domino tiles, I introduced decision variables to represent the positions of the tiles on the game table, as well as categorical variables to define the orientation and state of each tile. The variables used are as follows:

- **posX[TilesIndex]** and **posY[TilesIndex]** indicate the coordinates of each tile on the board.
- **orientation[TilesIndex]** specifies the orientation of each tile, where 0 represents the horizontal orientation and 1 the vertical orientation.
- **inserted[TilesIndex]** denotes the state of each tile, with 0 for tiles not inserted and 1 for those inserted.
- **mirror[TilesIndex]** manages the mirror orientation of the tiles, with 0 for the standard orientation "ABC" and 1 for the mirror orientation "CBA".

These variables ensure that each tile is uniquely identified by a pair of coordinates (X, Y), has a single orientation (horizontal or vertical), a defined state (inserted or not inserted), and a specific version (normal or mirror).

## Constraints for Tile Placement

The correct placement of domino tiles on a board is guaranteed by a set of constraints that I implemented in the MiniZinc code.

### **Constraints to Prevent Tiles from Overlapping and Exiting the Board** These constraints ensure that tiles do not overlap and stay within the game board’s limits.

- **Non-Overlap of Tiles with the Same Orientation** :
- Horizontal: Tiles with the same horizontal orientation do not overlap if they occupy different rows (**posY[i] != posY[j]** ) or if, even though they are on the same row, they are sufficiently spaced apart (**posX[i] + 2 < posX[j]** or **posX[j] + 2 < posX[i]** ).
- Vertical: Similarly, vertical tiles do not overlap if they are on different columns ( **posX[i] != posX[j]** ) or on the same column but spaced apart ( **posY[i] + 2 < posY[j]** or **posY[j] + 2 < posY[i]** ).
- **Non-Overlap of Tiles with Different Orientations** :
- Tiles of different orientations (one horizontal and the other vertical) do not overlap if their extensions do not intersect in the board’s space.
- **Respecting the Board Limits** :
- Horizontal: A horizontal tile respects the board’s limits if the sum of its starting position X and its length does not exceed the board’s size n **(posX[i] + 2 <= n)** .
- Vertical: Similarly, a vertical tile does not exceed the vertical limits if the sum of its starting position Y and its length does not exceed n ( **posY[i] + 2 <= n** ).

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.001.png)

Figure 1: Visual representation of base constraints.

### **Constraints to Ensure Each Pair of Tiles is Correctly Positioned**

Every pair of tiles ( *i*,*j*) must satisfy one of the following cases:

**CASE 1: both tiles i and j are vertical**

- **1A** : the tiles touch each other laterally (on two adjacent columns) and i is to the right of j. The tiles must satisfy one of the following configurations:
- **3 touching squares** : **posX[i] = posX[j] + 1** and **posY[i] = posY[j]** with **value\_i1 = value\_j1** , **value\_i2 = value\_j2** , **value\_i3 = value\_j3** .
- **2 touching squares** : **posX[i] = posX[j] + 1** and **posY[i] = posY[j]+1** with **value\_i1 = value\_j2** , **value\_i2 = value\_j3** , or **posY[i] = posY[j]-1** with **value\_i2 = value\_j1** , **value\_i3 = value\_j2** .
- **1 touching square** : **posX[i] = posX[j] + 1** and **posY[i] = posY[j]+2** with **value\_i1 = value\_j3** , or **posY[i] = posY[j]-2** with **value\_i3 = value\_j1** .
- **1B** : Symmetrical case to 1A (j is to the right of i). The contact configurations are mirror images of 1A with i and j swapping positions.
- **1C**: The two tiles do not touch.

  The two tiles can be in the same column but separated vertically by more than three rows, or in different (non-adjacent) columns. The conditions are:

- **Same column** : **posX[j] = posX[i]** and **posY[i] > posY[j] + 3** or **posY[j] > posY[i] + 3** .
- **Different columns** : **posX[j] < posX[i] - 1** or **posX[i] < posX[j] - 1** .
- **1D** : Same column and only touch at the ends.

  The conditions are:

- **posX[j] = posX[i]** and **posY[i] = posY[j] + 3** with **value\_i1 = value\_j3** , or **posY[j] = posY[i]**

  **+ 3** with **value\_j1 = value\_i3** .

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.002.png)

Figure 2: Visual representation of possible secenaries for case 1A.

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.003.png)

Figure 3: Further visual representation of possible secenaries for case 1.

In each scenario, for every pair of distinct vertical tiles (i and j), one of the described configurations must be satisfied, thus ensuring correct positioning that respects the rules of dominoes and gameplay restrictions.

**CASE 2: tiles i and j are both horizontal**

- **2A** : The tiles touch laterally (on two adjacent rows) and j is above i. This case includes various possibilities for tile contact:
- **3 touching squares** : **posY[i] = posY[j] + 1** and **posX[i] = posX[j]** , the tiles have all matching values (**value\_i1 = value\_j1** , **value\_i2 = value\_j2** , **value\_i3 = value\_j3** ).
- **2 touching squares** : The tiles only partially touch at the sides. For example, if **i** is slightly to the right of **j** (**posX[i] = posX[j]+1** ), then **value\_i1 = value\_j2** and **value\_i2 = value\_j3** . Similarly, if **i** is more to the left ( **posX[i] = posX[j]-1** ), then **value\_i2 = value\_j1** and **value\_i3 = value\_j2** .
- **1 touching square** : means that only one end of the tiles touches. If **i** is much more to the right ( **posX[i]**

  **= posX[j]+2** ), then **value\_i1 = value\_j3** . If **i** is much more to the left ( **posX[i] = posX[j]-2** ), then **value\_i3 = value\_j1** .

- **2B** : Symmetrical case to 2A (j is below i), where the positions and contact conditions of the tiles are reversed compared to 2A but follow the same logic.
- **2C**: Tiles on the same row touching. This occurs when one tile is immediately adjacent to the other, either to the left or right, with at least one matching value between the connecting sides.
- **2D** : Tiles on the same row not touching. This includes scenarios where tiles are in the same row but separated by more than three spaces, or when one tile is positioned such that its values do not match up with the potential connection points of the other tile.

The comprehensive detailing of these rules and configurations highlights how tile placement and interactions are governed in this game, ensuring strategic gameplay and adherence to the game’s fundamental principles.

**CASE 3: one tile is horizontal and the other is vertical (tile i is horizontal and tile j is vertical)**

- **3A** : Horizontal tile above and touches vertical tile below. The horizontal tile (i) is directly above the vertical tile (j), touching it only at the upper edge of j. The values of the tiles must match where they touch. Positions are valid if: **posY[i] + 1 = posY[j]** and **posX[i] <= posX[j] <= posX[i] + 2** . Possible contact configurations:
- **posX[j] = posX[i]** with value\_i1 = value\_j1 (left corner).
- **posX[j] = posX[i] + 2** with value\_i3 = value\_j1 (right corner).
- **posX[j] = posX[i] + 1** with value\_i2 = value\_j1 (center).
- **3B** : Vertical tile on the left and touches horizontal tile on the right. The vertical tile (j) is on the left and touches the horizontal tile (i) that is on its right. Positions are valid if: posX[j] + 1 = posX[i] and posY[i] <= posY[j] <= posY[i] + 2. Possible contact configurations:
- **posY[i] = posY[j]** with value\_j1 = value\_i1 (upper corner).
- **posY[i] = posY[j] + 2** with value\_j3 = value\_i1 (lower corner).
- **posY[i] = posY[j] + 1** with value\_j2 = value\_i1 (center vertically).
- **3C**: Horizontal tile below and touches vertical tile above. The horizontal tile (i) is directly below the vertical tile (j), touching only the lower edge of j. Positions are valid if: posY[i] - 3 = posY[j] and posX[i] <= posX[j] <= posX[i] + 2. Possible contact configurations:
- **posX[j] = posX[i]** with value\_i1 = value\_j3 (left corner).
- **posX[j] = posX[i] + 2** with value\_i3 = value\_j3 (right corner).
- **posX[j] = posX[i] + 1** with value\_i2 = value\_j3 (center).
- **3D** : Vertical tile on the right and touches horizontal tile on the left. The vertical tile (j) is on the right and touches the horizontal tile (i) that is on its left. Positions are valid if: posX[j] = posX[i] + 3 and posY[i] <= posY[j] <= posY[i] + 2. Possible contact configurations:
- **posY[i] = posY[j]** with value\_j1 = value\_i3 (upper corner).
- **posY[i] = posY[j] + 2** with value\_j3 = value\_i3 (lower corner).
- **posY[i] = posY[j] + 1** with value\_j2 = value\_i3 (center vertically).
- **3E**: The vertical tile is positioned on the left and does not touch the horizontal tile. The position is valid if: **posX[j] + 1 < posX[i]** , which means there is at least one column of space between the vertical tile (j) and the horizontal tile (i).
- **3F**: The vertical tile is positioned on the right and does not touch the horizontal tile. The position is valid if: **posX[j] > posX[i] + 3** , indicating that the vertical tile (j) starts at least 1 column after the end of the horizontal tile (i).
- **3G**: Vertical tile is positioned above and does not touch the horizontal tile. The position is valid if: **posY[j]**
  - **3 < posY[i]** , ensuring there is at least one row of space between the end of the vertical tile (j) and the beginning of the horizontal tile (i).
- **3H**: Vertical tile is positioned below and does not touch the horizontal tile. The position is valid if: **posY[j]**

  **> posY[i] + 1** , meaning the vertical tile (j) starts at least one row after the horizontal tile (i).

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.004.png)

Figure 4: Visual representation of possible secenaries for case 3.

<a name="_page7_x511.37_y655.50"></a>**CASE 4: Tile i is horizontal and tile j is vertical (symmetric to CASE 3)**

In CASE 4, we address the inverse situation compared to CASE 3, with tile i positioned horizontally and tile j vertically. This case explores configurations where tiles of different orientations touch or are positioned so as not to interfere with each other, following a logic symmetric to the cases previously described.

<a name="_page8_x56.69_y122.31"></a>**Search Strategies**

Within the scope of the project, I explored four variants of the **solve** directive in MiniZinc to investigate the effectiveness of different search strategies in solving the problem, primarily using the Gecode solver. The common goal of these variants is to maximize the number of domino tiles placed on the board, but each adopts a different approach in the search of the solution space:

1. **Basic Variant** :

   **solve maximize sum(i in TileIndex)(inserted[i]);**

   This basic form simply focuses on the maximization objective without specifying a particular search strategy, relying on the default behavior of the solver.

2. **Input Order Search with inserted** :

   **solve :: int\_search(inserted, input\_order, indomain\_min) maximize sum(i in TileIn- dex)(inserted[i]);**

   By specifying **int\_search** with **input\_order** and **indomain\_min** for the **inserted** variables, this variant aims to optimize the search based on the input order of variables, selecting the minimum values first. The intent is to guide the solver to first explore configurations with fewer tiles inserted: this gives the possibility of always finding a solution even when the problem is very complicated.

3. **Random Search with orientation** :

   **solve :: int\_search(orientation, input\_order, indomain\_random) maximize sum(i in TileIn- dex)(inserted[i]);**

   Using an input order for the **orientation** variables and choosing values randomly ( **indomain\_random** ), this strategy introduces an element of randomness in the search.

4. **Search with posX** :

   **solve :: int\_search(posX, input\_order, indomain) maximize sum(i in TileIndex)(inserted[i]);**

   In this variant, the idea is to systematically examine the possible horizontal positions of the tiles to optimize placement.

To test the effectiveness of these strategies in different environments, I used the Gecode solver for the four variants and compared the results.

Finally, I also tested another solver: Chuffed. It was used only on the basic variant.

Each model was tested on 10 groups of input (containing 10 different problem instances each): having obtained these results, it was then possible to make global evaluations on how each model behaves.

## **ASP Clingo Model**

The second approach adopted to address the problem of the optimal placement of domino tiles on a chessboard utilizes the Clingo solver, a powerful tool based on Answer Set Programming (ASP). Unlike constraint programming used in MiniZinc, Clingo allows describing the problem in terms of logical rules and constraints that must be simultaneously satisfied.

Clingo interprets problem instances through a precise syntax that includes facts and rules. Each tile is described by a fact **tile(id, val1, val2, val3)** , where **id** is a unique identifier and **val1, val2, val3** represent the numerical values of the tile. The size of the chessboard is defined by the fact **size(n)** , which sets the length of the side of the square grid. These elements are essential for determining the possible placement configurations without violating

the problem’s constraints.

To execute the code, use the clingo command with the time limit option, for example:

```bash
**clingo –time-limit=300 clingo\_domino.lp input\_clingo.lp.**
```

The file **clingo\_domino.lp** contains Clingo’s ASP code, while **input\_clingo.lp** is the file with the instances of the specific problem to be solved. As with minizinc, a Python script called **solve\_clingo.py** has been chosen, which transforms problem instances defined in an **input.txt** file into the format accepted by Clingo, executes the solver on these instances, and subsequently collects the results. As with MiniZinc, the script saves the outputs of the executions in text files, creates images representing the solutions found for each chessboard, and compiles a CSV file

with relevant data from each execution, facilitating comparative performance analysis.

### **Tile Representation**

The core of this model is characterized by the **pos\_tile** rule, which determines the ways tiles can be placed. For each tile, uniquely identified by its identifier **T** and values **Val1** , **Val2** , **Val3** , the model explores all possible placement configurations following domino rules and the constraints imposed by the chessboard’s size.

```bash
**1 { pos\_tile(T, I, X, Y, O, 0, Val1, Val2, Val3) : position(X, Y), orientation(O), inserted(I) ; pos\_tile(T, I, X, Y, O, 1, Val3, Val2, Val1) : position(X, Y), orientation(O), inserted(I) } 1 :- tile(T, Val1, Val2, Val3).**
```

This rule specifies that for each tile **T**, there exists a unique valid configuration determining its position **(X, Y)** on the grid, its orientation **O** (0 for horizontal, 1 for vertical), and whether it has been selected to be part of the solution ( **inserted(1)** ) or not ( **inserted(0)** ). The possibility of placing each tile in a mirror image is contemplated, allowing to choose between the original arrangement of values ( **0, Val1, Val2, Val3** ) and the mirror arrangement (**1, Val3, Val2, Val1** ).

Through the syntax **{...} 1** , the program ensures that only one of the possible configurations is selected for each tile, ensuring a consistent and unique assignment.

### **Problem Solving with Clingo**

In the Clingo model, the adopted approach uses logical rules to outline sets of permissible solutions. This methodology focuses on the automatic generation of solutions that simultaneously satisfy all imposed constraints.

#### **Placement and Overlapping Constraints**

The first part of the program ensures to prevent overlapping between tiles and ensures they remain confined to the chessboard limits. These constraints are expressed through logical rules that, if violated, render the proposed set of solutions inadmissible.

- **Chessboard Limits:** To ensure that tiles are placed within the chessboard boundaries, specific constraints are introduced based on orientation. For horizontal tiles, it is prevented from extending beyond the right edge, and for vertical tiles from exceeding the bottom limit. These constraints are formalized as follows:

```bash
**:- pos\_tile(T, 1, X, Y, 0, \_, \_, \_, \_), size(D), X+2 > D. :- pos\_tile(T, 1, X, Y, 1, \_, \_, \_, \_), size(D), Y+2 > D.**
```

- **Preventing Overlap:** Restrictions are imposed to prevent tiles from overlapping, considering both tiles of the same orientation and combinations of horizontal and vertical tiles. For example, two horizontal tiles cannot share the same row if the distance between them is less than the length of a tile. This logic is also extended to interactions between horizontal and vertical tiles, preventing configurations in which they intersect.

#### **Managing Adjacent Tiles**

The model implements detailed rules to manage adjacency between tiles, which is essential to adhere to the fundamental rules of domino:

- **Adjacent Horizontal Tiles:** It ensures that tiles on the same row but in contiguous columns have matching values in the contact cells, implementing the domino rule that requires equal values at adjacent ends.
- **Adjacent Vertical Tiles:** Similarly, for vertical tiles, the code ensures that tiles stacked vertically have matching values in the cells that touch.
- **Interactions between Horizontal and Vertical Tiles:** These rules extend to cover cases where horizontal and vertical tiles touch, imposing that the values in the contact cells be equal.

#### **Implementation and Constraints in Clingo**

The formulation of these constraints in Clingo leverages the use of rules that explicitly exclude invalid configurations (**:-**). This approach allows for a clear and concise definition of the conditions under which tiles can be placed, ensuring the generation of solutions that respect both the physical limits of the chessboard and the rules of the game of domino.

## **Results**

Using the Python scripts **solve\_minizinc.py** and **solve\_clingo.py** , it was possible to automate the solving process for the 10 problem instances provided. Each model was tested on each instance contained in the **/input** folder.

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.005.png)

Figure 5: Analysis of execution<a name="_page10_x306.00_y653.57"></a> time by model and difficulty.

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.006.png)

Figure 6: Impact of chessboard<a name="_page11_x306.00_y437.46"></a> size on execution time.

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.007.png)

Figure 7: Influence of the number<a name="_page12_x306.00_y437.46"></a> of tiles on execution time.

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.008.png)

Figure 8: Distribution of execution<a name="_page13_x306.00_y306.00"></a> time among different models.

Several key points emerge from the analysis:

- There is a common trend among all the models analyzed: as the difficulty of the problems increases, there is an increase in the average time required to reach a solution.
- The difficulty of the problems is significantly affected by both the number of tiles to be entered and the size of the board. In particular, models such as Clingo and Gecode (with "position" and "insert" strategies) show an increase in solving time already when faced with problems of medium difficulty, characterized by a number of tiles between 7 and 9. In contrast, other Gecode solvers do not show criticality until 16 tiles are reached, at which point the resolution time begins to increase. Chuffed, on the other hand, demonstrates remarkable stability, maintaining low resolution times regardless of difficulty.
- Analyzing the impact of chessboard size, a similar dynamic is observed: Clingo and the Gecode model based on the "position" strategy show difficulty already with chessboards larger than 5x5. In contrast, the other models begin to show slowdowns only with chessboards larger than 10x10 in size.
- Of all the solvers examined, Chuffed emerges as the best performing, managing to optimize search and complete proposed problems faster than both the other models implemented in MiniZinc and in comparison with Clingo. Its ability to maintain low resolution times regardless of the difficulty of the problem positions it as the solver of choice in the analysis conducted.

### **Further Considerations**

Given the excellent performance of the model executed with the Chuffed solver, curiosity arose to explore its limits. To do this, significantly more complex problem instances were generated compared to the initial ones. The goal was to test the robustness and efficiency of the solver against greater challenges.

![](Aspose.Words.8d93dda9-9b38-417b-b785-08f08a1029c4.009.png)

Figure 9: Average execution times with much more difficult instances (with a very<a name="_page14_x407.39_y217.32"></a> high number of tiles to insert/evaluate).

<a name="_page14_x56.69_y283.58"></a>**Conclusions**

The presented project focuses on optimizing the placement of dominoes on square checkerboards of varying sizes, attempting to maximize the number of tiles placed on the game plane. Through the use of two distinct computational approaches (Minizinc and ASP Clingo), it was possible to effectively explore and analyze the space of possible solutions, while respecting specific constraints such as avoiding overlaps, respecting the boundaries of the chessboard, and ensuring the consistency of values between adjacent tiles.

Analysis of the results showed that the complexity of the problem affects the solving time, with significant variations depending on the number of tiles and the size of the chessboard, as well as on the solver model used. In particular, the Chuffed solver stood out for efficiency, showing low resolution times even in the most difficult situations.
14
