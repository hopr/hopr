# Hopr
A hold-and-press pseudo-chorded keyboard remapper.

## What is it?
Hopr lets the user map certain key strokes, called chords, to any other set of keystrokes. The main goal is let the user do more without leving the home row, thereby reducing stress on the fingers and reducing the risk of Repetitive Strain Injuries (RSI). For example, the default configuration contains:

* The arrow keys can be accessed by holding SPACE and pressing J,K,L or SEMICOLON.
* Move up paragraph (CTRL+UP) can be accessed by holding SPACE and pressing U. Similarly for I,O,P.
* V and M are mapped to left and right CONTROL and C,COMMA are mapped to left ALT. That is, holding M and pressing X is the same as pressing CONTROL+X.

This way, most of the common editing keys such as movement, deletion or insertion can be accessed by holding SPACE. Symbols are accessed by holding D or K and a numeric keypad can be accessed on the right hand by holding S.

It works by distinguishing between sequential key presses and hold-and-press key events called chords. For example, during fast normal typing of the characters AB the following key events may be created:

    <PRESS A> <PRESS B> <RELEASE A> <RELEASE B>

Note how the B key is pressed before the A key is released. 

A key stroke is considered a chord if two keys are pressed and the second key is released before the first. For example, pressing and holding B and then pressing and releasing A is detected as a chord and can be mapped to another key stroke:

    <PRESS A> <PRESS B> <RELEASE B> <RELEASE A>
    
Therefore, typing SIM normally results in the text "sim" but holding S and typing IM gives the numbers 81.

The current default key bindings are here: [kbdlayout.pdf](doc/kbdlayout.pdf)

## Motivation
The main goal is to avoid repetitive strain for heavy keyboard users by reducing the load on the weakest fingers. 

## Status
Hopr is currently in a working Linux-only prototype stage. It works but little effort has been spent on setup or configuration. The current goal is to:

* Use it and evaluate if the algorithm works as expected without too many false-positives or other issues.
* Write a windows port so I can use it more often.

## To do

Near future:
* Windows port

Far future:
* Arduino port. Implement as USB box sitting between the keyboard and the computer.

