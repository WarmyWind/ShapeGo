# ShapeGo
A novel Go game made by WarmyWind

# Rules:
Chessboard size is 3x3, black go first.
One can do one of the below three operation in his turn:
1. Drop the pieces: Drop the pieces in the empty place of the board
2. Picking up: Picking up can be carried out when more than 2 pieces are connected. Recall the linked pieces (the whole piece must be taken together, not just a part) and get the corresponding shapes, each of which is marked as unused. A shape has points, equalling to how many pieces it contains. Shapes of the same point can only be obtained once (i.e. after picking up ":", you can no longer picking up ".. ").
3. Convert: Convert your opponent's pieces of the same shape into your own pieces if the shape you collected is unused. After doing convert, the used shape will be marked as used with a tick(√). Note: Shape cannot be rotated.

# Victory conditions:
1. There are no opposing pieces on the board except for the first round.
2. The opponent is unable to take any action during the turn (called trapped dead).
3. Collect the shapes of four different points.
