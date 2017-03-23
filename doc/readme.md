# Hopr - Hold and Press keyboard shortcuts
A pseudo-chorded keyboard remapper.

## What is it?
Hopr is an attempt at creating a more ergonomic keyboard experience by adding a special type of key stroke called chords. Hopr distinguishes between ordinary typing, where the first key is typically released before the second, and chords where the first key is held and the second key is released before the first. Chords can then be mapped to any other key sequence such as arrow `UP` or `CTRL+DEL`.

The main goal is to reduce stress on the hands and fingers by moving hard to reach keys and key combinations to more central positions. All common keyboard actions such as movement, editing, typing etc can be reached without leaving the home row. For example:

* The arrow keys can be accessed by holding `SPACE` and pressing `J,K,L` or `SEMICOLON`. 
* Move up/down paragraph and forward/back word can be accessed by holding `SPACE` and pressing `U,I,O` or `P`.
* Page up/down and Home/End are accessed by holding `SPACE` and pressing `M,COMMA,DOT` or `SLASH`.
* `V` and `M` are mapped as additional `CTRL` keys. That is, holding `M` and pressing `X` is the same as pressing `CTRL+X`

It works by distinguishing between sequential key presses and Hold-and-Press key events called chords. For example, during normal typing of the characters `AB` the following key events may be created:

    <PRESS A> <PRESS B> <RELEASE A> <RELEASE B>

Note that the `B` key is often pressed before the `A` key is released. This is OK since most programs only pay attention to press events.

A key stroke is considered a chord if two keys are pressed and the second key is released before the first. For example, pressing and holding A and then pressing and releasing B is detected as the chord `A+B` and can be mapped to another key stroke:

    <PRESS A> <PRESS B> <RELEASE B> <RELEASE A> -> chord A+B
    
Therefore, typing `SIM` the usual way results in the text `sim` but holding `S` and typing `IM` gives the numbers `81`.

Hopr relies on the order of press and release events to distinguish between normal key strokes and chords. Hopr is not a chorded keyboard in the traditional sense since the order of the key press and release events is important. The order of the held keys is not important though and `AB` and pressing `C` is the same as holding `BA` and pressing `C`. 

### Features

* Keyboard can be used almost like normal. No changes in default keyboard layout or behavior.
* Any key can be used as a modifier. 
* Any pair of keys can be mapped to a different key or set of keys. 
* Ergonomic key bindings. Map common shortcuts such as up-paragraph or delete-word to easy to reach positions. Fingers never leave the home row. 
* Layers group common operations together. For example, `SPACE` for movement and editing, `S` for entering numbers.
* Fewer false positives for fast typists than chorded approaches using timers.
* Reduce stress on the little finger by remapping shift, control, enter etc to the much stronger index finger.

### Side Effects

* Key press and release events are not sent until the key is released. This gives a slight lag which at first makes the keyboard feel sluggish.
* Key event order is not preserved. For example, Press A, Press B, Release A, Release B will be parsed as Press A, Release A, Press B, Release B
* There are still some false-positives. Further testing is needed to see when and why they occur it if further improvements can be made.
* Some chords such as `D+DOT` seem more error prone than others. Key bindings must be evaluated further.

### Default Key bindings
The current default key bindings are here [pdf](doc/kbdlayout.pdf) or here [keybindings.yaml](config/keybindings.yaml).

The key bindings are split into layers named by the activation keys. The default key bindings have two activation keys for each layer, one for the left hand and one for the right. The symbols or actions on the right hand side are activated by holding the activation key on the left hand side. For example, hold D and press J to create a left parenthesis.

It is possible to create chords using only the left or right hand but most combinations would be very unergonomic. 

By default, the `SHIFT, CTRL, ALT` keys are not parsed for chords but all key events are sent directly, unaltered. This allows the keys to be used like normal and prevents some issues with repeated use of `ALT+TAB` or using `SHIFT` during fast typing.

## Status
Hopr is currently in a working Linux-only prototype stage. It works but little effort has been spent on setup, configuration or documentation. The current goal is to:

* Use it and evaluate:
  * If the algorithm works as expected
  * What needs improvement (false-positives etc)
  * If the Hold and Press behavior becomes natural over time
  * If the key bindings are good enough or need modifications.
* Write a Windows or arduino port so I can use it everywhere.



## Motivation
The main goal is to avoid repetitive strain injuries (RSI) for heavy keyboard users by reducing the load on the weakest fingers. The inspiration came from chorded key mappers such as [key-chord](https://www.emacswiki.org/emacs/KeyChord) for Emacs. Many chorded key mappers use a timer to distinguish between chords and normal key strokes. For a fast typist it can be difficult to find the right time interval which is long enough to be usable but short enough not to produce false-positive chords. 

Inspiration for the keyboard layout came from both ergonomic keyboards such as the [Kinesis Advantage](https://www.kinesis-ergo.com/shop/advantage2/) where the thumb is used for many modifier keys and ergonomic keyboard layouts such as [Neo](https://neo-layout.org/index_en.html) which use multiple modifiers to access more keys from the home row.

The disadvantage with large ergonomic keyboards is that they make my laptop much less portable and the disadvantage with most keyboard layouts is that they all keep the unergonomic positions of many frequently used keys such as `CONTROL`, `SHIFT`, `DELETE` etc.

My main goals with Hopr are:

* Ergonomic usage. Reduce use of little finger and hand movements in general to minimize the risk of RSI.
* Transparent usage. All keys should also work as normal. No change in default layout or use. 
* Usable almost everywhere. Both laptops and desktops. In the future, also without installation using a physical box.
* Low level. Allow for use without installation by implementing an Arduino version and creating a USB box that can be plugged in between keyboard and computer. This is on the very distant future wish list.

## Installation

There is no installer or setup yet. You can test it by downloading the source and setting the appropriate permissions. I'm running it on Ubuntu 16.04 so it should work on similar setups.

### Dependencies
The program depends on pyyaml and python evdev 

    apt-get install python-evdev python-yaml

### Quick and Dirty Setup

**Do NOT do this on a multi-user machine or a machine that you do not fully control**

This adds read and write permissions for everyone on all input devices. This is not safe on a multi user machine since any user can read your keyboard input.

Set read and write permissions for all on on `/dev/uinput` and `/dev/input/event*`

    chmod +0006 /dev/input/event*
    chmod +0006 /dev/uinput
   
Then, run the program by executing:

    python <path to installation directory>/hopr/main.py

### Setup with group permissions

This approach gives your own user the right to read and write key events. This is safe unless your user is compromised since a key logger could be installed with your user.

1. Create a group `uinput` and change the group of `/dev/uinput` with a rule in `/etc/udev/rules.d`. See [udev rule](script/misc/91_hopr.rules).
1. Verify that `/dev/input/event*` has group `input`. If not, create a group input and make a udev rule to set the group. See [udev rule](script/misc/91_hopr.rules).
1. Add your own user to groups `input` and `uinput`.


### Setup with hopr user

To avoid giving read and write permissions to your own user, create a new user and follow the steps above to give it the proper permissions. Then run the program as the new user. This is the safest way to run the program since your logged in user does not have the right to read or write keyboard events.

See [create_hopr_user.example](script/misc/create_hopr_user.example) for an example.


