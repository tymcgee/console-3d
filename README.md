# console-3d
3D rendering in a console window

# Example
![demonstration](ico-demo.mp4)

# Notes
Like my other 3D project [here](https://github.com/tymcgee/3d-render), this project was heavily inspired by parts of the video series by javid9x [here](https://youtu.be/ih20l3pJoeU). While I didn't _completely_ copy his code, I figure it's safe for me to attribute it here [(part 1)](https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_olcEngine3D_Part1.cpp) and here [(part 2)](https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_olcEngine3D_Part2.cpp).

I originally implemented that code using
- pygame first, which was quite nice for drawing triangles easily but also quite slow, and
- openGL second, which was quite difficult to learn but ran on the GPU, and so was much faster.

After a while I decided I wanted to do a similar thing but in the console, because the look of ascii characters in 3D is quite pleasing in my opinion. This was also inspired by the classic [spinning donut in C](https://www.a1k0n.net/2011/07/20/donut-math.html).

While doing this project, I learned
- A lot more details about how 3D perspective projection works (although I'm sure I still don't fully understand it)
- How to use `ncurses` to write stuff to a console window
- And much more, I'm sure!

I don't expect to revisit this unless it would be to fix the annoying bug that the width scaling isn't quite right, but I don't really know how to fix that and I'm out of motivation to try. On a 1920x1080 screen with the console taking up the full screen, the scaling should be just about right.

# Requirements
On Linux this should run out of the box, but it takes advantage of `ncurses`, so on Windows you need an `ncurses` clone like `windows-curses`:
```
pip install windows-curses
```
