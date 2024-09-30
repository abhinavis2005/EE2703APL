## Assignment 4 

### Approach followed

- I first create a keyboard layout from the qwerty_layout in the file as in the keyboard heatmap programming quiz.

- The keyboard layout is generated using matplotlib rectangles in thhe function 
`genKeyboardLayout`

- My heatmap is a pixel grid of 58 * 16 pixels in x, y coordinates.

- Takes in an input string from the user.

- I then generate two arrays x, y each containing x, y coordinate of each key pressed
for example:
    - if i press a which has coordinates (1.75, 2) 1.75 gets appended to x, and 2 gets appended to y
    - This keeps track of the frequencies with which each coordinate in the keyboard has been pressed.

- I then call the `calculate_key_travel` function which calculates the total distance travelled for pressing the entire text.
it follows the following logic - 
    - 