# Hopr - Hold and Press keyboard shortcuts
A pseudo-chorded keyboard remapper.

## What is it?
Hopr lets the user map certain key sequences, called chords, to other keystrokes. The main goal is reduce stress on the hands and fingers by moving hard to reach keys and key combinations to more central positions. All common keyboard actions such as movement, editing, typing etc can be reached without leaving the home row. For example, some of the mappings in the default configuration are:

* The arrow keys can be accessed by holding SPACE and pressing J,K,L or SEMICOLON. 
* Move up paragraph (CTRL+UP) can be accessed by holding SPACE and pressing U. Similarly for I,O,P.
* V and M are mapped as additional CTRL keys. That is, holding M and pressing X is the same as pressing CTRL+X

It works by distinguishing between sequential key presses and hold-and-press key events called chords. For example, during fast normal typing of the characters AB the following key events may be created:

    <PRESS A> <PRESS B> <RELEASE A> <RELEASE B>

Note that the B key is often pressed before the A key is released during fast typing.

A key stroke is considered a chord if two keys are pressed and the second key is released before the first. For example, pressing and holding B and then pressing and releasing A is detected as a chord and can be mapped to another key stroke:

    <PRESS A> <PRESS B> <RELEASE B> <RELEASE A> -> chord A+B
    
Therefore, typing SIM the usual way results in the text "sim" but holding S and typing IM gives the numbers 81.

### Default Keybindings
The current default key bindings are here: [kbdlayout.pdf](doc/kbdlayout.pdf)

The keybindings are split into layers named by the activation keys. The default key bindings have two activation keys for each layer, one for the left hand and one for the right. The symbols or actions on the right hand side are activated by holding the activation key on the left hand side. For example, hold D and press J to create a left parenthesis.

It is possible to create chords using only the left or right hand but most combinations would be very unergonomic. 

By default, the following SHIFT, CTRL, ALT keys are not parsed for chords but all key events are sent directly, unaltered. This allows the keys to be used like normal and prevents some issues like repeated use of ALT+TAB, using shift when typing fast etc. 

## Status
Hopr is currently in a working Linux-only prototype stage. It works but little effort has been spent on setup, configuration or documentation. The current goal is to:

* Use it and evaluate if the algorithm works as expected without too many false-positives or other issues.
* Write a windows port so I can use it more often.
* Testing and modifying the keybindings.

## Motivation
The main goal is to avoid repetitive strain for heavy keyboard users by reducing the load on the weakest fingers. The inspiration came from chorded key mappers such as [key-chord](https://www.emacswiki.org/emacs/KeyChord) for emacs. Many of the chorded the chorded key mappers use a timer to distinguish between chords and normal key strokes. For a fast typist it can be difficult to find the right time interval which is long enough to be usable but short enough not to produce false-positive chords. Instead of using a timer, Hopr relies on the order of press and release events to distinguish between normal key strokes and chords. Strictly speaking, Hopr isn't using chords in the traditional sense since the order of the key press and release events is important. 

### Pros
* Fewer false positives for fast typists than approaches using timers.
* Map common shortcuts such as up-paragraph or delete-word to a single chord. 
* Group layers based on usage such as SPACE for movement and editing, S for entering numbers.
* Fingers never leave the home row. 
* Reduce stress on the little finger by remapping shift, control, enter etc to the much stronger index finger.
* Map common key combinations such as CTRL+UP or SHIFT+ALT+TAB to a single key chord. 

### Cons
* Currently, HOLD key events are ignored. Holding a key does not trigger key repeat.
* Both key press and release events are not sent until the key is released. This gives a slight lag which at first makes the keyboard feel sluggish. I got used to it after a while.
* There are still some false-positives. Further testing is needed to see how, when and why they occur. 
* Key event order is not preserved. For example, Press A, Press B, Release A, Release B will be parsed as Press A, Release A, Press B, Release B


### To do

Main items:

* Repeat key functionality
* Windows port
* Docs, setups, testing etc

In the far future:

* Arduino port. Create a box you can plug in between the keyboard and computer. 
